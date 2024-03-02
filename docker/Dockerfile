ARG RELEASE="bookworm-slim"

FROM kyzimaspb/gui:$RELEASE

LABEL maintainer="Kirill Vercetti <office@kyzima-spb.com>"

USER root

ARG TIXATI_DOWNLOAD_URL="https://download2.tixati.com/download"
ARG TIXATI_VERSION="3.22"
ADD ${TIXATI_DOWNLOAD_URL}/tixati_${TIXATI_VERSION}-1_amd64.deb /tmp

RUN set -x \
    && apt update \
    && apt install -yq \
        dbus \
        libgtk-3-0 \
        /tmp/tixati_*-1_amd64.deb \
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
