# 自媒体博主自动化辅助平台

## 项目简介

自媒体博主自动化辅助平台是一款为AI领域自媒体博主设计的Windows本地应用，旨在帮助内容创作者更高效地生成基于AI论文的讲解视频所需的PPT和演讲稿。通过爬取最新AI论文、分析过往内容，并结合大模型进行内容生成，实现智能化的内容生产。

## 核心功能

1. **论文爬取**：定期爬取当日热门AI论文，并进行预处理
2. **知识库管理**：存储PPT制作方法、演讲稿制作方法和以往内容
3. **RAG（检索增强生成）**：根据任务需求提取合适的制作方法，分析过往文稿风格
4. **内容生成**：调用大模型API，自动生成符合风格的PPT和演讲稿

## 安装步骤

1. 克隆仓库到本地
```
git clone https://github.com/yourusername/media-creator-assistant.git
cd media-creator-assistant
```

2. 安装依赖
```
pip install -r requirements.txt
```

3. 配置环境变量
创建`.env`文件，并添加以下内容：
```
OPENAI_API_KEY=your_openai_api_key
```

4. 运行应用
```
python run.py
```

## 使用方法

1. 启动应用后，在主界面选择需要的功能
2. 论文爬取：选择论文源，设置爬取参数，开始爬取
3. 知识库管理：上传或编辑PPT和演讲稿制作方法，管理历史内容
4. 内容生成：选择论文，设置生成参数，生成PPT和演讲稿

## 项目结构

```
app/
├── core/           # 核心功能模块
│   ├── crawler/    # 论文爬取模块
│   ├── knowledge/  # 知识库管理模块
│   ├── rag/        # RAG处理模块
│   └── generator/  # 内容生成模块
├── gui/            # GUI界面模块
├── data/           # 数据存储目录
└── utils/          # 工具函数
```

## 技术栈

- GUI框架：PyQt5
- 后端：Python (FastAPI)
- 数据库：SQLite
- 爬虫：Scrapy, Playwright
- 自然语言处理：LangChain, Sentence-Transformers
- LLM API：OpenAI API

## 贡献指南

欢迎贡献代码或提出建议！请先fork本仓库，然后提交pull request。

## 许可证

MIT 