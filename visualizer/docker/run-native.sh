#!/usr/bin/env bash
# Run from the Jetson's desktop session: bash run-native.sh
# Opens a ROS-ready shell. Run rviz2 inside the container when needed.
set -euo pipefail

if [[ -z "${DISPLAY:-}" ]]; then
  echo "DISPLAY is unset. Run this script from a terminal on the Jetson desktop." >&2
  exit 1
fi

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

# X11 authorization belongs to the host desktop session, not the image.
xhost +si:localuser:root
docker compose --profile native up -d robotics-native

exec docker compose exec robotics-native bash -lc '
  set -e
  mkdir -p "$XDG_RUNTIME_DIR"
  chmod 700 "$XDG_RUNTIME_DIR"
  source /opt/ros/humble/setup.bash
  if [ -f /root/Documents/ros2_ws/install/setup.bash ]; then
    source /root/Documents/ros2_ws/install/setup.bash
  fi
  exec bash -i
'
