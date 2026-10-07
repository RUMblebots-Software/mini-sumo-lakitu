#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
    printf 'Usage: %s FOLDER\n' "$0" >&2
    exit 1
fi

folder=$1

if [[ ! -d "$folder" ]]; then
    printf 'Error: not a directory: %s\n' "$folder" >&2
    exit 1
fi

user_id=${SUDO_UID:-$(id -u)}
group_id=${SUDO_GID:-$(id -g)}

find -P "$folder" -mindepth 1 -exec chown "$user_id:$group_id" {} +
printf 'Updated ownership in %s to %s:%s\n' "$folder" "$user_id" "$group_id"