
FROM python:3.10.13-alpine3.17

RUN apk --update --no-cache upgrade
RUN apk add build-base libressl libffi-dev libressl-dev libxslt-dev libxml2-dev xmlsec-dev xmlsec

RUN adduser -D monetization_user -h /data
WORKDIR /data
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/data"
COPY --chown=monetization_user:monetization_user ./requirements.dev.txt ./
RUN  pip install --upgrade pip \
     && pip install -r requirements.dev.txt
COPY --chown=monetization_user:monetization_user ./src/monetization_service/ ./src/monetization_service
COPY --chown=monetization_user:monetization_user ./src/common/ ./src/common
EXPOSE 8000/tcp
USER monetization_user
CMD alembic -c src/monetization_service/alembic.ini upgrade head;gunicorn -c src/monetization_service/gunicorn.conf.py src.monetization_service.app:app -k uvicorn.workers.UvicornWorker
