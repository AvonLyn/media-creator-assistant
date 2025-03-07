#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - 爬虫管理器模块
"""

from app.core.crawler.arxiv_crawler import ArxivCrawler
from app.data.database import Paper, get_session
import datetime
import threading

class CrawlerManager:
    """爬虫管理器类"""
    
    def __init__(self):
        """初始化爬虫管理器"""
        self.arxiv_crawler = ArxivCrawler()
        self.session = get_session()
        self.current_crawler = None
        self.crawl_thread = None
    
    def set_progress_callback(self, callback):
        """设置进度回调函数"""
        self.arxiv_crawler.set_progress_callback(callback)
    
    def start_crawl(self, source, keywords, date=None, max_results=10, callback=None):
        """开始爬取论文
        
        Args:
            source (str): 论文源，如"arXiv"
            keywords (str): 关键词，多个关键词用逗号分隔
            date (datetime.date, optional): 发布日期
            max_results (int, optional): 最大结果数
            callback (function, optional): 完成回调函数
            
        Returns:
            bool: 是否成功启动爬取
        """
        # 检查是否已有爬虫在运行
        if self.crawl_thread and self.crawl_thread.is_alive():
            return False
        
        # 根据源选择爬虫
        if source.lower() == "arxiv":
            self.current_crawler = self.arxiv_crawler
        else:
            # 暂不支持其他源
            return False
        
        # 创建并启动爬虫线程
        self.crawl_thread = threading.Thread(
            target=self._crawl_thread,
            args=(source, keywords, date, max_results, callback)
        )
        self.crawl_thread.daemon = True
        self.crawl_thread.start()
        
        return True
    
    def _crawl_thread(self, source, keywords, date, max_results, callback):
        """爬虫线程函数"""
        papers = []
        
        try:
            # 调用爬虫
            if source.lower() == "arxiv":
                papers = self.arxiv_crawler.crawl(keywords, date, max_results)
        except Exception as e:
            print(f"爬虫线程出错: {str(e)}")
        
        # 调用回调函数
        if callback:
            callback(papers)
    
    def stop_crawl(self):
        """停止爬取"""
        if self.current_crawler:
            self.current_crawler.stop()
    
    def get_papers(self, source=None, keywords=None, date=None, limit=100):
        """获取已爬取的论文
        
        Args:
            source (str, optional): 论文源
            keywords (str, optional): 关键词
            date (datetime.date, optional): 发布日期
            limit (int, optional): 最大结果数
            
        Returns:
            list: 论文列表
        """
        query = self.session.query(Paper)
        
        # 筛选条件
        if source:
            query = query.filter(Paper.source == source)
        
        if keywords:
            # 分割关键词
            for keyword in keywords.split(","):
                keyword = keyword.strip()
                query = query.filter(
                    (Paper.title.like(f"%{keyword}%")) | 
                    (Paper.abstract.like(f"%{keyword}%"))
                )
        
        if date:
            # 转换为datetime
            start_date = datetime.datetime.combine(date, datetime.time.min)
            end_date = datetime.datetime.combine(date, datetime.time.max)
            query = query.filter(Paper.published_date.between(start_date, end_date))
        
        # 按爬取日期降序排序
        query = query.order_by(Paper.crawled_date.desc())
        
        # 限制结果数
        query = query.limit(limit)
        
        return query.all()
    
    def get_paper_by_id(self, paper_id):
        """根据ID获取论文
        
        Args:
            paper_id (int): 论文ID
            
        Returns:
            Paper: 论文对象
        """
        return self.session.query(Paper).filter(Paper.id == paper_id).first()
    
    def get_paper_by_title(self, title):
        """根据标题获取论文
        
        Args:
            title (str): 论文标题
            
        Returns:
            Paper: 论文对象
        """
        return self.session.query(Paper).filter(Paper.title == title).first()
    
    def __del__(self):
        """析构函数"""
        self.session.close() 