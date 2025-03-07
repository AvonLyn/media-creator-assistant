#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - 论文爬取标签页
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QLineEdit, QTextEdit,
    QFormLayout, QGroupBox, QCheckBox, QSpinBox,
    QDateEdit, QProgressBar, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PyQt5.QtCore import Qt, QDate

class CrawlerTab(QWidget):
    """论文爬取标签页"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建爬取设置组
        settings_group = QGroupBox("爬取设置")
        settings_layout = QFormLayout()
        
        # 论文源选择
        self.source_combo = QComboBox()
        self.source_combo.addItems(["arXiv", "Semantic Scholar", "Google Scholar", "Papers With Code"])
        settings_layout.addRow("论文源:", self.source_combo)
        
        # 关键词输入
        self.keywords_edit = QLineEdit()
        self.keywords_edit.setPlaceholderText("输入关键词，多个关键词用逗号分隔")
        settings_layout.addRow("关键词:", self.keywords_edit)
        
        # 日期选择
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        settings_layout.addRow("日期:", self.date_edit)
        
        # 数量设置
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 100)
        self.count_spin.setValue(10)
        settings_layout.addRow("爬取数量:", self.count_spin)
        
        # 设置组完成
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)
        
        # 创建操作按钮组
        button_layout = QHBoxLayout()
        
        # 开始爬取按钮
        self.start_button = QPushButton("开始爬取")
        self.start_button.clicked.connect(self.start_crawling)
        button_layout.addWidget(self.start_button)
        
        # 停止爬取按钮
        self.stop_button = QPushButton("停止爬取")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_crawling)
        button_layout.addWidget(self.stop_button)
        
        # 清空结果按钮
        self.clear_button = QPushButton("清空结果")
        self.clear_button.clicked.connect(self.clear_results)
        button_layout.addWidget(self.clear_button)
        
        # 添加按钮组到主布局
        main_layout.addLayout(button_layout)
        
        # 创建进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # 创建结果表格
        self.result_table = QTableWidget(0, 4)
        self.result_table.setHorizontalHeaderLabels(["标题", "作者", "日期", "链接"])
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.result_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        main_layout.addWidget(self.result_table)
        
        # 创建日志区域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        main_layout.addWidget(QLabel("日志:"))
        main_layout.addWidget(self.log_text)
        
    def start_crawling(self):
        """开始爬取论文"""
        # 获取设置参数
        source = self.source_combo.currentText()
        keywords = self.keywords_edit.text()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        count = self.count_spin.value()
        
        # 更新UI状态
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setValue(0)
        
        # 记录日志
        self.log_text.append(f"开始从{source}爬取论文，关键词: {keywords}, 日期: {date}, 数量: {count}")
        
        # TODO: 调用爬虫模块进行爬取
        # 这里需要连接到core.crawler模块
        
    def stop_crawling(self):
        """停止爬取论文"""
        # 更新UI状态
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # 记录日志
        self.log_text.append("爬取已停止")
        
        # TODO: 调用爬虫模块停止爬取
        
    def clear_results(self):
        """清空结果"""
        self.result_table.setRowCount(0)
        self.log_text.clear()
        self.progress_bar.setValue(0)
        
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
        
    def add_paper(self, title, authors, date, link):
        """添加论文到结果表格"""
        row = self.result_table.rowCount()
        self.result_table.insertRow(row)
        
        self.result_table.setItem(row, 0, QTableWidgetItem(title))
        self.result_table.setItem(row, 1, QTableWidgetItem(authors))
        self.result_table.setItem(row, 2, QTableWidgetItem(date))
        self.result_table.setItem(row, 3, QTableWidgetItem(link)) 