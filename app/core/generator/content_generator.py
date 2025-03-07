#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自媒体博主自动化辅助平台 - 内容生成模块
"""

import os
import json
import time
import threading
from openai import OpenAI
from app.core.rag.embedding_manager import EmbeddingManager
from app.core.knowledge.knowledge_manager import KnowledgeManager
from app.data.database import Paper, HistoryContent, get_session

class ContentGenerator:
    """内容生成类"""
    
    def __init__(self):
        """初始化内容生成器"""
        self.session = get_session()
        self.embedding_manager = EmbeddingManager()
        self.knowledge_manager = KnowledgeManager()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.is_generating = False
        self.progress_callback = None
        self.generation_thread = None
    
    def set_progress_callback(self, callback):
        """设置进度回调函数"""
        self.progress_callback = callback
    
    def generate_content(self, paper_info, settings, callback=None):
        """生成内容
        
        Args:
            paper_info (dict): 论文信息，包含title和abstract
            settings (dict): 生成设置，包含generate_ppt, generate_speech, style, model, temperature等
            callback (function, optional): 完成回调函数
            
        Returns:
            bool: 是否成功启动生成
        """
        # 检查是否已有生成任务在运行
        if self.is_generating:
            return False
        
        # 创建并启动生成线程
        self.generation_thread = threading.Thread(
            target=self._generate_thread,
            args=(paper_info, settings, callback)
        )
        self.generation_thread.daemon = True
        self.generation_thread.start()
        
        return True
    
    def _generate_thread(self, paper_info, settings, callback):
        """生成线程函数"""
        self.is_generating = True
        results = {"ppt": None, "speech": None}
        
        try:
            # 更新进度
            if self.progress_callback:
                self.progress_callback(10)
            
            # 获取相关的PPT制作方法
            ppt_methods = []
            if settings["generate_ppt"]:
                ppt_methods = self.embedding_manager.search_ppt_methods(paper_info["title"], top_k=2)
            
            # 获取相关的演讲稿制作方法
            speech_methods = []
            if settings["generate_speech"]:
                speech_methods = self.embedding_manager.search_speech_methods(paper_info["title"], top_k=2)
            
            # 获取相关的历史内容
            history_contents = self.embedding_manager.search_history_contents(paper_info["title"], top_k=3)
            
            # 更新进度
            if self.progress_callback:
                self.progress_callback(20)
            
            # 生成PPT内容
            if settings["generate_ppt"]:
                ppt_content = self._generate_ppt(paper_info, settings, ppt_methods, history_contents)
                results["ppt"] = ppt_content
            
            # 更新进度
            if self.progress_callback:
                self.progress_callback(60)
            
            # 生成演讲稿内容
            if settings["generate_speech"]:
                speech_content = self._generate_speech(paper_info, settings, speech_methods, history_contents)
                results["speech"] = speech_content
            
            # 更新进度
            if self.progress_callback:
                self.progress_callback(100)
            
            # 保存到历史内容
            self._save_to_history(paper_info, results)
            
        except Exception as e:
            print(f"生成内容时出错: {str(e)}")
        finally:
            self.is_generating = False
        
        # 调用回调函数
        if callback:
            callback(results)
    
    def _generate_ppt(self, paper_info, settings, ppt_methods, history_contents):
        """生成PPT内容
        
        Args:
            paper_info (dict): 论文信息
            settings (dict): 生成设置
            ppt_methods (list): PPT制作方法列表
            history_contents (list): 历史内容列表
            
        Returns:
            str: 生成的PPT内容
        """
        # 构建提示词
        prompt = self._build_ppt_prompt(paper_info, settings, ppt_methods, history_contents)
        
        # 调用大模型API
        response = self._call_llm_api(prompt, settings)
        
        return response
    
    def _generate_speech(self, paper_info, settings, speech_methods, history_contents):
        """生成演讲稿内容
        
        Args:
            paper_info (dict): 论文信息
            settings (dict): 生成设置
            speech_methods (list): 演讲稿制作方法列表
            history_contents (list): 历史内容列表
            
        Returns:
            str: 生成的演讲稿内容
        """
        # 构建提示词
        prompt = self._build_speech_prompt(paper_info, settings, speech_methods, history_contents)
        
        # 调用大模型API
        response = self._call_llm_api(prompt, settings)
        
        return response
    
    def _build_ppt_prompt(self, paper_info, settings, ppt_methods, history_contents):
        """构建PPT生成提示词
        
        Args:
            paper_info (dict): 论文信息
            settings (dict): 生成设置
            ppt_methods (list): PPT制作方法列表
            history_contents (list): 历史内容列表
            
        Returns:
            str: 提示词
        """
        prompt = f"""请为以下AI论文生成一份详细的PPT大纲：

论文标题：{paper_info['title']}
论文摘要：{paper_info['abstract']}

