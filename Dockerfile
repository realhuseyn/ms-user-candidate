FROM python:3.9-alpine as base

ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev make && \
    pip install poetry

ENV APP_HOME=/usr/src/app
ENV APP_USER=appuser

RUN adduser -D ${APP_USER}

WORKDIR $APP_HOME

ENV TZ 'Asia/Baku'
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

FROM base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . $APP_HOME
RUN pip install --upgrade pip \
    && python -m venv .venv \
    && source .venv/bin/activate && \
    poetry install \
    && chown -R $APP_USER:$APP_USER $APP_HOME

USER $APP_USER
EXPOSE 8000

CMD /bin/sh start.sh