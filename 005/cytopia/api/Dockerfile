FROM python:3.8-alpine as develop


###
### Environment
###
ENV USER=flagodo
ENV GROUP=flagodo
ENV PIP_RUN_DEPS \
	flask


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
### User
###
RUN set -x \
	&& addgroup -g 1000 ${GROUP} \
	&& adduser -h /home/${USER} -G ${GROUP} -D -u 1000 ${USER}

###
### Project dependencies
###
RUN set -x \
	&& mkdir -p /home/${USER}/flagodo \
	&& mkdir -p /home/${USER}/flagodo \
	&& cd /home/${USER}/flagodo/ \
	&& virtualenv venv \
	&& source /home/${USER}/flagodo/venv/bin/activate \
	&& pip install ${PIP_RUN_DEPS}

RUN set -x \
	&& mkdir -p /var/log/uwsgi/ \
	&& touch /var/log/uwsgi/flagodo.log \
	&& chown -R flagodo:flagodo /var/log/uwsgi


###
### Copy src and config
###
COPY --chown=1000:1000 config /home/${USER}/config
#COPY --chown=1000:1000 src /home/${USER}/src


###
### Start
###
EXPOSE 8080
WORKDIR /home/${USER}/flagodo
USER ${USER}
CMD ["uwsgi", "--ini", "/home/flagodo/config/uwsgi.ini", "--py-autoreload", "1"]
