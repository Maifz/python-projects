FROM python:3.8-alpine


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
	&& pip install ${PIP_RUN_DEPS}


###
### Copy src and config
###
COPY --chown=1000:1000 config /home/${USER}/config
COPY --chown=1000:1000 src /home/${USER}/src


###
### Start
###
EXPOSE 8080
WORKDIR /home/${USER}/src
USER ${USER}
CMD ["uwsgi", "--ini", "/home/flagodo/config/uwsgi.ini"]
