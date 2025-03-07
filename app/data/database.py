#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - 数据库管理模块
"""

import os
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# 获取数据库文件路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                      'app', 'data', 'media_creator.db')

# 创建SQLAlchemy引擎
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)

# 创建基类
Base = declarative_base()

# 定义论文表
class Paper(Base):
    """论文数据模型"""
    __tablename__ = 'papers'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    authors = Column(String(255))
    abstract = Column(Text)
    url = Column(String(255))
    source = Column(String(50))
    published_date = Column(DateTime)
    crawled_date = Column(DateTime, default=datetime.datetime.now)
    
    def __repr__(self):
        return f"<Paper(title='{self.title}')>"

# 定义PPT制作方法表
class PPTMethod(Base):
    """PPT制作方法数据模型"""
    __tablename__ = 'ppt_methods'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
        return f"<PPTMethod(title='{self.title}')>"

# 定义演讲稿制作方法表
class SpeechMethod(Base):
    """演讲稿制作方法数据模型"""
    __tablename__ = 'speech_methods'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
        return f"<SpeechMethod(title='{self.title}')>"

# 定义历史内容表
class HistoryContent(Base):
    """历史内容数据模型"""
    __tablename__ = 'history_contents'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content_type = Column(String(50), nullable=False)  # PPT或演讲稿
    content = Column(Text, nullable=False)
    paper_id = Column(Integer, ForeignKey('papers.id'))
    created_date = Column(DateTime, default=datetime.datetime.now)
    
    # 关联论文
    paper = relationship("Paper", backref="history_contents")
    
    def __repr__(self):
        return f"<HistoryContent(title='{self.title}', type='{self.content_type}')>"

# 创建数据库会话
Session = sessionmaker(bind=engine)

def init_db():
    """初始化数据库"""
    # 创建数据库目录
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # 创建表
    Base.metadata.create_all(engine)
    
    # 添加一些初始数据
    session = Session()
    
    # 检查是否已有数据
    if session.query(PPTMethod).count() == 0:
        # 添加PPT制作方法示例
        ppt_method1 = PPTMethod(
            title="AI论文PPT制作模板",
            content="1. 标题页：论文标题、作者、日期\n2. 摘要页：研究背景、目标、方法\n3. 问题定义页：研究问题的详细描述\n4. 相关工作页：已有研究的总结\n5. 方法页：提出的方法详解\n6. 实验页：实验设置、数据集、评估指标\n7. 结果页：实验结果与分析\n8. 结论页：总结与未来工作"
        )
        
        ppt_method2 = PPTMethod(
            title="科技风格PPT设计",
            content="1. 配色：蓝色、灰色为主，点缀亮色\n2. 字体：无衬线字体，如Arial、Helvetica\n3. 图表：简洁清晰，避免过度装饰\n4. 动画：简单过渡，避免花哨效果\n5. 布局：留白充足，信息层次分明"
        )
        
        session.add_all([ppt_method1, ppt_method2])
    
    if session.query(SpeechMethod).count() == 0:
        # 添加演讲稿制作方法示例
        speech_method1 = SpeechMethod(
            title="AI论文讲解演讲稿模板",
            content="1. 开场白：简短介绍论文背景和重要性\n2. 研究问题：清晰阐述论文要解决的问题\n3. 相关工作：简要回顾已有方法的优缺点\n4. 提出方法：详细解释论文的创新点\n5. 实验结果：重点展示关键结果和比较\n6. 结论与展望：总结论文贡献和未来方向\n7. 互动环节：准备可能的问答"
        )
        
        speech_method2 = SpeechMethod(
            title="技术分享演讲技巧",
            content="1. 控制节奏：保持适中的语速，重点处放慢\n2. 专业术语：首次出现时给出解释\n3. 类比解释：用生活中的例子解释复杂概念\n4. 视觉辅助：关键点配合PPT图表展示\n5. 互动设计：适时提问，保持听众注意力"
        )
        
        session.add_all([speech_method1, speech_method2])
    
    if session.query(Paper).count() == 0:
        # 添加论文示例
        paper1 = Paper(
            title="GPT-4: 大型语言模型的新突破",
            authors="OpenAI研究团队",
            abstract="这是一篇关于GPT-4的论文，介绍了其架构、训练方法和性能评估。",
            url="https://example.com/gpt4-paper",
            source="arXiv",
            published_date=datetime.datetime(2023, 3, 15)
        )
        
        paper2 = Paper(
            title="DALL-E 3: 文本到图像生成的进展",
            authors="OpenAI研究团队",
            abstract="这是一篇关于DALL-E 3的论文，介绍了其架构、训练方法和性能评估。",
            url="https://example.com/dalle3-paper",
            source="arXiv",
            published_date=datetime.datetime(2023, 4, 20)
        )
        
        paper3 = Paper(
            title="Transformer架构在自然语言处理中的应用",
            authors="Google研究团队",
            abstract="这是一篇关于Transformer架构的论文，介绍了其在自然语言处理中的应用。",
            url="https://example.com/transformer-paper",
            source="Google Scholar",
            published_date=datetime.datetime(2023, 2, 10)
        )
        
        session.add_all([paper1, paper2, paper3])
    
    if session.query(HistoryContent).count() == 0:
        # 添加历史内容示例
        history1 = HistoryContent(
            title="GPT-4论文解析",
            content_type="PPT",
            content="# GPT-4论文解析\n\n## 背景\nGPT-4是OpenAI发布的大型语言模型，相比GPT-3有显著提升。\n\n## 技术创新\n1. 更大的参数规模\n2. 改进的训练方法\n3. 更强的推理能力\n\n## 性能评估\n在多项基准测试中，GPT-4均优于GPT-3。",
            paper_id=1
        )
        
        history2 = HistoryContent(
            title="DALL-E 3技术原理",
            content_type="演讲稿",
            content="今天我们来讨论DALL-E 3的技术原理。\n\nDALL-E 3是OpenAI最新的文本到图像生成模型，它能够根据文本描述生成高质量的图像。\n\n与前代模型相比，DALL-E 3在图像质量、文本理解和创意表达方面都有显著提升。\n\n它采用了扩散模型作为基础架构，并结合了大型语言模型来增强对文本提示的理解。",
            paper_id=2
        )
        
        session.add_all([history1, history2])
    
    # 提交事务
    session.commit()
    session.close()

def get_session():
    """获取数据库会话"""
    return Session()

# 初始化数据库
if not os.path.exists(DB_PATH):
    init_db() 