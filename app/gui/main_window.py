#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - 主窗口
"""

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTabWidget, QLabel, QStatusBar,
    QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

# 导入组件
from app.gui.components.crawler_tab import CrawlerTab
from app.gui.components.knowledge_tab import KnowledgeTab
from app.gui.components.generator_tab import GeneratorTab

class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle("自媒体博主自动化辅助平台")
        self.setMinimumSize(1000, 700)
        
        # 初始化UI
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标题
        title_label = QLabel("自媒体博主自动化辅助平台")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title_label)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 添加论文爬取标签页
        crawler_tab = CrawlerTab()
        tab_widget.addTab(crawler_tab, "论文爬取")
        
        # 添加知识库管理标签页
        knowledge_tab = KnowledgeTab()
        tab_widget.addTab(knowledge_tab, "知识库管理")
        
        # 添加内容生成标签页
        generator_tab = GeneratorTab()
        tab_widget.addTab(generator_tab, "内容生成")
        
        # 将标签页添加到主布局
        main_layout.addWidget(tab_widget)
        
        # 创建状态栏
        status_bar = QStatusBar()
        status_bar.showMessage("就绪")
        self.setStatusBar(status_bar)
        
    def closeEvent(self, event):
        """关闭窗口事件处理"""
        reply = QMessageBox.question(
            self, 
            '确认退出', 
            "确定要退出应用程序吗？",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 