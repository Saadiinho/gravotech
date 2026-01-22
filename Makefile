# ==================================================================================== #
# VARIABLES
# ==================================================================================== #
TEST_DIR := tests/

# ==================================================================================== #
# HELPERS
# ==================================================================================== #
# help: print this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ":" | sed -e 's/^/ /'


# ==================================================================================== #
# CHECK QUALITY OF CODE
# ==================================================================================== #

# lint-score: extract score of kynt project
.PHONY: lint-score
lint-score:
	PYTHONPATH=. pylint ./app/ ./libs/ ./tests/ | grep "Your code has been rated at" | awk '{print $(NF-1)}' | awk -F '/' '{print $1}'

# lint-all: run pylint on the libs directory
.PHONY: lint
lint:
	PYTHONPATH=. .venv/bin/pylint ./app/ ./tests/

# lint-app: run pylint on the app directory
.PHONY: lint-app
lint-app:
	PYTHONPATH=. .venv/bin/pylint ./app/

# lint-test: run pylint on the tests directory
.PHONY: lint-test
lint-test:
	PYTHONPATH=. .venv/bin/pylint ./tests/


# ==================================================================================== #
# UNIT TEST OF CODE
# ==================================================================================== #

# test: run pytest on the tests directory
.PHONY: test
test:
	pytest $(TEST_DIR)

# ==================================================================================== #
# Format
# ==================================================================================== #

# black: run black on the current directory
.PHONY: black
black:
	.venv/bin/black .

# black_check: Verify code formatting with black.
.PHONY: black-check
black-check:
	black --check .


# ==================================================================================== #
# SECURE VERIFICATION
# ==================================================================================== #

# bandit: verification of security in the code
.PHONY: bandit
bandit:
	bandit -r app/actions/*.py
	bandit -r app/api/*.py
	bandit -r app/core/*.py
	bandit -r app/streamers/*.py
	bandit -r app/utils/*.py
	bandit -r tests/*.py

# ==================================================================================== #
# START SERVER AND CLIENT AND GENERATE SCRIPTS
# ==================================================================================== #

# server: lunch server
.PHONY: server
server:
	PYTHONPATH=. .venv/bin/python3 app/server/main.py

# client: lunch client
.PHONY: client
client:
	PYTHONPATH=. .venv/bin/uvicorn app.client.api:app --host 0.0.0.0 --port 8000

# generate: generate scripts of server and mdd
.PHONY: generate
generate:
	PYTHONPATH=. .venv/bin/python3 app/generation/generate_script.py
	make black


# ==================================================================================== #
# DOCKER BUILD
# ==================================================================================== #

.PHONY: build-server
build-server:
	docker build --no-cache -t realtime_server -f ./docker/server.Dockerfile .

.PHONY: build-api
build-api:
	docker build -t realtime_api -f ./docker/Dockerfile .


# ==================================================================================== #
# DOCKER STOP
# ==================================================================================== #

.PHONY: stop
stop:
	docker compose -f ./docker/docker-compose.yml  --project-directory . down

.PHONY: stop-servers
stop-servers:
	docker compose -f ./docker/docker-compose-server.yml --project-directory . down

# ==================================================================================== #
# DOCKER RUN
# ==================================================================================== #

.PHONY: run-server2
run-server2: build-server
	docker compose --env-file .env.api2 -f ./docker/docker-compose.yml --project-directory . up realtime_server2 -d

.PHONY: run-server3
run-server3:
	docker compose --env-file .env.api3 -f ./docker/docker-compose.yml --project-directory . up realtime_server3 -d

.PHONY: run-servers
run-servers: build-server
	docker compose -f ./docker/docker-compose-server.yml --project-directory . up -d

.PHONY: run-api
run-api:
	docker compose --env-file .env.api -f ./docker/docker-compose.yml --project-directory . up realtime_api

.PHONY: run-api-prod
run-api-prod:
	docker compose --env-file .env.prod -f ./docker/docker-compose-prod.yml --project-directory . up realtime_api


.PHONY: run
run:stop
	docker compose --env-file .env -f ./docker/docker-compose.yml --project-directory . up
