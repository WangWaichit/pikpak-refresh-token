#!/bin/bash
# PikPak Refresh Token 一键获取
# 用法: bash refresh.sh
set -e
TMP=$(mktemp /tmp/pikpak_token.XXXXXX.py)
trap "rm -f $TMP" EXIT
curl -fsSL https://raw.githubusercontent.com/WangWaichit/pikpak-refresh-token/main/get_refresh_token.py -o "$TMP"
python3 "$TMP"
