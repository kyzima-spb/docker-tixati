ARG RELEASE=bullseye-slim

FROM kyzimaspb/gui:$RELEASE

LABEL maintainer="Kirill Vercetti <office@kyzima-spb.com>"

ARG TIXATI_DOWNLOAD_URL=https://download2.tixati.com/download
ARG TIXATI_VERSION=3.12

USER root

ADD ${TIXATI_DOWNLOAD_URL}/tixati_${TIXATI_VERSION}-1_amd64.deb /tmp

RUN set -x \
    && apt update \
    && apt install -yq \
        dbus \
        /tmp/tixati_${TIXATI_VERSION}-1_amd64.deb \
    && rm /tmp/tixati_${TIXATI_VERSION}-1_amd64.deb \
    && apt-get clean  \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./root /

USER user

RUN set -x \
    && /bin/bash -c 'mkdir -p /home/user/{.tixati,Desktop/{downloads,torrent-files}}' \
    && xmlstarlet edit -L \
      -N o="http://openbox.org/3.4/rc" \
      -s /o:openbox_config/o:applications -t elem -n applicationTMP -v "" \
      -i //applicationTMP -t attr -n "title" -v "Tixati v*" \
      -s //applicationTMP -t elem -n decor -v "no" \
      -s //applicationTMP -t elem -n fullscreen -v "yes" \
      -r //applicationTMP -v application \
          /home/user/.config/openbox/rc.xml

VOLUME /home/user/.tixati /home/user/Desktop/downloads /home/user/Desktop/torrent-files