"""
        
        # 添加PPT制作方法
        if ppt_methods:
            prompt += "参考以下PPT制作方法：\n\n"
            for method in ppt_methods:
                prompt += f"方法：{method.title}\n{method.content}\n\n"
        
        # 添加历史内容参考
        ppt_history = [content for content in history_contents if content.content_type == "PPT"]
        if ppt_history:
            prompt += "参考以下历史PPT内容风格：\n\n"
            for content in ppt_history[:1]:  # 只取一个最相关的
                prompt += f"标题：{content.title}\n{content.content}\n\n"
        
        # 添加风格要求
        prompt += f"风格要求：{settings['style']}\n"
        if settings["style"] == "自定义" and "custom_style" in settings:
            prompt += f"自定义风格描述：{settings['custom_style']}\n"
        
        prompt += """
请按照以下格式生成PPT大纲：

# 论文标题

## 第1页：标题
- 标题：...
- 作者：...
- 日期：...

## 第2页：摘要
- ...

## 第3页：研究背景
- ...

...（其他页面）

请确保内容全面、结构清晰，适合用于讲解AI论文。
"""
        
        return prompt
    
    def _build_speech_prompt(self, paper_info, settings, speech_methods, history_contents):
        """构建演讲稿生成提示词
        
        Args:
            paper_info (dict): 论文信息
            settings (dict): 生成设置
            speech_methods (list): 演讲稿制作方法列表
            history_contents (list): 历史内容列表
            
        Returns:
            str: 提示词
        """
        prompt = f"""请为以下AI论文生成一份详细的演讲稿：

论文标题：{paper_info['title']}
论文摘要：{paper_info['abstract']}

"""
        
        # 添加演讲稿制作方法
        if speech_methods:
            prompt += "参考以下演讲稿制作方法：\n\n"
            for method in speech_methods:
                prompt += f"方法：{method.title}\n{method.content}\n\n"
        
        # 添加历史内容参考
        speech_history = [content for content in history_contents if content.content_type == "演讲稿"]
        if speech_history:
            prompt += "参考以下历史演讲稿内容风格：\n\n"
            for content in speech_history[:1]:  # 只取一个最相关的
                prompt += f"标题：{content.title}\n{content.content}\n\n"
        
        # 添加风格要求
        prompt += f"风格要求：{settings['style']}\n"
        if settings["style"] == "自定义" and "custom_style" in settings:
            prompt += f"自定义风格描述：{settings['custom_style']}\n"
        
        prompt += """
请生成一份完整的演讲稿，包括开场白、主体内容和结束语。演讲稿应该清晰地解释论文的核心内容，使听众能够理解论文的创新点和价值。

请确保演讲稿语言流畅、逻辑清晰，适合口头表达。
"""
        
        return prompt
    
    def _call_llm_api(self, prompt, settings):
        """调用大模型API
        
        Args:
            prompt (str): 提示词
            settings (dict): 生成设置
            
        Returns:
            str: 生成的内容
        """
        try:
            # 根据设置选择模型
            model = "gpt-4"
            if settings["model"] == "Claude":
                # 这里需要替换为实际的Claude API调用
                return self._simulate_generation()
            elif settings["model"] == "Gemini":
                # 这里需要替换为实际的Gemini API调用
                return self._simulate_generation()
            elif settings["model"] == "自定义API":
                # 这里需要实现自定义API的调用
                return self._simulate_generation()
            
            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个专业的AI论文解读助手，擅长生成高质量的PPT大纲和演讲稿。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings["temperature"]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"调用大模型API时出错: {str(e)}")
            # 出错时返回模拟生成的内容
            return self._simulate_generation()
    
    def _simulate_generation(self):
        """模拟生成内容（仅用于演示）"""
        # 随机等待一段时间，模拟生成过程
        time.sleep(2)
        
        # 返回模拟生成的内容
        return """# GPT-4: 大型语言模型的新突破

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
    
    def _save_to_history(self, paper_info, results):
        """保存生成结果到历史内容
        
        Args:
            paper_info (dict): 论文信息
            results (dict): 生成结果
        """
        # 获取论文ID
        paper = None
        if "id" in paper_info:
            paper = self.session.query(Paper).filter(Paper.id == paper_info["id"]).first()
        else:
            paper = self.session.query(Paper).filter(Paper.title == paper_info["title"]).first()
        
        paper_id = paper.id if paper else None
        
        # 保存PPT内容
        if results["ppt"]:
            self.knowledge_manager.add_history_content(
                title=f"{paper_info['title']} - PPT",
                content_type="PPT",
                content=results["ppt"],
                paper_id=paper_id
            )
        
        # 保存演讲稿内容
        if results["speech"]:
            self.knowledge_manager.add_history_content(
                title=f"{paper_info['title']} - 演讲稿",
                content_type="演讲稿",
                content=results["speech"],
                paper_id=paper_id
            )
    
    def cancel_generation(self):
        """取消生成"""
        self.is_generating = False
    
    def __del__(self):
        """析构函数"""
        self.session.close() 