#!/bin/sh

if command -v "${1}" >/dev/null 2>&1; then
    exec "${@}"
fi

exec python -- /app/infer.py "${@}"

