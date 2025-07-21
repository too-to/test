#!/bin/bash

SRC=~/features
DST=gdrive:feature
LOG=~/logs/drive_sync.log

mkdir -p "$SRC"
mkdir -p ~/logs

echo "[$(date)] Sync start" >> "$LOG"
rclone copy "$SRC" "$DST" --update --log-file="$LOG"
echo "[$(date)] Sync complete" >> "$LOG"

