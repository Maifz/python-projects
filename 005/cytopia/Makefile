API_IMAGE = cytopia/flagodo
API_DIR   = api
API_FILE  = Dockerfile

WEB_IMAGE = cytopia/web
WEB_DIR   = web
WEB_FILE  = Dockerfile



help:
	@echo "help"

build: build-api build-web

build-api:
	docker build -t $(API_IMAGE) -f $(API_DIR)/$(API_FILE) $(API_DIR)

build-web:
	docker build -t $(WEB_IMAGE) -f $(WEB_DIR)/$(WEB_FILE) $(WEB_DIR)

run-api:
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		--name flagodo-api \
		-v $(PWD)/api/src:/home/flagodo/flagodo/src \
		-p "8090:8080" $(API_IMAGE) $(ARGS)
exec-api:
	docker exec -it --user root flagodo-api sh

start:
	docker-compose up -d

stop:
	docker-compose down
