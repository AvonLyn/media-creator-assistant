#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - 启动脚本
"""

import os
import sys
from app.main import main

if __name__ == "__main__":
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 检查环境变量
    if not os.path.exists('.env'):
        print("警告: 未找到.env文件，请从.env.example复制并配置")
    
    # 启动应用
    main() 