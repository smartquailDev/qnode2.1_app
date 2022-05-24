FROM python:3.9-alpine3.13
LABEL maintainer="smartquail.io"

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache git
ARG username=smartquailDev
ARG password=ms1719183830
RUN git clone https://github.com/smartquailDev/qnode2.1_app.git

#COPY . /qnode0_app
#COPY ./qnode0_app.dev/qnode0_app_env_dev/qnode0_app/ /qnode0_app
COPY ./requirements.txt /requirements.txt
COPY ./scripts /scripts
COPY ./uwsgi_prod.ini /qnode2.1_app/qnode21_app/uwsgi_prod.ini

#COPY ./.env /qnode0.1_app/qnode01_app/.env 
#No olvidar sacar las variables de entorno.


WORKDIR /qnode2.1_app/qnode21_app/
EXPOSE 443 
EXPOSE 25
EXPOSE 9000
EXPOSE 587

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps && \
    apk add build-base  postgresql-dev gcc musl-dev python3-dev linux-headers && \
    apk add libffi-dev build-base py3-cffi py3-cryptography && \
    apk add jpeg-dev   zlib-dev libjpeg build-base  wget  && \
    apk --update --upgrade --no-cache add fontconfig ttf-freefont font-noto terminus-font && \
    apk add gtk+3.0 pango && \
    apk del libressl-dev && \
    apk add busybox-extras && \
    apk add openssl-dev && \
    #/py/bin/pip install  rust  &&  \
    #/py/bin/pip install   py3-kiwisolver &&  \
    /py/bin/pip install -r /requirements.txt && \
    apk del openssl-dev  &&  \
    apk add libressl-dev  && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home qnode21 && \

    #Static Files
    mkdir -p /qnode2.1_app/qnode21_app/static && \
   # mkdir -p /qnode0.0_app/qnode0_app/static/media && \
    chmod -R 755 /qnode2.1_app/qnode21_app/static  && \

    mkdir -p /qnode2.1_app/qnode21_app/media && \
    chmod -R 755 /qnode2.1_app/qnode21_app/media  && \
    chown -R qnode21:qnode21 /qnode2.1_app/qnode21_app/media && \
    
    mkdir -p /qnode2.1_app/qnode21_app/staticfiles && \
    chmod -R 755 /qnode2.1_app/qnode21_app/staticfiles  && \
    chown -R qnode21:qnode21 /qnode2.1_app/qnode21_app/staticfiles && \

    #chmod -R 755 /qnode0.0_app/qnode0_app/static/media  && \
    chown -R qnode21:qnode21 /qnode2.1_app/qnode21_app/static && \
    #chown -R qnode0:qnode0 /qnode0.0_app/qnode0_app/static/media && \
    #Uswgi
    
    mkdir -p  /var/log/uwsgi/ && \
    chown -R qnode21:qnode21 /var/log/uwsgi/ && \
    #GNUCORN
    mkdir -p /qnode2.1_app/qnode21_app/run/ && \
    mkdir -p /var/log/gunicorn &&\
    chown -R qnode21:qnode21 /var/log/gunicorn &&\
    
    chmod -R 755 /qnode2.1_app/qnode21_app/ && \
    
    chmod -R 755 /scripts  && \
    chown -R qnode21:qnode21 /qnode2.1_app/qnode21_app/run/  && \
    chown -R qnode21:qnode21 /qnode2.1_app/qnode21_app/ &&\
    chmod -R 755 /var/log/gunicorn  && \
    
    #chmod -R u+x /scripts/gunicorn_run.sh &&\
    chmod -R u+x /scripts/run.sh &&\
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"
#COPY ./scripts/gunicorn.socket /qnode0.0_app/qnode0_app/run/

USER qnode21

CMD ["run.sh"]


