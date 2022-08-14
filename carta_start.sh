#!/usr/bin/bash

trap "exit" INT TERM ERR
trap "kill 0" EXIT
# job handling from https://spin.atomicobject.com/2017/08/24/start-stop-bash-background-process/

squeue -u joarlewi | grep carta

APPIMAGE_EXTRACT_AND_RUN=1
export APPIMAGE_EXTRACT_AND_RUN
$HOME/CARTA-v2.0-redhat.AppImage --no_browser --exit_timeout 120 --initial_timeout 120 --idle_timeout 1200 # >/dev/null 2>&1 &

sleep 2s

# get line of interest
# get last entry
# put new line in front of http
# get lines beginning with http
# get the line upto a space
# keep only unique lines
grep "CARTA is accessible at" $HOME/.carta/log/carta.log | tail -1 | sed 's/http/\nhttp/g' | grep ^http | sed 's/\(^http[^ <]*\)\(.*\)/\1/g' | sort -u
# grep "joarlewi" carta.log | grep "carta"

wait