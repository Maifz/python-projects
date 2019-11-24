ifneq (,)
.error This Makefile requires GNU Make.
endif


# -------------------------------------------------------------------------------------------------
# Default configuration
# -------------------------------------------------------------------------------------------------
TPL_DIR   = $(PWD)

APP_IMAGE = app
APP_DIR   = $(TPL_DIR)/app
APP_FILE  = Dockerfile

WEB_IMAGE = web
WEB_DIR   = $(TPL_DIR)/web
WEB_FILE  = Dockerfile

UID = 1000
GID = 1000


# --------------------------------------------------------------------------------------------------
# Default Target
# --------------------------------------------------------------------------------------------------

help:
	@echo "init         Initialize project"
	@echo "build        Build Docker images"
	@echo "start        Start Docker Compose"
	@echo "stop         Stop Docker Compose"


# --------------------------------------------------------------------------------------------------
# Init Target
# --------------------------------------------------------------------------------------------------

init: requirements.txt src/app.py .env


# --------------------------------------------------------------------------------------------------
# Build Targets
# --------------------------------------------------------------------------------------------------

build: build-app build-web

build-app: build-app-dev build-app-prod

build-app-dev: _copy_source
	docker build --target development --build-arg UID=$(UID) --build-arg GID=$(GID) -t $(APP_IMAGE):dev -f $(APP_DIR)/$(APP_FILE) $(APP_DIR)

build-app-prod: _copy_source
	docker build --target production --build-arg UID=$(UID) --build-arg GID=$(GID) -t $(APP_IMAGE):prod -f $(APP_DIR)/$(APP_FILE) $(APP_DIR)

build-web:
	docker build -t $(WEB_IMAGE) -f $(WEB_DIR)/$(WEB_FILE) $(WEB_DIR)


# --------------------------------------------------------------------------------------------------
# Run Targets
# --------------------------------------------------------------------------------------------------

run-app-dev:
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		--name app-dev \
		-v $(APP_DIR)/src:/home/myuser/project/src \
		-p "8080:8080" $(APP_IMAGE):dev $(ARGS)

run-app-prod:
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		--name app-prod \
		-p "8080:8080" $(APP_IMAGE):prod $(ARGS)


# --------------------------------------------------------------------------------------------------
# Compose Targets
# --------------------------------------------------------------------------------------------------

restart: stop start

start: build
	cd $(TPL_DIR) && docker-compose up -d

stop:
	cd $(TPL_DIR) && docker-compose down
	cd $(TPL_DIR) && docker-compose rm -f




# --------------------------------------------------------------------------------------------------
# Helper Targets
# --------------------------------------------------------------------------------------------------

.PHONY: _copy_source
_copy_source: init
	cp -rf src $(APP_DIR)
	cp -f requirements.txt $(APP_DIR)/requirements.txt
	cp -f .env $(TPL_DIR)/.env

.env:
	cp $(TPL_DIR)/.env.example .env

requirements.txt:
	@echo "flask" > requirements.txt

src/app.py:
	mkdir -p src
	@echo "\"\"\"Flask hello world app.\"\"\"" > src/app.py
	@echo "from flask import Flask" >> src/app.py
	@echo >> src/app.py
	@echo "app = Flask(__name__)" >> src/app.py
	@echo >> src/app.py
	@echo >> src/app.py
	@echo "@app.route(\"/\")" >> src/app.py
	@echo "def index():" >> src/app.py
	@echo "    \"\"\"Serve the default page.\"\"\"" >> src/app.py
	@echo "    return '<span style=\"color:red\">Hello World3!</span>'" >> src/app.py
