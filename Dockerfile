FROM debian:buster-slim

LABEL maintainer="Kirill Vercetti <office@kyzima-spb.com>"

ENV DEBIAN_FRONTEND noninteractive

ARG UID=1000
ARG GID=1000

RUN apt update

RUN apt install -yq --no-install-recommends wget \
    && wget --no-check-certificate -qO /tmp/tixati.deb "https://download2.tixati.com/download/tixati_2.67-1_amd64.deb" \
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
    && /bin/bash -c 'mkdir -p /home/tixati/{.tixati,Desktop/{downloads,torrent-files}}'

COPY ./menu.xml /var/lib/openbox/debian-menu.xml
COPY ./bookmarks /home/tixati/.config/gtk-3.0/bookmarks

RUN chown -R tixati:tixati /home/tixati

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER tixati

VOLUME /home/tixati/.tixati
VOLUME /home/tixati/Desktop/downloads
VOLUME /home/tixati/Desktop/torrent-files

ENTRYPOINT "/entrypoint.sh"

