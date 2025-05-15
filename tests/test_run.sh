#!/usr/bin/env bash
set -e


close_update_dialog() {
    local wnd
    wnd="$(find_window "$1")"

    if [[ -n "$wnd" ]]; then
        xdotool windowactivate --sync "$wnd"
        xdotool key ISO_Left_Tab Return
    fi
}


find_window() {
    local title

    xdotool search --onlyvisible --name "" | while read -r wnd; do
        title="$(xdotool getwindowname "$wnd")"
        if [ "$title" = "$1" ]; then
            echo "$wnd"
        fi
    done
}


setup() {
    if ! command -v xdotool > /dev/null; then
        apt-get update && apt-get install -y xdotool
    fi
}


test_confirm_licence() {
    local wnd
    wnd="$(find_window "$1")"

    [[ -z "$wnd" ]] && echo "Licence window not found." && return 1

    xdotool windowactivate --sync "$wnd"
    xdotool key Tab Return
}


test_initial_configuration() {
    local wnd
    wnd="$(find_window "$1")"

    [[ -z "$wnd" ]] && echo "Initial Configuration window not found." && return 1

    xdotool windowactivate --sync "$wnd"
    xdotool key ISO_Left_Tab Return
}


test_main_window() {
    local wnd
    wnd="$(find_window "$1")"

    [[ -z "$wnd" ]] && echo "Main window not found." && return 1
}


setup

test_confirm_licence 'Tixati'
sleep 0.1

test_initial_configuration 'Tixati Initial Configuration'
sleep 1

# close_update_dialog 'Update Available'
# sleep 0.1

test_main_window "Tixati v$TIXATI_VERSION"
