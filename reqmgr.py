#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
需求管理系統 CLI 工具啟動腳本

這是 CLI 工具的主要入口點。
"""

import sys
from pathlib import Path

# 添加 CLI 模組到 Python 路徑
cli_path = Path(__file__).parent / 'cli'
sys.path.insert(0, str(cli_path))

if __name__ == '__main__':
    from cli.main import main
    main() 