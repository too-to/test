#!/bin/bash

SRC=~/features                 # 피처 파일이 저장되는 로컬 경로
DST=~/mydrive/features         # Google Drive에 연결된 디렉토리 (rclone mount한 곳)
mkdir -p "$DST"                # 대상 폴더가 없으면 만든다

rclone copy "$SRC" "$DST" \
  --update \                   # 변경된 파일만 복사
  --log-file=~/logs/drive_sync.log   # 로그 파일로 저장
