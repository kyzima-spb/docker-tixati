#!/bin/bash

export DISPLAY=${XVFB_DISPLAY:-:99}

ATTEMPTS_COUNT=${ATTEMPTS_COUNT:-3}


main()
{
    start_xvfb
    start_wm
    tixati %U &
    start_vnc_server
}


start_xvfb()
{
    local screen=${XVFB_SCREEN:-0}
    local resolution=${XVFB_RESOLUTION:-1280x720x24}
    local attempts=$ATTEMPTS_COUNT

    echo -n "Starting virtual X frame buffer: Xvfb "

    /usr/bin/Xvfb $DISPLAY -screen $screen $resolution -ac -noreset -nolisten tcp &
    XVFB_PID=$!

    while [ ! -e /tmp/.X11-unix/X99 ] # xset q
    do
        echo -n "."

        ((attempts--))
        sleep 0.3

        if [ $attempts -le 0 ]
        then
            echo "[FAIL]"
            exit 1
        fi
    done

    echo " [OK]"
}


stop_xvfb()
{
    echo -n "Stoppping virtual X frame buffer: Xvfb "
    kill -SIGTERM $XVFB_PID
    echo "[OK]"
}


start_wm()
{
    local attempts=$ATTEMPTS_COUNT

    echo -n "Starting window manager: openbox "

    /usr/bin/openbox-session 2>/dev/null &
    WM_PID=$!

    while [ -z "$(wmctrl -m 2>/dev/null)" ]
    do
        echo -n "."

        ((attempts--))
        sleep 0.3

        if [ $attempts -le 0 ]
        then
            echo "[FAIL]"
            exit 1
        fi
    done
    
    echo " [OK]"
}


stop_wm()
{
    echo -n "Stoppping window manager: openbox "
    kill -SIGTERM $WM_PID
    echo "[OK]"
}


start_vnc_server()
{
    local password=${VNC_SERVER_PASSWORD}
    local password_arg="-nopw"
    local password_file="${HOME}/x11vnc.pswd"

    if [ -z $password ]
    then
        echo -n "Starting VNC server without password: "
    else
        echo -n "Starting VNC server: "

        password_arg="-rfbauth ${password_file}"

        if ! x11vnc -storepasswd "${password}" "${password_file}"
        then
            echo "[FAIL]"
            echo "Failed to store x11vnc password."
            exit 1
        fi
    fi

    x11vnc -q -display $DISPLAY $password_arg -forever -listen 0.0.0.0 -xkb -many 2>/dev/null
    echo "[OK]"
}


control_c()
{
    stop_wm
    stop_xvfb
    exit 0
}


trap control_c SIGINT SIGTERM SIGHUP

main
