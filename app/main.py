#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - 主入口文件
"""

import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入GUI模块
from app.gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication

def main():
    """应用程序主入口函数"""
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    # 创建并显示主窗口
    main_window = MainWindow()
    main_window.show()
    
    # 运行应用程序事件循环
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 