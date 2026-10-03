import {readFileSync, readdirSync} from 'node:fs';
import assert from 'node:assert/strict';
import {test} from 'node:test';

const workflow=JSON.parse(readFileSync('workflows/s-orchestrator-hourly.json','utf8'));
const node=name=>workflow.nodes.find(n=>n.name===name);
const select=(rows,env={})=>new Function('$input','$execution','$env',node('Keep Active Rows').parameters.jsCode)({all:()=>rows.map(json=>({json}))},{id:'run-1'},env);
const decide=row=>new Function('$json',node('Assign Owner and Decide').parameters.jsCode)(row).json;
const source=decide({'Task ID':'AC-test',row_number:2,Status:'Active','Has Value':'yes',Authorized:'yes','Next Action':'Safe synthetic operation','Approval Status':'approved','Approval Reference':'approval-1','Updated At':'2026-10-03T00:00:00Z',_runId:'run-1',_selection:{priorityRank:1}});
const verify=(input,row=source)=>new Function('$json','$',node('Verify Delivery Receipt').parameters.jsCode)(input,()=>({item:{json:row}})).json;
const receipt={id:'receipt-1',taskId:'AC-test',runId:'run-1',idempotency_key:source._followUp.idempotencyKey,approval_reference:'approval-1',status:'completed'};

test('one canonical hourly schedule, inactive until live acceptance',()=>{
 const schedules=readdirSync('workflows').flatMap(path=>JSON.parse(readFileSync('workflows/'+path)).nodes.filter(n=>n.type==='n8n-nodes-base.scheduleTrigger' && n.parameters.rule.interval.some(i=>i.field==='hours')));
 assert.equal(schedules.length,1);
 assert.equal(workflow.active,false);
 assert.equal(workflow.settings.timezone,'Asia/Dubai');
 assert.deepEqual(node('Every Hour').parameters.rule.interval,[{field:'hours',hoursInterval:1}]);
 assert.ok(workflow.connections['Manual Evidence Run']);
});

test('archive rows survive selection and keep their original item association',()=>{
 const items=select([{row_number:4,'Task ID':'AC-normal',Status:'Active',Priority:'P2'},{row_number:2,'Task ID':'AC-obsolete',Status:'Obsolete',Priority:'P0'}]);
 assert.equal(items[0].json['Task ID'],'AC-obsolete');
 assert.deepEqual(items[0].pairedItem,{item:1});
 assert.equal(decide(items[0].json)._followUp.disposition,'archive');
 assert.equal(decide(items[0].json)['Execution Owner'],'');
});

test('authorized row alone does not manufacture approval evidence',()=>{
 for(const patch of [{'Approval Reference':''},{'Approval Status':'pending'},{'Updated At':''},{'Updated At':'not a date'},{'Task ID':'x'.repeat(129)}]) {
  assert.equal(decide({...source,...patch})._followUp.disposition,'hold');
 }
 assert.equal(source._followUp.disposition,'execute');
 const repeated=decide({...source,_runId:'run-2'});
 assert.equal(repeated._followUp.idempotencyKey,source._followUp.idempotencyKey);
});

test('acceptance allowlist isolates synthetic work from real tasks',()=>{
 const rows=[{row_number:2,'Task ID':'AC-real',Status:'Active',Priority:'P0'},{row_number:3,'Task ID':'AC-synthetic',Status:'Active',Priority:'P1'}];
 assert.deepEqual(select(rows,{ASSISTANT_ACCEPTANCE_TASK_IDS:' AC-synthetic '}).map(i=>i.json['Task ID']),['AC-synthetic']);
 assert.equal(select(rows,{ASSISTANT_ACCEPTANCE_TASK_IDS:'AC-missing'}).length,0);
});

test('owner decisions escalate, ordinary waiting stays silent',()=>{
 assert.equal(decide({...source,'Outcome Decision Required':'yes'})._followUp.disposition,'escalate');
 assert.equal(decide({...source,'Next Action':'',Authorized:'no'})._followUp.disposition,'hold');
});

test('HTTP 200 gateway routing is not a worker receipt',()=>{
 const result=verify({statusCode:200,body:{ok:true,result:{accepted_by_gateway:true}}});
 assert.equal(result._delivery.accepted,false);
 assert.equal(result._delivery.disposition,'delivery_failed');
 assert.equal(result._delivery.outcome,'Delivery unverified; reconcile before retry');
});

test('HTTP failures, transport errors and mismatched receipts remain unverified',()=>{
 for(const response of [{statusCode:500,body:{ok:true,receipt}},{error:'secret-error-payload'},{statusCode:200,body:{ok:false,receipt}},...['taskId','runId','idempotency_key','approval_reference','status','id'].map(key=>({statusCode:200,body:{ok:true,receipt:{...receipt,[key]:'invalid value'}}}))]) {
  const result=verify(response);
  assert.equal(result._delivery.accepted,false);
  assert.ok(!JSON.stringify(result).includes('secret-error-payload'));
 }
});

test('worker success requires task, run, approval and idempotency binding',()=>{
 const result=verify({statusCode:200,body:{ok:true,receipt}});
 assert.equal(result._delivery.accepted,true);
 assert.equal(result._delivery.disposition,'execute');
 assert.equal(result._delivery.outcome,'Receipt receipt-1');
});

test('unverified dispatch is quarantined until explicit reconciliation',()=>{
 const row={...source,'Last Follow-up':new Date(Date.now()-6*3600000).toISOString(),'Updated At':'2026-01-01','Follow-up Disposition':'delivery_failed'};
 assert.equal(select([row]).length,0);
 assert.equal(select([{...row,'Updated At':new Date().toISOString()}]).length,1);
});

test('new invocation uses configured gateway and bounded timeout without retries',()=>{
 const worker=node('Route to Worker');
 assert.equal(worker.parameters.url,'={{ $env.S_AGENTOS_COMMAND_URL }}');
 assert.ok(worker.parameters.headerParameters.parameters.some(h=>h.name==='X-AgentOS-Key'));
 assert.equal(worker.retryOnFail,false);
 assert.equal(worker.parameters.options.timeout,30000);
 assert.equal(worker.parameters.options.response.response.fullResponse,true);
 assert.equal(node('Escalate Decision to Seif').parameters.sendHeaders,true);
});

test('every disposition passes delivery verification before audit and row write-back',()=>{
 for(const name of ['Route to Worker','Escalate Decision to Seif','Archive Obsolete Definition','Keep Working Silently'])
  assert.equal(workflow.connections[name].main[0][0].node,'Verify Delivery Receipt');
 assert.equal(workflow.connections['Append Redacted Audit Evidence'].main[0][0].node,'Link Evidence to Assistant Control');
 assert.ok(node('Append Redacted Audit Evidence').parameters.columns.value.Outcome.includes('_delivery.outcome'));
 assert.ok(node('Link Evidence to Assistant Control').parameters.columns.value['Follow-up Disposition'].includes('_delivery.disposition'));
 for(const d of ['archive','hold']) assert.equal(verify({}, {...source,_followUp:{...source._followUp,disposition:d}})._delivery.accepted,true);
});
