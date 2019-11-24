API_IMAGE = cytopia/flagodo
API_DIR   = api
API_FILE  = Dockerfile

WEB_IMAGE = cytopia/web
WEB_DIR   = web
WEB_FILE  = Dockerfile

UID = 1000
GID = 1000

# --------------------------------------------------------------------------------------------------
#  Default Target
# --------------------------------------------------------------------------------------------------

help:
	@echo "TODO"


# --------------------------------------------------------------------------------------------------
#  Build Targets
# --------------------------------------------------------------------------------------------------

build: build-api build-web

build-api: build-api-dev build-api-prod

build-api-dev:
	docker build --target development --build-arg UID=$(UID) --build-arg GID=$(GID) -t $(API_IMAGE):dev -f $(API_DIR)/$(API_FILE) $(API_DIR)

build-api-prod:
	docker build --target production --build-arg UID=$(UID) --build-arg GID=$(GID) -t $(API_IMAGE):prod -f $(API_DIR)/$(API_FILE) $(API_DIR)

build-web:
	docker build -t $(WEB_IMAGE) -f $(WEB_DIR)/$(WEB_FILE) $(WEB_DIR)


# --------------------------------------------------------------------------------------------------
#  Run Targets
# --------------------------------------------------------------------------------------------------

run-api-dev:
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		--name flagodo-api \
		-v $(PWD)/api/src:/home/flagodo/flagodo/src \
		-p "8090:8080" $(API_IMAGE):dev $(ARGS)

run-api-prod:
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		--name flagodo-api \
		-p "8090:8080" $(API_IMAGE):prod $(ARGS)


# --------------------------------------------------------------------------------------------------
#  Compose Targets
# --------------------------------------------------------------------------------------------------

start:
	docker-compose up -d

stop:
	docker-compose down
