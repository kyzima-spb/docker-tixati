## Attention

This crazy idea to run GUI applications in the Docker container, but unfortunately I did not find another way to run Tixati on the server. Use this image only on servers without a desktop environment. If your server has a DE, use the installer from the official site.


## Volumes

* `/home/tixati/Desktop/downloads` - directory with downloaded files;
* `/home/tixati/Desktop/torrent-files` - directory with torrent files;
* `/home/tixati/.tixati` - directory with tixati profile.


## Run in daemon mode

Run the container named tixati_1 in daemon mode and mount the specified volumes to the specified directories of the host machine:

```bash
docker run -d --name tixati_1 \
    -p 5900:5900 \
    -p 29939:29939 \
    -v $(pwd)/downloads:/home/tixati/Desktop/downloads \
    -v $(pwd)/torrent-files:/home/tixati/Desktop/torrent-files kyzimaspb/tixati
```

Forwarded ports:
* `5900` - TCP port for connecting VNC clients;
* `29939` - TCP/UDP port for peer connections and messages (see the configuration of your Tixati or remember to change after run).


## Environment Variables

* `ATTEMPTS_COUNT` - the number of attempts to start each service;
* `XVFB_RESOLUTION` - screen resolution of the virtual X server;
* `VNC_SERVER_PASSWORD` - the password for the VNC server.


## Autostart with a password

Automatically start the container at system startup with the password `qwe123` to connect to the VNC server:

```bash
docker run -d --name tixati_1 --restart always \
    -p 5900:5900 \
    -p 29939:29939 \
    -e VNC_SERVER_PASSWORD=qwe123 \
    -v $(pwd)/downloads:/home/tixati/Desktop/downloads \
    -v $(pwd)/torrent-files:/home/tixati/Desktop/torrent-files kyzimaspb/tixati
```


## Resource limits

You can use all resource limits available for the `docker run` command. For example, limit the amount of RAM:

```bash
docker run -d --name tixati_1 --restart always \
    -m 512M \
    -p 5900:5900 \
    -p 29939:29939 \
    -e VNC_SERVER_PASSWORD=qwe123 \
    -v $(pwd)/downloads:/home/tixati/Desktop/downloads \
    -v $(pwd)/torrent-files:/home/tixati/Desktop/torrent-files kyzimaspb/tixati
```
