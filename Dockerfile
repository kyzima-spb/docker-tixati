FROM kyzimaspb/gui

LABEL maintainer="Kirill Vercetti <office@kyzima-spb.com>"

ARG TIXATI_VERSION=2.89

USER root

ADD https://download2.tixati.com/download/tixati_${TIXATI_VERSION}-1_amd64.deb /tmp

RUN set -x \
    && apt update \
    && dpkg -i /tmp/tixati_${TIXATI_VERSION}-1_amd64.deb || true \
    && apt install -yqf --no-install-recommends \
    && rm /tmp/tixati_${TIXATI_VERSION}-1_amd64.deb \
    && apt-get clean  \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./root /

USER user

RUN set -x \
    && /bin/bash -c 'mkdir -p /home/user/{.tixati,Desktop/{downloads,torrent-files}}'

VOLUME /home/user/.tixati /home/user/Desktop/downloads /home/user/Desktop/torrent-files
