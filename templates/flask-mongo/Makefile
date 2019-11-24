APP_IMAGE = app
APP_DIR   = app
APP_FILE  = Dockerfile

WEB_IMAGE = web
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

build: build-app build-web

build-app: build-app-dev build-app-prod

build-app-dev:
	docker build --target development --build-arg UID=$(UID) --build-arg GID=$(GID) -t $(APP_IMAGE):dev -f $(APP_DIR)/$(APP_FILE) $(APP_DIR)

build-app-prod:
	docker build --target production --build-arg UID=$(UID) --build-arg GID=$(GID) -t $(APP_IMAGE):prod -f $(APP_DIR)/$(APP_FILE) $(APP_DIR)

build-web:
	docker build -t $(WEB_IMAGE) -f $(WEB_DIR)/$(WEB_FILE) $(WEB_DIR)


# --------------------------------------------------------------------------------------------------
#  Run Targets
# --------------------------------------------------------------------------------------------------

run-app-dev:
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		--name app-dev \
		-v $(PWD)/app/src:/home/myuser/project/src \
		-p "8080:8080" $(APP_IMAGE):dev $(ARGS)

run-app-prod:
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		--name app-prod \
		-p "8080:8080" $(APP_IMAGE):prod $(ARGS)


# --------------------------------------------------------------------------------------------------
#  Compose Targets
# --------------------------------------------------------------------------------------------------

start:
	docker-compose up -d

stop:
	docker-compose down
