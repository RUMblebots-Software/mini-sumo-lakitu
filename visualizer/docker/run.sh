#!/usr/bin/env bash
# Auto-detects WSL vs Jetson/native Linux, starts the right service, opens a shell in it.
# Usage: bash run.sh      (native CPU rendering or WSLg, detected automatically)
#        ./run.sh web      (browser desktop at http://localhost:6080/vnc.html)
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

if docker compose version >/dev/null 2>&1; then DC=(docker compose); else DC=(docker-compose); fi

if [ -n "${1:-}" ]; then
  PROFILE="$1"
elif grep -qi microsoft /proc/version 2>/dev/null; then
  PROFILE=wsl
else
  PROFILE=native
fi
case "$PROFILE" in
  native|wsl|web) ;;
  *) echo "Usage: bash run.sh [native|wsl|web]" >&2; exit 1 ;;
esac
SERVICE="robotics-$PROFILE"

if [[ "$PROFILE" == "native" && -z "${DISPLAY:-}" ]]; then
  echo "DISPLAY is unset. Run this script from a terminal on the Jetson/native desktop." >&2
  exit 1
fi

export DISPLAY="${DISPLAY:-:0}"
echo "Profile: $PROFILE | DISPLAY=$DISPLAY"

# Native Linux/Jetson X server blocks root-in-container by default; WSLg doesn't.
if [ "$PROFILE" = "native" ]; then
  # Authorization belongs to the host desktop session, not the image.
  xhost +si:localuser:root
fi

"${DC[@]}" --profile "$PROFILE" up -d --build "$SERVICE"

if [ "$PROFILE" = "web" ]; then
  echo "Open http://localhost:6080/vnc.html"
elif [ "$PROFILE" = "native" ]; then
  exec "${DC[@]}" --profile "$PROFILE" exec "$SERVICE" bash -lc '
    set -e
    mkdir -p "$XDG_RUNTIME_DIR"
    chmod 700 "$XDG_RUNTIME_DIR"
    source /opt/ros/humble/setup.bash
    if [ -f /root/Documents/ros2_ws/install/setup.bash ]; then
      source /root/Documents/ros2_ws/install/setup.bash
    fi
    exec bash -i
  '
else
  exec "${DC[@]}" --profile "$PROFILE" exec "$SERVICE" bash
fi
