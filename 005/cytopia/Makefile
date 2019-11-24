API_IMAGE = cytopia/flagodo
API_DIR   = api
API_FILE  = Dockerfile

WEB_IMAGE = cytopia/web
WEB_DIR   = web
WEB_FILE  = Dockerfile



help:
	@echo "help"


build-api:
	docker build -t $(API_IMAGE) -f $(API_DIR)/$(API_FILE) $(API_DIR)

build-web:
	docker build -t $(WEB_IMAGE) -f $(WEB_DIR)/$(WEB_FILE) $(WEB_DIR)

start:
	docker-compose up -d

stop:
	docker-compose down
