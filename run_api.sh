#!/bin/bash
# iBrushPal API 启动脚本
cd "$(dirname "$0")"
source .venv/bin/activate
python teeth_detection_api.py