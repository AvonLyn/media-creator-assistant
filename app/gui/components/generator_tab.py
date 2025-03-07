#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - 内容生成标签页
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QLineEdit, QTextEdit,
    QFormLayout, QGroupBox, QCheckBox, QSpinBox,
    QTabWidget, QSplitter, QFileDialog, QMessageBox,
    QRadioButton, QButtonGroup, QProgressBar
)
from PyQt5.QtCore import Qt, QSize

class GeneratorTab(QWidget):
    """内容生成标签页"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建分割器
        splitter = QSplitter(Qt.Vertical)
        
        # 上部分 - 论文选择和生成设置
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        
        # 论文选择组
        paper_group = QGroupBox("论文选择")
        paper_layout = QFormLayout()
        
        # 论文来源选择
        self.source_combo = QComboBox()
        self.source_combo.addItems(["已爬取论文", "手动输入"])
        self.source_combo.currentIndexChanged.connect(self.toggle_paper_source)
        paper_layout.addRow("论文来源:", self.source_combo)
        
        # 已爬取论文选择
        self.paper_combo = QComboBox()
        self.load_papers()
        paper_layout.addRow("选择论文:", self.paper_combo)
        
        # 手动输入论文信息
        self.paper_title_edit = QLineEdit()
        self.paper_title_edit.setPlaceholderText("输入论文标题")
        self.paper_title_edit.setEnabled(False)
        paper_layout.addRow("论文标题:", self.paper_title_edit)
        
        self.paper_abstract_edit = QTextEdit()
        self.paper_abstract_edit.setPlaceholderText("输入论文摘要")
        self.paper_abstract_edit.setEnabled(False)
        self.paper_abstract_edit.setMaximumHeight(100)
        paper_layout.addRow("论文摘要:", self.paper_abstract_edit)
        
        paper_group.setLayout(paper_layout)
        top_layout.addWidget(paper_group)
        
        # 生成设置组
        settings_group = QGroupBox("生成设置")
        settings_layout = QFormLayout()
        
        # 生成内容类型
        type_layout = QHBoxLayout()
        self.ppt_check = QCheckBox("PPT")
        self.ppt_check.setChecked(True)
        type_layout.addWidget(self.ppt_check)
        
        self.speech_check = QCheckBox("演讲稿")
        self.speech_check.setChecked(True)
        type_layout.addWidget(self.speech_check)
        
        settings_layout.addRow("生成内容:", type_layout)
        
        # 风格选择
        self.style_combo = QComboBox()
        self.style_combo.addItems(["学术风格", "通俗易懂", "技术深入", "自定义"])
        self.style_combo.currentIndexChanged.connect(self.toggle_custom_style)
        settings_layout.addRow("内容风格:", self.style_combo)
        
        # 自定义风格描述
        self.custom_style_edit = QTextEdit()
        self.custom_style_edit.setPlaceholderText("描述您期望的内容风格")
        self.custom_style_edit.setEnabled(False)
        self.custom_style_edit.setMaximumHeight(80)
        settings_layout.addRow("风格描述:", self.custom_style_edit)
        
        # 大模型选择
        self.model_combo = QComboBox()
        self.model_combo.addItems(["GPT-4", "Claude", "Gemini", "自定义API"])
        self.model_combo.currentIndexChanged.connect(self.toggle_custom_api)
        settings_layout.addRow("使用模型:", self.model_combo)
        
        # 自定义API设置
        self.api_edit = QLineEdit()
        self.api_edit.setPlaceholderText("输入API端点")
        self.api_edit.setEnabled(False)
        settings_layout.addRow("API端点:", self.api_edit)
        
        # 温度设置
        self.temperature_spin = QSpinBox()
        self.temperature_spin.setRange(0, 100)
        self.temperature_spin.setValue(70)
        self.temperature_spin.setSuffix("%")
        settings_layout.addRow("创造性:", self.temperature_spin)
        
        settings_group.setLayout(settings_layout)
        top_layout.addWidget(settings_group)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.generate_button = QPushButton("开始生成")
        self.generate_button.clicked.connect(self.start_generation)
        button_layout.addWidget(self.generate_button)
        
        self.cancel_button = QPushButton("取消生成")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel_generation)
        button_layout.addWidget(self.cancel_button)
        
        top_layout.addLayout(button_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        top_layout.addWidget(self.progress_bar)
        
        splitter.addWidget(top_widget)
        
        # 下部分 - 生成结果
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        
        # 结果标签页
        result_tabs = QTabWidget()
        
        # PPT内容标签页
        self.ppt_tab = QWidget()
        ppt_layout = QVBoxLayout(self.ppt_tab)
        
        self.ppt_content = QTextEdit()
        self.ppt_content.setReadOnly(True)
        ppt_layout.addWidget(self.ppt_content)
        
        ppt_button_layout = QHBoxLayout()
        
        self.save_ppt_button = QPushButton("保存PPT")
        self.save_ppt_button.clicked.connect(self.save_ppt)
        ppt_button_layout.addWidget(self.save_ppt_button)
        
        self.copy_ppt_button = QPushButton("复制内容")
        self.copy_ppt_button.clicked.connect(lambda: self.copy_content(self.ppt_content))
        ppt_button_layout.addWidget(self.copy_ppt_button)
        
        ppt_layout.addLayout(ppt_button_layout)
        
        result_tabs.addTab(self.ppt_tab, "PPT内容")
        
        # 演讲稿内容标签页
        self.speech_tab = QWidget()
        speech_layout = QVBoxLayout(self.speech_tab)
        
        self.speech_content = QTextEdit()
        self.speech_content.setReadOnly(True)
        speech_layout.addWidget(self.speech_content)
        
        speech_button_layout = QHBoxLayout()
        
        self.save_speech_button = QPushButton("保存演讲稿")
        self.save_speech_button.clicked.connect(self.save_speech)
        speech_button_layout.addWidget(self.save_speech_button)
        
        self.copy_speech_button = QPushButton("复制内容")
        self.copy_speech_button.clicked.connect(lambda: self.copy_content(self.speech_content))
        speech_button_layout.addWidget(self.copy_speech_button)
        
        speech_layout.addLayout(speech_button_layout)
        
        result_tabs.addTab(self.speech_tab, "演讲稿内容")
        
        # 日志标签页
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        
        self.log_content = QTextEdit()
        self.log_content.setReadOnly(True)
        log_layout.addWidget(self.log_content)
        
        result_tabs.addTab(log_tab, "生成日志")
        
        bottom_layout.addWidget(result_tabs)
        
        splitter.addWidget(bottom_widget)
        
        # 设置分割比例
        splitter.setSizes([400, 300])
        
        main_layout.addWidget(splitter)
    
    def load_papers(self):
        """加载已爬取的论文列表"""
        # TODO: 从数据库加载论文列表
        # 这里需要连接到core.crawler模块
        
        # 临时添加一些示例数据
        self.paper_combo.clear()
        self.paper_combo.addItems([
            "GPT-4: 大型语言模型的新突破",
            "DALL-E 3: 文本到图像生成的进展",
            "Transformer架构在自然语言处理中的应用"
        ])
    
    def toggle_paper_source(self, index):
        """切换论文来源"""
        if index == 0:  # 已爬取论文
            self.paper_combo.setEnabled(True)
            self.paper_title_edit.setEnabled(False)
            self.paper_abstract_edit.setEnabled(False)
        else:  # 手动输入
            self.paper_combo.setEnabled(False)
            self.paper_title_edit.setEnabled(True)
            self.paper_abstract_edit.setEnabled(True)
    
    def toggle_custom_style(self, index):
        """切换自定义风格"""
        if self.style_combo.currentText() == "自定义":
            self.custom_style_edit.setEnabled(True)
        else:
            self.custom_style_edit.setEnabled(False)
    
    def toggle_custom_api(self, index):
        """切换自定义API"""
        if self.model_combo.currentText() == "自定义API":
            self.api_edit.setEnabled(True)
        else:
            self.api_edit.setEnabled(False)
    
    def start_generation(self):
        """开始生成内容"""
        # 检查是否选择了生成内容类型
        if not self.ppt_check.isChecked() and not self.speech_check.isChecked():
            QMessageBox.warning(self, "警告", "请至少选择一种生成内容类型")
            return
        
        # 获取论文信息
        paper_info = self.get_paper_info()
        if not paper_info:
            return
        
        # 获取生成设置
        settings = self.get_generation_settings()
        
        # 更新UI状态
        self.generate_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress_bar.setValue(0)
        
        # 清空结果
        self.ppt_content.clear()
        self.speech_content.clear()
        
        # 记录日志
        self.log_content.append(f"开始生成内容，论文：{paper_info['title']}")
        self.log_content.append(f"生成设置：{settings}")
        
        # TODO: 调用内容生成模块
        # 这里需要连接到core.generator模块
        
        # 模拟生成过程
        self.simulate_generation()
    
    def get_paper_info(self):
        """获取论文信息"""
        if self.source_combo.currentIndex() == 0:  # 已爬取论文
            title = self.paper_combo.currentText()
            if not title:
                QMessageBox.warning(self, "警告", "请选择一篇论文")
                return None
            
            # TODO: 从数据库获取论文摘要
            # 这里需要连接到core.crawler模块
            
            # 临时使用示例数据
            abstract = "这是一篇关于大型语言模型的论文，探讨了最新的技术进展和应用场景。"
            
            return {
                "title": title,
                "abstract": abstract
            }
        else:  # 手动输入
            title = self.paper_title_edit.text()
            abstract = self.paper_abstract_edit.toPlainText()
            
            if not title:
                QMessageBox.warning(self, "警告", "请输入论文标题")
                return None
            
            if not abstract:
                QMessageBox.warning(self, "警告", "请输入论文摘要")
                return None
            
            return {
                "title": title,
                "abstract": abstract
            }
    
    def get_generation_settings(self):
        """获取生成设置"""
        settings = {
            "generate_ppt": self.ppt_check.isChecked(),
            "generate_speech": self.speech_check.isChecked(),
            "style": self.style_combo.currentText(),
            "model": self.model_combo.currentText(),
            "temperature": self.temperature_spin.value() / 100.0
        }
        
        if settings["style"] == "自定义":
            settings["custom_style"] = self.custom_style_edit.toPlainText()
        
        if settings["model"] == "自定义API":
            settings["api_endpoint"] = self.api_edit.text()
        
        return settings
    
    def cancel_generation(self):
        """取消生成内容"""
        # 更新UI状态
        self.generate_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # 记录日志
        self.log_content.append("已取消生成")
        
        # TODO: 调用内容生成模块取消生成
        # 这里需要连接到core.generator模块
    
    def simulate_generation(self):
        """模拟生成过程（仅用于演示）"""
        # 模拟PPT内容
        if self.ppt_check.isChecked():
            ppt_content = """# GPT-4: 大型语言模型的新突破

