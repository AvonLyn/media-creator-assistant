#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - arXiv爬虫模块
"""

import requests
import datetime
import time
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
from app.data.database import Paper, get_session

class ArxivCrawler:
    """arXiv爬虫类"""
    
    def __init__(self):
        """初始化爬虫"""
        self.base_url = "http://export.arxiv.org/api/query"
        self.session = get_session()
        self.is_running = False
        self.progress_callback = None
    
    def set_progress_callback(self, callback):
        """设置进度回调函数"""
        self.progress_callback = callback
    
    def crawl(self, keywords, date=None, max_results=10):
        """爬取论文
        
        Args:
            keywords (str): 关键词，多个关键词用逗号分隔
            date (datetime.date, optional): 发布日期
            max_results (int, optional): 最大结果数
            
        Returns:
            list: 爬取到的论文列表
        """
        self.is_running = True
        papers = []
        
        # 处理关键词
        search_query = " OR ".join([f"all:{kw.strip()}" for kw in keywords.split(",")])
        
        # 处理日期
        if date:
            date_str = date.strftime("%Y%m%d")
            search_query = f"{search_query} AND submittedDate:[{date_str}000000 TO {date_str}235959]"
        
        # 构造请求参数
        params = {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }
        
        try:
            # 发送请求
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            # 解析XML响应
            root = ET.fromstring(response.content)
            
            # 命名空间
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "arxiv": "http://arxiv.org/schemas/atom"
            }
            
            # 获取论文条目
            entries = root.findall(".//atom:entry", ns)
            
            for i, entry in enumerate(entries):
                # 检查是否停止爬取
                if not self.is_running:
                    break
                
                # 获取标题
                title_elem = entry.find("atom:title", ns)
                title = title_elem.text.strip() if title_elem is not None else ""
                
                # 获取作者
                authors_elem = entry.findall("atom:author/atom:name", ns)
                authors = ", ".join([author.text for author in authors_elem]) if authors_elem else ""
                
                # 获取摘要
                summary_elem = entry.find("atom:summary", ns)
                abstract = summary_elem.text.strip() if summary_elem is not None else ""
                
                # 获取链接
                link_elem = entry.find("atom:link[@title='pdf']", ns)
                url = link_elem.get("href") if link_elem is not None else ""
                
                # 获取发布日期
                published_elem = entry.find("atom:published", ns)
                published_date = None
                if published_elem is not None:
                    try:
                        published_date = datetime.datetime.strptime(published_elem.text, "%Y-%m-%dT%H:%M:%SZ")
                    except ValueError:
                        pass
                
                # 创建论文对象
                paper = Paper(
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    url=url,
                    source="arXiv",
                    published_date=published_date
                )
                
                # 添加到列表
                papers.append(paper)
                
                # 更新进度
                if self.progress_callback:
                    progress = int((i + 1) / len(entries) * 100)
                    self.progress_callback(progress)
                
                # 防止请求过快
                time.sleep(0.5)
            
            # 保存到数据库
            if papers and self.is_running:
                self.session.add_all(papers)
                self.session.commit()
            
        except Exception as e:
            print(f"爬取arXiv论文时出错: {str(e)}")
        finally:
            self.is_running = False
        
        return papers
    
    def stop(self):
        """停止爬取"""
        self.is_running = False
    
    def __del__(self):
        """析构函数"""
        self.session.close() 