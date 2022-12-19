## Attention

This crazy idea to run GUI applications in the Docker container, but unfortunately I did not find another way to run Tixati on the server. Use this image only on servers without a desktop environment. If your server has a DE, use the installer from the official site.


### Volumes

* `/home/tixati/Desktop/downloads` - directory with downloaded files;
* `/home/tixati/Desktop/torrent-files` - directory with torrent files;
* `/home/tixati/.tixati` - directory with tixati profile.

### Environment Variables

* `XVFB_RESOLUTION` - screen resolution of the virtual X server;
* `VNC_SERVER_PASSWORD` - the password for the VNC server.

### Forwarded ports:
* `5900` - TCP port for connecting VNC clients.


## Run in daemon mode

Run the container named tixati_1 in daemon mode and mount the specified volumes to the specified directories of the host machine:

```bash
$ docker run -d --name tixati_1 \
      --network host \
      -v $(pwd)/downloads:/home/tixati/Desktop/downloads \
      -v $(pwd)/torrent-files:/home/tixati/Desktop/torrent-files \
      kyzimaspb/tixati
```


## Autostart with a password

Automatically start the container at system startup with the password `qwe123` to connect to the VNC server:

```bash
$ docker run -d --name tixati_1 \
      --network host \
      --restart unless-stopped \
      -e VNC_SERVER_PASSWORD=qwe123 \
      -v $(pwd)/downloads:/home/tixati/Desktop/downloads \
      -v $(pwd)/torrent-files:/home/tixati/Desktop/torrent-files \
      kyzimaspb/tixati
```


## Resource limits

You can use all resource limits available for the `docker run` command. For example, limit the amount of RAM:

```bash
$ docker run -d --name tixati_1 \
      --network host \
      --restart unless-stopped \
      -m 512M \
      -e VNC_SERVER_PASSWORD=qwe123 \
      -v $(pwd)/downloads:/home/tixati/Desktop/downloads \
      -v $(pwd)/torrent-files:/home/tixati/Desktop/torrent-files \
      kyzimaspb/tixati
```


## How to change Tixati version?

The `TIXATI_VERSION` build argument allows you to specify the version of Tixati:

```bash
$ git clone https://github.com/kyzima-spb/docker-tixati.git
$ cd docker-tixati
$ docker build -t tixati --build-arg TIXATI_VERSION=3.11 .
```


## How to change distribution release?

The `RELEASE` build argument allows you to specify the release of the Debian distribution.
Available values: `bullseye-slim` (default), `bullseye`, `buster-slim`, `buster`,
`stretch-slim`, `stretch`:

```bash
$ git clone https://github.com/kyzima-spb/docker-tixati.git
$ cd docker-tixati
$ docker build -t tixati --build-arg RELEASE=stretch-slim .
```

## How to change UID/GID?

We clone the sources of the base image and build it with the values of the identifiers.
The image name must be in the format `kyzimaspb/<RELEASE>`:

```bash
$ git clone https://github.com/kyzima-spb/docker-gui.git
$ cd docker-gui
$ docker build -t kyzimaspb/buster-slim \
      --build-arg RELEASE=buster-slim \
      --build-arg UID=1001 \
      --build-arg GID=1001 \
      .
```

We clone the image sources from Tixati and build with the release name used when building the base image (the image will not be downloaded from Docker Hub, because it exists locally):

```bash
$ git clone https://github.com/kyzima-spb/docker-tixati.git
$ cd docker-tixati
$ docker build -t tixati --build-arg RELEASE=buster-slim .
```
