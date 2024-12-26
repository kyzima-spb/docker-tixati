ARG RELEASE="bookworm-slim"

FROM kyzimaspb/gui:$RELEASE

LABEL maintainer="Kirill Vercetti <office@kyzima-spb.com>"

WORKDIR /tixati

COPY --from=kyzimaspb/useful /apps/compver/compver.sh /usr/local/bin/

ARG TIXATI_DOWNLOAD_URL="https://download.tixati.com"
ARG TIXATI_VERSION="3.31"

ENV TIXATI_VERSION=${TIXATI_VERSION}

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    --mount=type=secret,id=mirrorurl,target=/root/.mirrorurl \
    set -ex; \
        rm -f /etc/apt/apt.conf.d/docker-clean; \
        echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache; \
        \
        savedAptMark="$(apt-mark showmanual)"; \
        apt update; \
        apt install -yq --no-install-recommends \
            ca-certificates \
            wget \
        ; \
        \
        downloadUrl="${TIXATI_DOWNLOAD_URL}"; \
        test -f /root/.mirrorurl && downloadUrl="$(cat /root/.mirrorurl)" || true; \
        compver.sh "${TIXATI_VERSION} < 3.31" && downloadUrl='https://download2.tixati.com/download' || true; \
        wget -q --progress=dot -O tixati.deb ${downloadUrl}/tixati_${TIXATI_VERSION}-1_amd64.deb; \
        apt-mark auto '.*' > /dev/null; \
	    apt-mark manual $savedAptMark; \
        apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
        \
        apt install -yq --no-install-recommends \
            dbus \
            ./tixati.deb \
        ; \
        rm tixati.deb; \
        \
        cd /tixati; \
        homeDIR="$(getent passwd user | cut -d: -f6)"; \
        tixatiConfigDir="$(compver.sh "${TIXATI_VERSION} < 2.87" && echo '.tixati' || echo '.config/tixati')"; \
        ln -s "$homeDIR/$tixatiConfigDir" ./config; \
        for p in Desktop/downloads Desktop/torrent-files; do \
            mkdir -p "$homeDIR/$p"; \
            ln -s "$homeDIR/$p" "./$(basename $p)"; \
        done; \
        chown -R user:user "$homeDIR"


VOLUME /tixati/config /tixati/downloads

COPY ./ /
