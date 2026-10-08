#!/usr/bin/env bash
# Auto-detects WSL vs Jetson/native Linux, starts the right service, opens a shell in it.
# Usage: bash run.sh      (native CPU rendering or WSLg, detected automatically)
#        bash run.sh jetson-gpu (experimental Jetson Nano GPU profile)
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
  native|jetson-gpu|wsl|web) ;;
  *) echo "Usage: bash run.sh [native|jetson-gpu|wsl|web]" >&2; exit 1 ;;
esac
SERVICE="robotics-$PROFILE"

if [[ ( "$PROFILE" == "native" || "$PROFILE" == "jetson-gpu" ) && -z "${DISPLAY:-}" ]]; then
  echo "DISPLAY is unset. Run this script from a terminal on the Jetson/native desktop." >&2
  exit 1
fi

export DISPLAY="${DISPLAY:-:0}"
echo "Profile: $PROFILE | DISPLAY=$DISPLAY"

# Native Linux/Jetson X server blocks root-in-container by default; WSLg doesn't.
if [[ "$PROFILE" == "native" || "$PROFILE" == "jetson-gpu" ]]; then
  # Authorization belongs to the host desktop session, not the image.
  xhost +si:localuser:root
fi

"${DC[@]}" --profile "$PROFILE" up -d --build "$SERVICE"

if [ "$PROFILE" = "web" ]; then
  echo "Open http://localhost:6080/vnc.html"
elif [[ "$PROFILE" == "native" || "$PROFILE" == "jetson-gpu" ]]; then
  exec "${DC[@]}" --profile "$PROFILE" exec "$SERVICE" bash -lc '
    set -e
    mkdir -p "$XDG_RUNTIME_DIR"
    chmod 700 "$XDG_RUNTIME_DIR"
    if [ "$1" = jetson-gpu ]; then
      renderer=$(glxinfo -B 2>&1 || true)
      printf "%s\n" "$renderer"
      if ! printf "%s\n" "$renderer" | grep -Eq "OpenGL vendor string: (Mesa|llvmpipe|VMware)"; then
        echo "Mesa software OpenGL is not working. Keep the output above for diagnosis; use bash run.sh native for a stable CPU-render fallback." >&2
        exit 1
      fi
    fi
    if [ -f /opt/ros/humble/install/setup.bash ]; then
      source /opt/ros/humble/install/setup.bash
    else
      source /opt/ros/humble/setup.bash
    fi
    if [ -f /root/Documents/ros2_ws/install/setup.bash ]; then
      source /root/Documents/ros2_ws/install/setup.bash
    fi
    exec bash -i
  ' bash "$PROFILE"
else
  exec "${DC[@]}" --profile "$PROFILE" exec "$SERVICE" bash
fi
