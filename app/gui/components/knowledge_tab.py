#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - 知识库管理标签页
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QLineEdit, QTextEdit,
    QFormLayout, QGroupBox, QTabWidget, QFileDialog,
    QListWidget, QListWidgetItem, QSplitter, QMessageBox
)
from PyQt5.QtCore import Qt, QSize

class KnowledgeTab(QWidget):
    """知识库管理标签页"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建子标签页
        sub_tabs = QTabWidget()
        
        # 添加PPT制作方法标签页
        ppt_tab = self.create_method_tab("PPT")
        sub_tabs.addTab(ppt_tab, "PPT制作方法")
        
        # 添加演讲稿制作方法标签页
        speech_tab = self.create_method_tab("演讲稿")
        sub_tabs.addTab(speech_tab, "演讲稿制作方法")
        
        # 添加历史内容标签页
        history_tab = self.create_history_tab()
        sub_tabs.addTab(history_tab, "历史内容")
        
        # 将子标签页添加到主布局
        main_layout.addWidget(sub_tabs)
        
    def create_method_tab(self, method_type):
        """创建制作方法标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧列表
        list_widget = QListWidget()
        list_widget.setMaximumWidth(200)
        splitter.addWidget(list_widget)
        
        # 右侧编辑区
        edit_widget = QWidget()
        edit_layout = QVBoxLayout(edit_widget)
        
        # 标题输入
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("标题:"))
        title_edit = QLineEdit()
        title_layout.addWidget(title_edit)
        edit_layout.addLayout(title_layout)
        
        # 内容编辑
        content_label = QLabel("内容:")
        edit_layout.addWidget(content_label)
        
        content_edit = QTextEdit()
        edit_layout.addWidget(content_edit)
        
        # 按钮组
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("保存")
        save_button.clicked.connect(lambda: self.save_method(method_type, title_edit, content_edit))
        button_layout.addWidget(save_button)
        
        delete_button = QPushButton("删除")
        delete_button.clicked.connect(lambda: self.delete_method(method_type, list_widget))
        button_layout.addWidget(delete_button)
        
        import_button = QPushButton("导入")
        import_button.clicked.connect(lambda: self.import_method(method_type, list_widget))
        button_layout.addWidget(import_button)
        
        export_button = QPushButton("导出")
        export_button.clicked.connect(lambda: self.export_method(method_type, list_widget))
        button_layout.addWidget(export_button)
        
        edit_layout.addLayout(button_layout)
        
        splitter.addWidget(edit_widget)
        
        # 设置初始分割比例
        splitter.setSizes([200, 600])
        
        layout.addWidget(splitter)
        
        # 存储控件引用
        setattr(self, f"{method_type.lower()}_list", list_widget)
        setattr(self, f"{method_type.lower()}_title", title_edit)
        setattr(self, f"{method_type.lower()}_content", content_edit)
        
        # 连接列表选择事件
        list_widget.currentItemChanged.connect(
            lambda current, previous: self.load_method_content(method_type, current)
        )
        
        # 加载方法列表
        self.load_method_list(method_type, list_widget)
        
        return tab
    
    def create_history_tab(self):
        """创建历史内容标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧列表
        list_widget = QListWidget()
        list_widget.setMaximumWidth(200)
        splitter.addWidget(list_widget)
        
        # 右侧内容查看区
        view_widget = QWidget()
        view_layout = QVBoxLayout(view_widget)
        
        # 标题显示
        title_label = QLabel("标题:")
        view_layout.addWidget(title_label)
        
        # 类型显示
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("类型:"))
        type_combo = QComboBox()
        type_combo.addItems(["PPT", "演讲稿"])
        type_layout.addWidget(type_combo)
        view_layout.addLayout(type_layout)
        
        # 内容显示
        content_label = QLabel("内容:")
        view_layout.addWidget(content_label)
        
        content_view = QTextEdit()
        content_view.setReadOnly(True)
        view_layout.addWidget(content_view)
        
        # 按钮组
        button_layout = QHBoxLayout()
        
        delete_button = QPushButton("删除")
        delete_button.clicked.connect(lambda: self.delete_history(list_widget))
        button_layout.addWidget(delete_button)
        
        export_button = QPushButton("导出")
        export_button.clicked.connect(lambda: self.export_history(list_widget))
        button_layout.addWidget(export_button)
        
        view_layout.addLayout(button_layout)
        
        splitter.addWidget(view_widget)
        
        # 设置初始分割比例
        splitter.setSizes([200, 600])
        
        layout.addWidget(splitter)
        
        # 存储控件引用
        self.history_list = list_widget
        self.history_type = type_combo
        self.history_content = content_view
        
        # 连接列表选择事件
        list_widget.currentItemChanged.connect(
            lambda current, previous: self.load_history_content(current)
        )
        
        # 加载历史内容列表
        self.load_history_list(list_widget)
        
        return tab
    
    def load_method_list(self, method_type, list_widget):
        """加载制作方法列表"""
        # TODO: 从数据库加载方法列表
        # 这里需要连接到core.knowledge模块
        
        # 临时添加一些示例数据
        if method_type == "PPT":
            list_widget.addItem("AI论文PPT制作模板")
            list_widget.addItem("科技风格PPT设计")
        else:
            list_widget.addItem("AI论文讲解演讲稿模板")
            list_widget.addItem("技术分享演讲技巧")
    
    def load_method_content(self, method_type, current_item):
        """加载制作方法内容"""
        if not current_item:
            return
        
        title = current_item.text()
        title_edit = getattr(self, f"{method_type.lower()}_title")
        content_edit = getattr(self, f"{method_type.lower()}_content")
        
        title_edit.setText(title)
        
        # TODO: 从数据库加载方法内容
        # 这里需要连接到core.knowledge模块
        
        # 临时添加一些示例数据
        if method_type == "PPT":
            if title == "AI论文PPT制作模板":
                content_edit.setText("1. 标题页：论文标题、作者、日期\n2. 摘要页：研究背景、目标、方法\n3. 问题定义页：研究问题的详细描述\n4. 相关工作页：已有研究的总结\n5. 方法页：提出的方法详解\n6. 实验页：实验设置、数据集、评估指标\n7. 结果页：实验结果与分析\n8. 结论页：总结与未来工作")
            elif title == "科技风格PPT设计":
                content_edit.setText("1. 配色：蓝色、灰色为主，点缀亮色\n2. 字体：无衬线字体，如Arial、Helvetica\n3. 图表：简洁清晰，避免过度装饰\n4. 动画：简单过渡，避免花哨效果\n5. 布局：留白充足，信息层次分明")
        else:
            if title == "AI论文讲解演讲稿模板":
                content_edit.setText("1. 开场白：简短介绍论文背景和重要性\n2. 研究问题：清晰阐述论文要解决的问题\n3. 相关工作：简要回顾已有方法的优缺点\n4. 提出方法：详细解释论文的创新点\n5. 实验结果：重点展示关键结果和比较\n6. 结论与展望：总结论文贡献和未来方向\n7. 互动环节：准备可能的问答")
            elif title == "技术分享演讲技巧":
                content_edit.setText("1. 控制节奏：保持适中的语速，重点处放慢\n2. 专业术语：首次出现时给出解释\n3. 类比解释：用生活中的例子解释复杂概念\n4. 视觉辅助：关键点配合PPT图表展示\n5. 互动设计：适时提问，保持听众注意力")
    
    def save_method(self, method_type, title_edit, content_edit):
        """保存制作方法"""
        title = title_edit.text()
        content = content_edit.toPlainText()
        
        if not title:
            QMessageBox.warning(self, "警告", "标题不能为空")
            return
        
        if not content:
            QMessageBox.warning(self, "警告", "内容不能为空")
            return
        
        # TODO: 保存到数据库
        # 这里需要连接到core.knowledge模块
        
        QMessageBox.information(self, "成功", f"{method_type}制作方法已保存")
        
        # 刷新列表
        list_widget = getattr(self, f"{method_type.lower()}_list")
        
        # 检查是否已存在
        items = list_widget.findItems(title, Qt.MatchExactly)
        if not items:
            list_widget.addItem(title)
    
    def delete_method(self, method_type, list_widget):
        """删除制作方法"""
        current_item = list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择要删除的项目")
            return
        
        reply = QMessageBox.question(
            self, 
            '确认删除', 
            f"确定要删除{current_item.text()}吗？",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # TODO: 从数据库删除
            # 这里需要连接到core.knowledge模块
            
            list_widget.takeItem(list_widget.row(current_item))
            
            title_edit = getattr(self, f"{method_type.lower()}_title")
            content_edit = getattr(self, f"{method_type.lower()}_content")
            
            title_edit.clear()
            content_edit.clear()
    
    def import_method(self, method_type, list_widget):
        """导入制作方法"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "导入制作方法",
            "",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    title = f.readline().strip()
                    content = f.read()
                
                if not title:
                    QMessageBox.warning(self, "警告", "导入文件格式不正确，第一行应为标题")
                    return
                
                # TODO: 保存到数据库
                # 这里需要连接到core.knowledge模块
                
                # 检查是否已存在
                items = list_widget.findItems(title, Qt.MatchExactly)
                if not items:
                    list_widget.addItem(title)
                
                QMessageBox.information(self, "成功", f"{method_type}制作方法已导入")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入失败: {str(e)}")
    
    def export_method(self, method_type, list_widget):
        """导出制作方法"""
        current_item = list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择要导出的项目")
            return
        
        title = current_item.text()
        content_edit = getattr(self, f"{method_type.lower()}_content")
        content = content_edit.toPlainText()
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "导出制作方法",
            f"{title}.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"{title}\n{content}")
                
                QMessageBox.information(self, "成功", f"{method_type}制作方法已导出")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
    
    def load_history_list(self, list_widget):
        """加载历史内容列表"""
        # TODO: 从数据库加载历史内容列表
        # 这里需要连接到core.knowledge模块
        
        # 临时添加一些示例数据
        list_widget.addItem("GPT-4论文解析")
        list_widget.addItem("DALL-E 3技术原理")
    
    def load_history_content(self, current_item):
        """加载历史内容"""
        if not current_item:
            return
        
        title = current_item.text()
        
        # TODO: 从数据库加载历史内容
        # 这里需要连接到core.knowledge模块
        
        # 临时添加一些示例数据
        if title == "GPT-4论文解析":
            self.history_type.setCurrentText("PPT")
            self.history_content.setText("# GPT-4论文解析\n\n## 背景\nGPT-4是OpenAI发布的大型语言模型，相比GPT-3有显著提升。\n\n## 技术创新\n1. 更大的参数规模\n2. 改进的训练方法\n3. 更强的推理能力\n\n## 性能评估\n在多项基准测试中，GPT-4均优于GPT-3。")
        elif title == "DALL-E 3技术原理":
            self.history_type.setCurrentText("演讲稿")
            self.history_content.setText("今天我们来讨论DALL-E 3的技术原理。\n\nDALL-E 3是OpenAI最新的文本到图像生成模型，它能够根据文本描述生成高质量的图像。\n\n与前代模型相比，DALL-E 3在图像质量、文本理解和创意表达方面都有显著提升。\n\n它采用了扩散模型作为基础架构，并结合了大型语言模型来增强对文本提示的理解。")
    
    def delete_history(self, list_widget):
        """删除历史内容"""
        current_item = list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择要删除的项目")
            return
        
        reply = QMessageBox.question(
            self, 
            '确认删除', 
            f"确定要删除{current_item.text()}吗？",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # TODO: 从数据库删除
            # 这里需要连接到core.knowledge模块
            
            list_widget.takeItem(list_widget.row(current_item))
            self.history_content.clear()
    
    def export_history(self, list_widget):
        """导出历史内容"""
        current_item = list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择要导出的项目")
            return
        
        title = current_item.text()
        content = self.history_content.toPlainText()
        content_type = self.history_type.currentText()
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "导出历史内容",
            f"{title}.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"标题: {title}\n类型: {content_type}\n\n{content}")
                
                QMessageBox.information(self, "成功", "历史内容已导出")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}") 