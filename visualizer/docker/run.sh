#!/usr/bin/env bash
# Auto-detects WSL vs Jetson/native Linux, starts the right service, opens a shell in it.
# Usage: ./run.sh          (GPU/display profile for this machine)
#        ./run.sh web      (browser desktop at http://localhost:6080/vnc.html)
set -e
cd "$(dirname "$0")"

if docker compose version >/dev/null 2>&1; then DC="docker compose"; else DC="docker-compose"; fi

if [ -n "$1" ]; then
  PROFILE="$1"
elif grep -qi microsoft /proc/version 2>/dev/null; then
  PROFILE=wsl
else
  PROFILE=native
fi
SERVICE="robotics-$PROFILE"

export DISPLAY="${DISPLAY:-:0}"
echo "Profile: $PROFILE | DISPLAY=$DISPLAY"

# Native Linux/Jetson X server blocks root-in-container by default; WSLg doesn't.
if [ "$PROFILE" = "native" ]; then
  xhost +SI:localuser:root || echo "WARNING: xhost failed - GUI apps (rviz2, rqt_graph) may not open"
fi

$DC --profile "$PROFILE" up -d --build "$SERVICE"

if [ "$PROFILE" = "web" ]; then
  echo "Open http://localhost:6080/vnc.html"
else
  $DC --profile "$PROFILE" exec "$SERVICE" bash
fi