# 🎨 AI Voice Painter (AI 语音绘图助手)

> 一款**零外设、全双工、基于 RAG 架构**的纯语音控制智能绘图系统。只需一句“你好小智”，即可让大模型化身为你的神笔马良。

## ✨ 核心特性 (Features)

- 🎙️ **真正的“零外设”交互**
  前端内置有限状态机（FSM），支持“你好小智”唤醒词持续静默监听与自动静音防回音，首次授权后彻底解放双手。
- 🧠 **组件化 RAG 驱动引擎**
  摒弃传统生硬的全局像素坐标预测。系统挂载了 `0-100` 相对坐标系的组件知识库（内置 50+ 日常高频事物）。大模型作为“空间规划师”，实现复杂概念的降维拆解与动态拼装。
- ⚡ **极速毫秒级渲染响应**
  采用“语义拆解 + 矢量绘制”双轨架构，配合极速文本大模型，告别传统 Diffusion 模型生图的漫长等待。话音刚落，画面即达。
- 💾 **上下文滑动窗口记忆**
  后端基于 MySQL 与 SQLAlchemy 实现轻量级会话状态持久化，完美支持多轮连续的局部修改与叠加绘图指令。

---

## 🛠️ 技术栈 (Tech Stack)

- **后端服务**: Python 3.9+, FastAPI, Uvicorn
- **AI 与大模型**: LangChain, 阿里云百炼 API (推荐使用 `qwen-turbo-latest`)
- **数据持久化**: MySQL 8.0, SQLAlchemy, PyMySQL
- **前端与渲染**: HTML5 Canvas, Web Speech API (识别+合成), Vanilla JavaScript

---

## 📁 项目目录结构

```text
AI_Painter/
├── agent/
│   └── core.py             # 核心 Agent：集成 LangChain、RAG 与状态更新
├── config/
│   ├── agent.yml           # 大模型 Prompt 与模型参数配置
│   └── db.yml              # MySQL 数据库连接配置
├── data/
│   └── components.json     # RAG 图形组件知识库 (核心数据资产)
├── frontend/
│   └── index.html          # 前端单页面应用 (语音交互引擎 + Canvas 渲染器)
├── models/
│   └── models.py           # SQLAlchemy 数据表 ORM 模型 (画布状态表)
├── schemas/
│   └── payload.py          # FastAPI 接口 Pydantic 校验数据模型
├── utils/
│   ├── config_handler.py   # YAML 配置解析工具
│   ├── database.py         # 数据库连接池与 Session 管理
│   ├── llm_factory.py      # 大模型单例实例化工厂
│   ├── path_tool.py        # 全局绝对路径管理
│   └── rag_retriever.py    # 内存级轻量 RAG 语义检索器
├── main.py                 # FastAPI 服务启动入口
└── requirements.txt        # Python 依赖清单
```

---

## 🚀 快速启动 (Quick Start)

### 1. 环境准备
请确保本机已安装 `Python 3.9+` 和 `MySQL 8.0+`，并使用最新版 Chrome 或 Edge 浏览器。

### 2. 安装依赖
克隆项目后，在项目根目录下打开终端，执行以下命令安装核心依赖包：

```bash
pip install -r requirements.txt
```

### 3. 配置数据库与环境变量
1. **配置 MySQL**：打开 `config/db.yml`，修改 `user`、`password` 为你本地的数据库账号密码。请提前在 MySQL 中创建一个名为 `ai_painter_db` 的空数据库（系统启动时会自动建表）。
2. **配置大模型 API Key**：在系统环境变量中配置您的阿里云 DashScope API Key。
   - **Windows**: `setx DASHSCOPE_API_KEY "你的_API_KEY"`
   - **Mac/Linux**: `export DASHSCOPE_API_KEY="你的_API_KEY"`

### 4. 启动后端服务
在项目根目录下运行主程序：

```bash
python main.py
```

*当终端出现 `Uvicorn running on http://127.0.0.1:8000` 提示时，说明后端已成功启动。*

---

## 🎮 使用指南 (Usage)

1. **打开界面**：直接在文件管理器中找到 `frontend/index.html`，双击用浏览器打开。
2. **破冰授权**：点击页面上的绿色按钮“🟢 引擎已自动启动，待唤醒”，允许浏览器使用麦克风权限。
3. **彻底脱手**：放下鼠标，对着麦克风说出唤醒词：**“你好小智”**。
4. **下达指令**：听到“我在呢，请吩咐”后，立刻下达你的绘图指令。例如：
   > *"在画布左边画一棵树，右边画一座带红屋顶的房子，天上画一个太阳。"*


