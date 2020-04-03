## Attention

This crazy idea to run GUI applications in the Docker container, but unfortunately I did not find another way to run Tixati on the server. Use this image only on servers without a desktop environment. If your server has a DE, use the installer from the official site.


## Volumes

### `/home/tixati/Desktop/downloads`
Directory with downloaded files.

### `/home/tixati/Desktop/torrent-files`
Directory with torrent files.


## Run in daemon mode

Run the container named tixati_1 in daemon mode and mount the specified volumes to the specified directories of the host machine:

```bash
docker run -d --name tixati_1 -p 5900:5900 -p 29939:29939 -v $(pwd)/downloads:/home/tixati/Desktop/downloads -v $(pwd)/torrent-files:/home/tixati/Desktop/torrent-files kyzimaspb/tixati
```

Forwarded ports:
* `5900` - TCP port for connecting VNC clients;
* `29939` - TCP/UDP port for peer connections and messages (see the configuration of your Tixati or remember to change after run).


## Environment Variables

### `ATTEMPTS_COUNT`
The number of attempts to start each service.

### `DISPLAY`
### `XVFB_SCREEN`

### `XVFB_RESOLUTION`
Screen resolution of the virtual X server.

### `VNC_SERVER_PASSWORD`
The password for the VNC server.
