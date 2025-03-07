#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - 知识库管理模块
"""

from app.data.database import PPTMethod, SpeechMethod, HistoryContent, get_session

class KnowledgeManager:
    """知识库管理类"""
    
    def __init__(self):
        """初始化知识库管理器"""
        self.session = get_session()
    
    # PPT制作方法管理
    
    def get_ppt_methods(self):
        """获取所有PPT制作方法
        
        Returns:
            list: PPT制作方法列表
        """
        return self.session.query(PPTMethod).order_by(PPTMethod.title).all()
    
    def get_ppt_method_by_id(self, method_id):
        """根据ID获取PPT制作方法
        
        Args:
            method_id (int): 方法ID
            
        Returns:
            PPTMethod: PPT制作方法对象
        """
        return self.session.query(PPTMethod).filter(PPTMethod.id == method_id).first()
    
    def get_ppt_method_by_title(self, title):
        """根据标题获取PPT制作方法
        
        Args:
            title (str): 方法标题
            
        Returns:
            PPTMethod: PPT制作方法对象
        """
        return self.session.query(PPTMethod).filter(PPTMethod.title == title).first()
    
    def add_ppt_method(self, title, content):
        """添加PPT制作方法
        
        Args:
            title (str): 方法标题
            content (str): 方法内容
            
        Returns:
            PPTMethod: 添加的PPT制作方法对象
        """
        # 检查是否已存在
        existing = self.get_ppt_method_by_title(title)
        if existing:
            # 更新内容
            existing.content = content
            self.session.commit()
            return existing
        
        # 创建新方法
        method = PPTMethod(title=title, content=content)
        self.session.add(method)
        self.session.commit()
        return method
    
    def update_ppt_method(self, method_id, title, content):
        """更新PPT制作方法
        
        Args:
            method_id (int): 方法ID
            title (str): 方法标题
            content (str): 方法内容
            
        Returns:
            PPTMethod: 更新的PPT制作方法对象
        """
        method = self.get_ppt_method_by_id(method_id)
        if not method:
            return None
        
        method.title = title
        method.content = content
        self.session.commit()
        return method
    
    def delete_ppt_method(self, method_id):
        """删除PPT制作方法
        
        Args:
            method_id (int): 方法ID
            
        Returns:
            bool: 是否成功删除
        """
        method = self.get_ppt_method_by_id(method_id)
        if not method:
            return False
        
        self.session.delete(method)
        self.session.commit()
        return True
    
    # 演讲稿制作方法管理
    
    def get_speech_methods(self):
        """获取所有演讲稿制作方法
        
        Returns:
            list: 演讲稿制作方法列表
        """
        return self.session.query(SpeechMethod).order_by(SpeechMethod.title).all()
    
    def get_speech_method_by_id(self, method_id):
        """根据ID获取演讲稿制作方法
        
        Args:
            method_id (int): 方法ID
            
        Returns:
            SpeechMethod: 演讲稿制作方法对象
        """
        return self.session.query(SpeechMethod).filter(SpeechMethod.id == method_id).first()
    
    def get_speech_method_by_title(self, title):
        """根据标题获取演讲稿制作方法
        
        Args:
            title (str): 方法标题
            
        Returns:
            SpeechMethod: 演讲稿制作方法对象
        """
        return self.session.query(SpeechMethod).filter(SpeechMethod.title == title).first()
    
    def add_speech_method(self, title, content):
        """添加演讲稿制作方法
        
        Args:
            title (str): 方法标题
            content (str): 方法内容
            
        Returns:
            SpeechMethod: 添加的演讲稿制作方法对象
        """
        # 检查是否已存在
        existing = self.get_speech_method_by_title(title)
        if existing:
            # 更新内容
            existing.content = content
            self.session.commit()
            return existing
        
        # 创建新方法
        method = SpeechMethod(title=title, content=content)
        self.session.add(method)
        self.session.commit()
        return method
    
    def update_speech_method(self, method_id, title, content):
        """更新演讲稿制作方法
        
        Args:
            method_id (int): 方法ID
            title (str): 方法标题
            content (str): 方法内容
            
        Returns:
            SpeechMethod: 更新的演讲稿制作方法对象
        """
        method = self.get_speech_method_by_id(method_id)
        if not method:
            return None
        
        method.title = title
        method.content = content
        self.session.commit()
        return method
    
    def delete_speech_method(self, method_id):
        """删除演讲稿制作方法
        
        Args:
            method_id (int): 方法ID
            
        Returns:
            bool: 是否成功删除
        """
        method = self.get_speech_method_by_id(method_id)
        if not method:
            return False
        
        self.session.delete(method)
        self.session.commit()
        return True
    
    # 历史内容管理
    
    def get_history_contents(self):
        """获取所有历史内容
        
        Returns:
            list: 历史内容列表
        """
        return self.session.query(HistoryContent).order_by(HistoryContent.created_date.desc()).all()
    
    def get_history_content_by_id(self, content_id):
        """根据ID获取历史内容
        
        Args:
            content_id (int): 内容ID
            
        Returns:
            HistoryContent: 历史内容对象
        """
        return self.session.query(HistoryContent).filter(HistoryContent.id == content_id).first()
    
    def get_history_content_by_title(self, title):
        """根据标题获取历史内容
        
        Args:
            title (str): 内容标题
            
        Returns:
            HistoryContent: 历史内容对象
        """
        return self.session.query(HistoryContent).filter(HistoryContent.title == title).first()
    
    def add_history_content(self, title, content_type, content, paper_id=None):
        """添加历史内容
        
        Args:
            title (str): 内容标题
            content_type (str): 内容类型，如"PPT"或"演讲稿"
            content (str): 内容
            paper_id (int, optional): 关联的论文ID
            
        Returns:
            HistoryContent: 添加的历史内容对象
        """
        # 检查是否已存在
        existing = self.get_history_content_by_title(title)
        if existing:
            # 更新内容
            existing.content_type = content_type
            existing.content = content
            existing.paper_id = paper_id
            self.session.commit()
            return existing
        
        # 创建新内容
        history = HistoryContent(
            title=title,
            content_type=content_type,
            content=content,
            paper_id=paper_id
        )
        self.session.add(history)
        self.session.commit()
        return history
    
    def update_history_content(self, content_id, title, content_type, content, paper_id=None):
        """更新历史内容
        
        Args:
            content_id (int): 内容ID
            title (str): 内容标题
            content_type (str): 内容类型，如"PPT"或"演讲稿"
            content (str): 内容
            paper_id (int, optional): 关联的论文ID
            
        Returns:
            HistoryContent: 更新的历史内容对象
        """
        history = self.get_history_content_by_id(content_id)
        if not history:
            return None
        
        history.title = title
        history.content_type = content_type
        history.content = content
        history.paper_id = paper_id
        self.session.commit()
        return history
    
    def delete_history_content(self, content_id):
        """删除历史内容
        
        Args:
            content_id (int): 内容ID
            
        Returns:
            bool: 是否成功删除
        """
        history = self.get_history_content_by_id(content_id)
        if not history:
            return False
        
        self.session.delete(history)
        self.session.commit()
        return True
    
    def __del__(self):
        """析构函数"""
        self.session.close()