#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - 嵌入向量管理模块
"""

import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from app.data.database import PPTMethod, SpeechMethod, HistoryContent, Paper, get_session

class EmbeddingManager:
    """嵌入向量管理类"""
    
    def __init__(self):
        """初始化嵌入向量管理器"""
        self.session = get_session()
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # 嵌入向量存储路径
        self.embedding_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
            'app', 'data', 'embeddings'
        )
        
        # 创建存储目录
        os.makedirs(self.embedding_dir, exist_ok=True)
        
        # 嵌入向量文件路径
        self.ppt_methods_embedding_path = os.path.join(self.embedding_dir, 'ppt_methods_embeddings.json')
        self.speech_methods_embedding_path = os.path.join(self.embedding_dir, 'speech_methods_embeddings.json')
        self.history_contents_embedding_path = os.path.join(self.embedding_dir, 'history_contents_embeddings.json')
        self.papers_embedding_path = os.path.join(self.embedding_dir, 'papers_embeddings.json')
        
        # 加载嵌入向量
        self.ppt_methods_embeddings = self._load_embeddings(self.ppt_methods_embedding_path)
        self.speech_methods_embeddings = self._load_embeddings(self.speech_methods_embedding_path)
        self.history_contents_embeddings = self._load_embeddings(self.history_contents_embedding_path)
        self.papers_embeddings = self._load_embeddings(self.papers_embedding_path)
    
    def _load_embeddings(self, path):
        """加载嵌入向量
        
        Args:
            path (str): 嵌入向量文件路径
            
        Returns:
            dict: 嵌入向量字典
        """
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载嵌入向量时出错: {str(e)}")
        
        return {}
    
    def _save_embeddings(self, embeddings, path):
        """保存嵌入向量
        
        Args:
            embeddings (dict): 嵌入向量字典
            path (str): 嵌入向量文件路径
        """
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(embeddings, f, ensure_ascii=False)
        except Exception as e:
            print(f"保存嵌入向量时出错: {str(e)}")
    
    def _compute_embedding(self, text):
        """计算文本的嵌入向量
        
        Args:
            text (str): 文本
            
        Returns:
            list: 嵌入向量
        """
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    def _cosine_similarity(self, vec1, vec2):
        """计算余弦相似度
        
        Args:
            vec1 (list): 向量1
            vec2 (list): 向量2
            
        Returns:
            float: 余弦相似度
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def update_ppt_methods_embeddings(self):
        """更新PPT制作方法的嵌入向量"""
        methods = self.session.query(PPTMethod).all()
        embeddings = {}
        
        for method in methods:
            text = f"{method.title}\n{method.content}"
            embeddings[str(method.id)] = {
                "title": method.title,
                "embedding": self._compute_embedding(text)
            }
        
        self.ppt_methods_embeddings = embeddings
        self._save_embeddings(embeddings, self.ppt_methods_embedding_path)
    
    def update_speech_methods_embeddings(self):
        """更新演讲稿制作方法的嵌入向量"""
        methods = self.session.query(SpeechMethod).all()
        embeddings = {}
        
        for method in methods:
            text = f"{method.title}\n{method.content}"
            embeddings[str(method.id)] = {
                "title": method.title,
                "embedding": self._compute_embedding(text)
            }
        
        self.speech_methods_embeddings = embeddings
        self._save_embeddings(embeddings, self.speech_methods_embedding_path)
    
    def update_history_contents_embeddings(self):
        """更新历史内容的嵌入向量"""
        contents = self.session.query(HistoryContent).all()
        embeddings = {}
        
        for content in contents:
            text = f"{content.title}\n{content.content}"
            embeddings[str(content.id)] = {
                "title": content.title,
                "content_type": content.content_type,
                "paper_id": content.paper_id,
                "embedding": self._compute_embedding(text)
            }
        
        self.history_contents_embeddings = embeddings
        self._save_embeddings(embeddings, self.history_contents_embedding_path)
    
    def update_papers_embeddings(self):
        """更新论文的嵌入向量"""
        papers = self.session.query(Paper).all()
        embeddings = {}
        
        for paper in papers:
            text = f"{paper.title}\n{paper.abstract}"
            embeddings[str(paper.id)] = {
                "title": paper.title,
                "embedding": self._compute_embedding(text)
            }
        
        self.papers_embeddings = embeddings
        self._save_embeddings(embeddings, self.papers_embedding_path)
    
    def update_all_embeddings(self):
        """更新所有嵌入向量"""
        self.update_ppt_methods_embeddings()
        self.update_speech_methods_embeddings()
        self.update_history_contents_embeddings()
        self.update_papers_embeddings()
    
    def search_ppt_methods(self, query, top_k=3):
        """搜索PPT制作方法
        
        Args:
            query (str): 查询文本
            top_k (int, optional): 返回结果数量
            
        Returns:
            list: 相似度最高的PPT制作方法列表
        """
        query_embedding = self._compute_embedding(query)
        results = []
        
        for method_id, data in self.ppt_methods_embeddings.items():
            similarity = self._cosine_similarity(query_embedding, data["embedding"])
            results.append({
                "id": int(method_id),
                "title": data["title"],
                "similarity": similarity
            })
        
        # 按相似度降序排序
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # 获取相似度最高的方法
        top_results = results[:top_k]
        
        # 获取完整的方法对象
        method_ids = [result["id"] for result in top_results]
        methods = self.session.query(PPTMethod).filter(PPTMethod.id.in_(method_ids)).all()
        
        # 按相似度排序
        methods_dict = {method.id: method for method in methods}
        sorted_methods = [methods_dict[result["id"]] for result in top_results if result["id"] in methods_dict]
        
        return sorted_methods
    
    def search_speech_methods(self, query, top_k=3):
        """搜索演讲稿制作方法
        
        Args:
            query (str): 查询文本
            top_k (int, optional): 返回结果数量
            
        Returns:
            list: 相似度最高的演讲稿制作方法列表
        """
        query_embedding = self._compute_embedding(query)
        results = []
        
        for method_id, data in self.speech_methods_embeddings.items():
            similarity = self._cosine_similarity(query_embedding, data["embedding"])
            results.append({
                "id": int(method_id),
                "title": data["title"],
                "similarity": similarity
            })
        
        # 按相似度降序排序
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # 获取相似度最高的方法
        top_results = results[:top_k]
        
        # 获取完整的方法对象
        method_ids = [result["id"] for result in top_results]
        methods = self.session.query(SpeechMethod).filter(SpeechMethod.id.in_(method_ids)).all()
        
        # 按相似度排序
        methods_dict = {method.id: method for method in methods}
        sorted_methods = [methods_dict[result["id"]] for result in top_results if result["id"] in methods_dict]
        
        return sorted_methods
    
    def search_history_contents(self, query, content_type=None, top_k=3):
        """搜索历史内容
        
        Args:
            query (str): 查询文本
            content_type (str, optional): 内容类型，如"PPT"或"演讲稿"
            top_k (int, optional): 返回结果数量
            
        Returns:
            list: 相似度最高的历史内容列表
        """
        query_embedding = self._compute_embedding(query)
        results = []
        
        for content_id, data in self.history_contents_embeddings.items():
            # 如果指定了内容类型，则只搜索该类型的内容
            if content_type and data["content_type"] != content_type:
                continue
            
            similarity = self._cosine_similarity(query_embedding, data["embedding"])
            results.append({
                "id": int(content_id),
                "title": data["title"],
                "content_type": data["content_type"],
                "similarity": similarity
            })
        
        # 按相似度降序排序
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # 获取相似度最高的内容
        top_results = results[:top_k]
        
        # 获取完整的内容对象
        content_ids = [result["id"] for result in top_results]
        contents = self.session.query(HistoryContent).filter(HistoryContent.id.in_(content_ids)).all()
        
        # 按相似度排序
        contents_dict = {content.id: content for content in contents}
        sorted_contents = [contents_dict[result["id"]] for result in top_results if result["id"] in contents_dict]
        
        return sorted_contents
    
    def search_papers(self, query, top_k=3):
        """搜索论文
        
        Args:
            query (str): 查询文本
            top_k (int, optional): 返回结果数量
            
        Returns:
            list: 相似度最高的论文列表
        """
        query_embedding = self._compute_embedding(query)
        results = []
        
        for paper_id, data in self.papers_embeddings.items():
            similarity = self._cosine_similarity(query_embedding, data["embedding"])
            results.append({
                "id": int(paper_id),
                "title": data["title"],
                "similarity": similarity
            })
        
        # 按相似度降序排序
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # 获取相似度最高的论文
        top_results = results[:top_k]
        
        # 获取完整的论文对象
        paper_ids = [result["id"] for result in top_results]
        papers = self.session.query(Paper).filter(Paper.id.in_(paper_ids)).all()
        
        # 按相似度排序
        papers_dict = {paper.id: paper for paper in papers}
        sorted_papers = [papers_dict[result["id"]] for result in top_results if result["id"] in papers_dict]
        
        return sorted_papers
    
    def __del__(self):
        """析构函数"""
        self.session.close() 