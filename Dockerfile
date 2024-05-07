################### WEB BUILD #########################

FROM node:22-bookworm-slim AS web-build

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt install -y patch \
    && apt -y upgrade \
    && apt -y clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY --chown=appuser empi-web ./
COPY --chown=appuser docker/patches/svelte.config.js.patch ./
RUN patch svelte.config.js svelte.config.js.patch

RUN npm ci
RUN npm audit fix
RUN npm run build

FROM python:3.12-slim-bookworm AS api

ARG POETRY_INSTALL_ARGS=""

WORKDIR /app
RUN useradd -ms /bin/bash appuser

ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1
ENV PATH=/home/appuser/.local/bin:$PATH

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt install -y caddy xz-utils libmagic1 patch \
    && apt -y upgrade \
    && apt -y clean \
    && rm -rf /var/lib/apt/lists/*

ARG S6_OVERLAY_VERSION=3.1.6.2
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz
COPY docker/s6 /etc/s6-overlay/s6-rc.d
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

WORKDIR /app/empi-server
COPY --chown=appuser docker/patches/settings.py.patch ./
RUN patch empi_server/settings.py settings.py.patch

RUN poetry run python manage.py collectstatic --no-input

CMD ["/init"]

FROM node:22-bookworm-slim AS web

RUN mkdir /app
RUN useradd -ms /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser
RUN mkdir /app/empi-web

WORKDIR /app/empi-web

COPY --from=web-build --chown=appuser /build/package*.json ./

RUN npm ci --production --ignore-scripts
RUN npm audit fix

COPY --from=web-build --chown=appuser /build/build ./
ARG ORIGIN
ENV ORIGIN ${ORIGIN}
CMD ["node", "-r", "dotenv/config", "."]