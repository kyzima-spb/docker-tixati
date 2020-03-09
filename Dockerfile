FROM debian:buster-slim

LABEL maintainer="Kirill Vercetti <office@kyzima-spb.com>"

ARG UID=1000
ARG GID=1000

VOLUME /root/.tixati

VOLUME /srv/tixati/downloads
VOLUME /srv/tixati/incomplete-pieces
VOLUME /srv/tixati/torrent-files

ENV DEBIAN_FRONTEND noninteractive

RUN groupadd -g $GID tixati \
    && useradd -u $UID -g $GID -s /bin/bash -m tixati

RUN apt update

RUN apt install -yq --no-install-recommends wget \
    && wget --no-check-certificate -qO /tmp/tixati.deb "https://download2.tixati.com/download/tixati_2.67-1_amd64.deb" \
    && dpkg -i /tmp/tixati.deb || true \
    && apt install -yqf --no-install-recommends \
    && apt install -yq --no-install-recommends wmctrl openbox xvfb x11vnc thunar locales xterm \
    && rm /tmp/tixati.deb \
    && apt-get clean  \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./menu.xml /var/lib/openbox/debian-menu.xml
COPY ./bookmarks /home/tixati/.config/gtk-3.0/bookmarks

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

USER tixati

ENTRYPOINT "/entrypoint.sh"

