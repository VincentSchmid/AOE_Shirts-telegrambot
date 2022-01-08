include params.mk

# DEFINED VARIABLES:
	# SHIRT_POROCESSING_ADDRESS
	# TELEGRAM_TOKEN
	# GCLOUD_PROJECT_ID
	# CONTAINER_NAME
	# LOCAL_PORT
	# CONFIG_FILE
	# USERNAME

.DEFAULT_GOAL := build-container

gcloud-build:
	gcloud builds submit --tag gcr.io/$(GCLOUD_PROJECT_ID)/$(CONTAINER_NAME) --project=$(GCLOUD_PROJECT_ID)

gcloud-deploy:
	gcloud run deploy $(CONTAINER_NAME) --image=gcr.io/$(GCLOUD_PROJECT_ID)/$(CONTAINER_NAME) --set-env-vars TOKEN=$(TELEGRAM_TOKEN),SHIRT_POROCESSING_ADDRESS=$(SHIRT_POROCESSING_ADDRESS),CONFIG_FILE=$(CONFIG_FILE) --project=$(GCLOUD_PROJECT_ID)  --platform=managed --allow-unauthenticated --region=$(GCLOUD_REGION) --memory=256Mi
	
gcloud-link:
	SERVICE_URL="$(shell gcloud run services describe ${CONTAINER_NAME} --format 'value(status.url)' --project $(GCLOUD_PROJECT_ID))"; \
	curl "https://api.telegram.org/bot${TELEGRAM_TOKEN}/setWebhook?url="$$SERVICE_URL

gcloud-run: gcloud-build gcloud-deploy gcloud-link ## Deploys code to gcloud and links telegram bot to deployed instance

container-build: ## Builds the container (default target)
	docker build -t $(USERNAME)/$(CONTAINER_NAME) .

container-deploy: container-build ## Builds the container and runs it locally
	-docker stop $(CONTAINER_NAME)
	-docker rm $(CONTAINER_NAME)
	docker run --env PORT=$(LOCAL_PORT) --env SHIRT_POROCESSING_ADDRESS=$(SHIRT_POROCESSING_ADDRESS) --env TOKEN=$(TELEGRAM_TOKEN) --env CONFIG_FILE=${CONFIG_FILE} --name $(CONTAINER_NAME) -d schmivin/$(CONTAINER_NAME)
	# docker exec -t -i $(CONTAINER_NAME) /bin/bash

local-run: ## Runs app localy without container
	export TOKEN=$(TELEGRAM_TOKEN) && \
	uvicorn main:app --reload --port ${LOCAL_PORT}

test: ## Runs test and return coverage report
	pytest --cov=src tests/

.PHONY: help

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