## 第1页：标题
- 标题：GPT-4: 大型语言模型的新突破
- 作者：OpenAI研究团队
- 日期：2023年

## 第2页：摘要
- GPT-4是OpenAI发布的最新大型语言模型
- 相比GPT-3有显著性能提升
- 在多项基准测试中表现优异
- 具有更强的推理能力和更少的幻觉

## 第3页：研究背景
- 大型语言模型的发展历程
- GPT系列模型的演进
- 当前大模型面临的主要挑战

## 第4页：技术创新
- 更大的参数规模
- 改进的训练方法
- 更强的推理能力
- 更好的对齐技术

## 第5页：实验结果
- 在多项NLP基准测试中的表现
- 与GPT-3的对比分析
- 在实际应用场景中的效果评估

## 第6页：结论与展望
- GPT-4的主要贡献
- 当前局限性
- 未来研究方向"""
            
            self.ppt_content.setText(ppt_content)
        
        # 模拟演讲稿内容
        if self.speech_check.isChecked():
            speech_content = """# GPT-4: 大型语言模型的新突破

大家好，今天我要向大家介绍OpenAI最新发布的大型语言模型GPT-4。

GPT-4是目前最先进的大型语言模型之一，相比其前身GPT-3有了显著的性能提升。它在多项基准测试中表现优异，展示了更强的推理能力和更少的幻觉现象。

