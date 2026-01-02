################### WEB BUILD #########################

FROM node:25-alpine AS web-build

ARG EMPI_INT_API_ENDPOINT
ENV EMPI_INT_API_ENDPOINT=$EMPI_INT_API_ENDPOINT
ARG EMPI_EXT_API_ENDPOINT
ENV EMPI_EXT_API_ENDPOINT=$EMPI_EXT_API_ENDPOINT
ARG ORIGIN
ENV ORIGIN=$ORIGIN

WORKDIR /build

COPY empi-web ./

RUN npm ci
RUN npm run build

FROM python:3.14-slim-trixie AS api

ARG POETRY_INSTALL_ARGS=""

WORKDIR /app
RUN useradd -ms /bin/bash appuser

ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1
ENV PATH=/home/appuser/.local/bin:$PATH
ENV EMPI_DOCKER 1

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y caddy xz-utils libmagic1 \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

ARG MULTIRUN_VERSION=1.1.3
ADD https://github.com/nicolas-van/multirun/releases/download/${MULTIRUN_VERSION}/multirun-x86_64-linux-gnu-${MULTIRUN_VERSION}.tar.gz /tmp
RUN tar -xf /tmp/multirun-x86_64-linux-gnu-${MULTIRUN_VERSION}.tar.gz \
    && mv multirun /bin \
    && rm /tmp/*

COPY docker/start.sh /app/start.sh
COPY docker/Caddyfile /app/Caddyfile

RUN chown -R appuser:appuser /app
USER appuser
RUN mkdir -p /app/empi-server

RUN pip install --upgrade poetry
COPY --chown=appuser pyproject.toml poetry.lock ./
RUN touch README.md
RUN poetry install ${POETRY_INSTALL_ARGS} --no-root

COPY --chown=appuser empi-server ./empi-server
RUN poetry install ${POETRY_INSTALL_ARGS}

RUN poetry run ./empi-server/manage.py collectstatic --no-input

CMD ["/bin/multirun", "caddy run --adapter caddyfile --config /app/Caddyfile", "/app/start.sh"]

FROM node:25-alpine AS web

ARG ORIGIN
ENV ORIGIN=$ORIGIN

RUN mkdir /app
RUN mkdir /app/empi-web

WORKDIR /app/empi-web

COPY --from=web-build /build/package*.json ./

RUN npm ci --production --ignore-scripts

COPY --from=web-build --chown=appuser /build/build ./

CMD ["node", "."]
