import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "workflows" / "telegram-approval.json"


class TelegramWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = json.loads(WORKFLOW.read_text())
        cls.nodes = {node["name"]: node for node in cls.workflow["nodes"]}
        cls.connections = cls.workflow["connections"]

    def test_source_workflow_is_not_claimed_active(self):
        self.assertIs(self.workflow["active"], False)

    def test_separates_notifications_from_decisions(self):
        self.assertIn("Telegram Decision Adapter", self.nodes)
        self.assertIn("Telegram Notification Adapter", self.nodes)
        decision = json.dumps(self.nodes["Telegram Decision Adapter"])
        notification = json.dumps(self.nodes["Telegram Notification Adapter"])
        self.assertIn("sosd:", decision)
        self.assertNotIn("callback_data", notification)
        self.assertNotIn('"callback_data": "approve"', decision)
        self.assertNotIn('"callback_data": "reject"', decision)

    def test_callback_execution_is_gated_by_owner_and_gateway(self):
        verification = self.nodes["Verify Owner and Callback Envelope"]["parameters"]["jsCode"]
        classification = self.nodes["Enforce Gateway Decision Result"]["parameters"]["jsCode"]
        self.assertIn("TELEGRAM_OWNER_CHAT_ID", verification)
        self.assertIn("TELEGRAM_OWNER_USER_ID", verification)
        self.assertIn("passport_authorized === true", classification)
        self.assertIn("d.outcome === 'accepted'", classification)
        self.assertIn("d.decision === 'approve'", classification)
        true_branch = self.connections["Approved and Authorized?"]["main"][0]
        self.assertEqual(true_branch[0]["node"], "S-OS Execute Approved Command")

    def test_gateway_credentials_are_references_not_secrets(self):
        serialized = WORKFLOW.read_text()
        self.assertIn("S-OS Passport Gateway (private)", serialized)
        self.assertNotIn("Bearer ", serialized)
        self.assertNotIn("TELEGRAM_BOT_TOKEN", serialized)


if __name__ == "__main__":
    unittest.main()
