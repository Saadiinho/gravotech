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
	PYTHONPATH=. .venv/bin/pylint ./app/ ./libs/ ./tests/

# lint-app: run pylint on the app directory
.PHONY: lint-app
lint-app:
	PYTHONPATH=. .venv/bin/pylint ./app/

# lint-libs: run pylint on the libs directory
.PHONY: lint-libs
lint-libs:
	PYTHONPATH=. .venv/bin/pylint ./libs/

# lint-tests: run pylint on the tests directory
.PHONY: lint-tests
lint-tests:
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
	bandit -r app/api/*.py
	bandit -r libs/actions/*.py
	bandit -r libs/core/*.py
	bandit -r libs/server/*.py
	bandit -r libs/streamers/*.py
	bandit -r libs/utils/*.py
	bandit -r tests/*.py

# ==================================================================================== #
# START SERVER AND CLIENT AND GENERATE SCRIPTS
# ==================================================================================== #

# fake-graveuse: lunch a fake graveuse
.PHONY: fake-graveuse
fake-graveuse:
	PYTHONPATH=. .venv/bin/python3 libs/server/dumb_gravotech.py

# ==================================================================================== #
# DOCKER BUILD
# ==================================================================================== #

.PHONY: build-server
build-server:
	docker build --no-cache -t graveuse_fake -f ./docker/server.Dockerfile .

.PHONY: build-api
build-api:
	docker build -t graveuse_api -f ./docker/Dockerfile .


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

.PHONY: run-server
run-server:
	docker compose --env-file .env -f ./docker/docker-compose.yml --project-directory . up graveuse_fake

.PHONY: run-api-prod
run-api-prod:
	docker compose --env-file .env.prod -f ./docker/docker-compose-prod.yml --project-directory . up realtime_api


.PHONY: run
run:stop
	docker compose --env-file .env -f ./docker/docker-compose.yml --project-directory . up
