#!/bin/bash

xset s off
xset s off -dpms
chromium http://localhost:8000 --kiosk --start-fullscreen --start-maximized --host-rules="MAP * localhost:8000" --enable-offline-auto-reload
