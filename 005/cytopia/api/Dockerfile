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
	&& addgroup -g ${GID} flagodo \
	&& adduser -h /home/flagodo -G flagodo -D -u ${UID} flagodo

###
### Project dependencies
###
COPY --chown=${UID}:${GID} requirements.txt /home/flagodo/requirements.txt
RUN set -x \
	&& mkdir -p /home/flagodo/flagodo \
	&& mkdir -p /home/flagodo/flagodo \
	&& cd /home/flagodo/flagodo/ \
	&& virtualenv venv \
	&& source /home/flagodo/flagodo/venv/bin/activate \
	&& pip install -r ../requirements.txt

###
### Copy src and config
###
COPY --chown=${UID}:${GID} config /home/flagodo/config
#COPY --chown=${UID}:${GID} src /home/flagodo/src

###
### Start
###
EXPOSE 8080
WORKDIR /home/flagodo/flagodo
USER flagodo
CMD ["uwsgi", "--ini", "/home/flagodo/config/uwsgi.ini", "--py-autoreload", "1"]

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
	&& addgroup -g ${GID} flagodo \
	&& adduser -h /home/flagodo -G flagodo -D -u ${UID} flagodo

###
### Project dependencies
###
COPY --chown=${UID}:${GID} requirements.txt /home/flagodo/requirements.txt
RUN set -x \
	&& mkdir -p /home/flagodo/flagodo \
	&& mkdir -p /home/flagodo/flagodo \
	&& cd /home/flagodo/flagodo/ \
	&& virtualenv venv \
	&& source /home/flagodo/flagodo/venv/bin/activate \
	&& pip install -r ../requirements.txt

###
### Copy src and config
###
COPY --chown=${UID}:${GID} config /home/flagodo/config
COPY --chown=${UID}:${GID} src /home/flagodo/flagodo/src

###
### Start
###
EXPOSE 8080
WORKDIR /home/flagodo/flagodo
USER flagodo
CMD ["uwsgi", "--ini", "/home/flagodo/config/uwsgi.ini"]
