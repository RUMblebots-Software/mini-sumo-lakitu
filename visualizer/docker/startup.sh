#!/bin/bash
# Start the virtual display (monitor)
Xvfb :0 -screen 0 1280x800x24 &
export DISPLAY=:0

# Give Xvfb time to initialize
sleep 2

# Start the XFCE visual desktop
startxfce4 &

# Start the VNC server to capture the virtual display
x11vnc -display :0 -nopw -listen localhost -xkb -forever &

# Start noVNC to bridge the VNC stream to a web browser
websockify --web /usr/share/novnc/ 6080 localhost:5900