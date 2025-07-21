#!/bin/bash

WATCH_DIR=~/path
DEST=gdrive:feature
LOG=~/logs/drive_loop.log

mkdir -p ~/logs
mkdir -p "$WATCH_DIR"

echo "[$(date)] Initial full sync" >> "$LOG"
rclone copy "$WATCH_DIR" "$DEST" --update --log-file="$LOG"

echo "[$(date)] Entering loop for 30-second sync..." >> "$LOG"

while true; do
    sleep 30
    echo "[$(date)] Sync tick" >> "$LOG"
    rclone copy "$WATCH_DIR" "$DEST" --update --log-file="$LOG"
done
