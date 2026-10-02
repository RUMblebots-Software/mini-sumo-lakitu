#!/usr/bin/env bash
set -e

export DISPLAY="${DISPLAY:-:0}"
export XDG_RUNTIME_DIR=/tmp/runtime-root

mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"

Xvfb "$DISPLAY" -screen 0 1280x800x24 +extension GLX +render -noreset &

until xdpyinfo -display "$DISPLAY" >/dev/null 2>&1; do
  sleep 0.2
done

dbus-launch --exit-with-session startxfce4 &

x11vnc \
  -display "$DISPLAY" \
  -nopw \
  -listen localhost \
  -xkb \
  -forever \
  -shared \
  -rfbport 5900 &

exec websockify --web /usr/share/novnc 6080 localhost:5900