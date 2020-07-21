FROM debian:buster-slim

LABEL maintainer="Kirill Vercetti <office@kyzima-spb.com>"

ENV DEBIAN_FRONTEND noninteractive

ARG UID=1000
ARG GID=1000
ARG TIXATI_VERSION=2.74

RUN apt update

RUN set -x \
    && apt install -yq --no-install-recommends wget \
    && \
    download_url="https://download2.tixati.com/download/tixati_${TIXATI_VERSION}-1_amd64.deb"; \
    echo "Checking for package existence..."; \
    wget -q --no-check-certificate --method=HEAD $download_url || { \
        echo "Version ${TIXATI_VERSION} of the package was not found."; \
        exit 1; \
    } \
    && wget --no-check-certificate -qO /tmp/tixati.deb $download_url \
    && dpkg -i /tmp/tixati.deb || true \
    && apt install -yqf --no-install-recommends \
    && apt install -yq --no-install-recommends wmctrl openbox xvfb x11vnc locales \
    && rm /tmp/tixati.deb \
    && apt-get clean  \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /tmp/.X11-unix \
    && chmod 1777 /tmp/.X11-unix

RUN groupadd -g $GID tixati \
    && useradd -u $UID -g $GID -s /bin/bash -m tixati \
    && /bin/bash -c 'mkdir -p /home/tixati/{.tixati,Desktop/{downloads,torrent-files}}' \
    && chown -R tixati:tixati /home/tixati

COPY ./menu.xml /var/lib/openbox/debian-menu.xml
COPY ./entrypoint.sh /entrypoint.sh

USER tixati

VOLUME /home/tixati/.tixati /home/tixati/Desktop/downloads /home/tixati/Desktop/torrent-files

STOPSIGNAL SIGTERM

ENTRYPOINT "/entrypoint.sh"

