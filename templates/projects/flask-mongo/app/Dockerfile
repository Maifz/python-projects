###
### BUILDER
###
FROM python:3.8-alpine as builder

###
### General requirements
###
RUN set -x \
	&& apk add --no-cache \
		gcc \
		musl-dev \
		linux-headers

RUN set -x \
	&& pip install \
		virtualenv \
		uwsgi


###
### DEVELOPMENT
###
FROM python:3.8-alpine as development
COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=builder /usr/local/bin/virtualenv /usr/local/bin/virtualenv
COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/uwsgi

###
### Build args
###
ARG UID=1000
ARG GID=1000

###
### User
###
RUN set -x \
	&& addgroup -g ${GID} mygroup \
	&& adduser -h /home/myuser -G mygroup -D -u ${UID} myuser

###
### Switch to normal user
###
USER myuser

###
### Project dependencies
###
COPY --chown=${UID}:${GID} requirements.txt /home/myuser/requirements.txt
RUN set -x \
	&& mkdir -p /home/myuser/project \
	&& chown -R ${UID}:${GID} /home/myuser \
	&& cd /home/myuser/project/ \
	&& virtualenv venv \
	&& source /home/myuser/project/venv/bin/activate \
	&& pip install -r ../requirements.txt

###
### Copy src and config
###
COPY --chown=${UID}:${GID} config /home/myuser/config

###
### Start
###
EXPOSE 8080
WORKDIR /home/myuser/project
CMD ["uwsgi", "--ini", "/home/myuser/config/uwsgi.ini", "--py-autoreload", "1"]


###
### PRODUCTION
###
FROM python:3.8-alpine as production
COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=builder /usr/local/bin/virtualenv /usr/local/bin/virtualenv
COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/uwsgi

###
### Build args
###
ARG UID=1000
ARG GID=1000

###
### User
###
RUN set -x \
	&& addgroup -g ${GID} mygroup \
	&& adduser -h /home/myuser -G mygroup -D -u ${UID} myuser

###
### Switch to normal user
###
USER myuser

###
### Project dependencies
###
COPY --chown=${UID}:${GID} requirements.txt /home/myuser/requirements.txt
RUN set -x \
	&& mkdir -p /home/myuser/project \
	&& chown -R ${UID}:${GID} /home/myuser \
	&& cd /home/myuser/project/ \
	&& virtualenv venv \
	&& source /home/myuser/project/venv/bin/activate \
	&& pip install -r ../requirements.txt

###
### Copy src and config
###
COPY --chown=${UID}:${GID} config /home/myuser/config
COPY --chown=${UID}:${GID} src /home/myuser/project/src

###
### Start
###
EXPOSE 8080
WORKDIR /home/myuser/project
CMD ["uwsgi", "--ini", "/home/myuser/config/uwsgi.ini"]