首先，让我们回顾一下大型语言模型的发展历程。从早期的BERT到GPT系列，大型语言模型的规模和能力不断提升。然而，当前的大模型仍然面临着幻觉、偏见和安全性等多方面的挑战。

GPT-4的技术创新主要体现在以下几个方面：
1. 更大的参数规模，使模型能够捕捉更复杂的语言模式
2. 改进的训练方法，提高了模型的学习效率
3. 更强的推理能力，能够处理更复杂的任务
4. 更好的对齐技术，减少了有害输出

在实验结果方面，GPT-4在多项NLP基准测试中都取得了优异的成绩。与GPT-3相比，它在几乎所有任务上都有显著提升，特别是在需要复杂推理的任务上。在实际应用场景中，GPT-4也展示了更强的实用性。

总结来说，GPT-4代表了大型语言模型的最新突破，它不仅在性能上有所提升，还在安全性和实用性方面取得了进展。当然，它仍然存在一些局限性，如对事实的准确性仍有提升空间，对长文本的理解能力有限等。

未来的研究方向可能包括进一步提升模型的事实准确性，增强长文本理解能力，以及探索多模态能力的融合。

谢谢大家的聆听，有什么问题欢迎提问。"""
            
            self.speech_content.setText(speech_content)
        
        # 更新UI状态
        self.generate_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.progress_bar.setValue(100)
        
        # 记录日志
        self.log_content.append("内容生成完成")
        
        QMessageBox.information(self, "成功", "内容生成完成")
    
    def save_ppt(self):
        """保存PPT内容"""
        if not self.ppt_content.toPlainText():
            QMessageBox.warning(self, "警告", "没有可保存的PPT内容")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存PPT内容",
            "PPT内容.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.ppt_content.toPlainText())
                
                QMessageBox.information(self, "成功", "PPT内容已保存")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
    
    def save_speech(self):
        """保存演讲稿内容"""
        if not self.speech_content.toPlainText():
            QMessageBox.warning(self, "警告", "没有可保存的演讲稿内容")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存演讲稿内容",
            "演讲稿内容.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.speech_content.toPlainText())
                
                QMessageBox.information(self, "成功", "演讲稿内容已保存")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
    
    def copy_content(self, text_edit):
        """复制内容到剪贴板"""
        text_edit.selectAll()
        text_edit.copy()
        QMessageBox.information(self, "成功", "内容已复制到剪贴板") 