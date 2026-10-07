start:
	python3 scripts/validate-versions.py --check-env
	docker compose -f docker-compose.local.yml up -d

stop:
	docker compose -f docker-compose.local.yml down

restart:
	python3 scripts/validate-versions.py --check-env
	docker compose -f docker-compose.local.yml down && docker compose -f docker-compose.local.yml up -d

health:
	bash scripts/healthcheck.sh

validate:
	python3 scripts/validate-versions.py
	bash scripts/validate-workflows.sh
	bash scripts/validate-secrets.sh

