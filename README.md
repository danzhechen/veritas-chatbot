# Summer School Chatbot 🤖 | 唯理暑期书院智能助手

An intelligent chatbot for summer school programs that can answer questions about school information, schedules, policies, and more. The chatbot uses Google Drive as a knowledge base and integrates with multiple LLM providers for intelligent responses.

一个专为暑期书院项目设计的智能聊天机器人，可以回答关于学校信息、日程安排、政策等各类问题。机器人使用Google Drive作为知识库，并集成多个LLM提供商以提供智能响应。

## 🚀 Features | 特性

- **📚 Google Drive Integration**: Automatically syncs with Google Drive documents | **Google Drive集成**：自动同步Google Drive文档
- **🧠 Multiple LLM Support**: Works with OpenAI, Anthropic, Google AI, and more | **多LLM支持**：支持OpenAI、Anthropic、Google AI等
- **🔍 Enhanced Chinese Search**: Optimized for Chinese text processing and search | **增强中文搜索**：针对中文文本处理和搜索进行优化
- **💬 Intelligent Q&A**: Context-aware responses with semantic understanding | **智能问答**：具有语义理解的上下文感知响应
- **📱 CLI Interface**: Easy-to-use command-line interface for testing | **CLI界面**：易于使用的命令行界面用于测试
- **🔧 Modular Design**: Extensible architecture for different interfaces | **模块化设计**：可扩展架构支持不同界面

## 📁 Project Structure | 项目结构

```
summer-school-chatbot/
├── src/                          # Core application code | 核心应用代码
│   ├── chatbot_engine.py        # Main chatbot logic | 主聊天机器人逻辑
│   ├── knowledge_base.py        # Enhanced knowledge management | 增强知识管理
│   ├── drive_connector.py       # Google Drive integration | Google Drive集成
│   └── cli_interface.py         # Command-line interface | 命令行界面
├── config/                       # Configuration files | 配置文件
│   ├── config.env.example       # Configuration template | 配置模板
│   └── google_drive_credentials.json.example  # Credentials template | 凭证模板
├── data/                         # Data storage | 数据存储
│   └── knowledge_base.json      # Local knowledge base | 本地知识库
├── tests/                        # Unit tests | 单元测试
├── docs/                         # Documentation | 文档
├── requirements.txt             # Python dependencies | Python依赖
├── README.md                    # This file | 本文件
├── QUICK_START.md              # Quick start guide | 快速开始指南
└── .gitignore                  # Git ignore rules | Git忽略规则
```

## 🛠️ Setup Instructions | 安装说明

### 1. Prerequisites | 前置要求

- Python 3.8 or higher | Python 3.8或更高版本
- A Google Cloud Project (for Google Drive API) | Google Cloud项目（用于Google Drive API）
- LLM API keys (OpenAI, Anthropic, or Google AI) | LLM API密钥（OpenAI、Anthropic或Google AI）

### 2. Installation | 安装

```bash
# Clone the repository | 克隆仓库
git clone <repository-url>
cd summer-school-chatbot

# Create virtual environment | 创建虚拟环境
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies | 安装依赖
pip install -r requirements.txt

# Or use the setup script | 或者使用安装脚本
python setup.py
```

### 3. Google Drive API Setup | Google Drive API设置

1. **Create a Google Cloud Project** | **创建Google Cloud项目**: Go to [Google Cloud Console](https://console.cloud.google.com/)
2. **Enable Google Drive API** | **启用Google Drive API**: In APIs & Services → Library
3. **Create Service Account** | **创建服务账户**: In IAM & Admin → Service Accounts
4. **Download JSON Key** | **下载JSON密钥**: Create and download the service account key
5. **Copy credentials** | **复制凭证**: Place the JSON file as `config/google_drive_credentials.json`

### 4. Configuration | 配置

```bash
# Copy configuration template | 复制配置模板
cp config/config.env.example config.env

# Edit configuration file | 编辑配置文件
nano config.env  # Add your API keys and folder IDs | 添加你的API密钥和文件夹ID
```

### 5. Run the Chatbot | 运行聊天机器人

#### CLI Interface | 命令行界面
```bash
# Navigate to src directory | 进入src目录
cd src

# Start CLI interface | 启动CLI界面
python cli_interface.py

# Or run directly | 或直接运行
python -c "from chatbot_engine import SummerSchoolChatbot; bot = SummerSchoolChatbot(); print(bot.ask('你好'))"
```

#### Web API for Forum Integration | 论坛集成Web API
```bash
# Start web API server | 启动Web API服务器
python run_server.py

# Or start from src directory | 或从src目录启动
cd src && python web_api.py

# Server will be available at | 服务器地址
# http://localhost:5000
```

## 🎯 Usage Examples | 使用示例

### CLI Commands | CLI命令

```bash
# Ask questions in Chinese | 用中文提问
> 书院的地址在哪里？
> 我需要准备什么床上用品？
> 晚间活动是强制参加的吗？

# English questions also supported | 也支持英语提问
> Where is the school located?
> What should I bring?

# Commands | 命令
> help / 帮助          # Show help | 显示帮助
> stats / 统计         # Show statistics | 显示统计
> history / 历史       # Show history | 显示历史
> update / 更新        # Update from Google Drive | 从Google Drive更新
> quit / 退出          # Exit | 退出
```

### Programmatic Usage | 编程使用

```python
from chatbot_engine import SummerSchoolChatbot

# Initialize chatbot | 初始化聊天机器人
chatbot = SummerSchoolChatbot()

# Ask questions in Chinese | 用中文提问
response = chatbot.ask("书院的举办地址在哪里？")
print(response)

# Ask questions in English | 用英语提问
response = chatbot.ask("Where is the summer school located?")
print(response)

# Update from Google Drive | 从Google Drive更新
chatbot.update_from_drive()
```

## 🇨🇳 Chinese Language Support | 中文语言支持

This chatbot is specifically optimized for Chinese students with:

本聊天机器人专为中国学生优化，具有以下特性：

- **🔤 Bilingual Interface**: Supports both Chinese and English commands | **双语界面**：支持中英文命令
- **🧠 Chinese NLP**: Advanced Chinese text processing and keyword extraction | **中文NLP**：高级中文文本处理和关键词提取
- **🎯 Intent Recognition**: Understands Chinese question patterns | **意图识别**：理解中文问题模式
- **📚 Semantic Mapping**: Chinese-English keyword mapping for better search | **语义映射**：中英文关键词映射以提升搜索效果

### Sample Chinese Questions | 中文问题示例

```
书院的地址在哪里？               # Where is the college located?
我需要自己买床垫吗？             # Do I need to buy my own mattress?
晚间活动可以不参加吗？           # Can I skip evening activities?
书院行为不当的定义是什么？       # What is the definition of misconduct?
如何邮寄物品到学校？             # How to mail items to school?
```

## 🚀 Key Algorithm Optimizations | 核心算法优化

The chatbot features an enhanced search algorithm optimized for Chinese text:

聊天机器人采用针对中文文本优化的增强搜索算法：

- **🇨🇳 Chinese Text Processing**: Advanced segmentation and keyword extraction | **中文文本处理**：高级分词和关键词提取
- **🧠 Semantic Mapping**: Context-aware keyword expansion | **语义映射**：上下文感知的关键词扩展
- **🎯 Intent Recognition**: Automatic question type detection | **意图识别**：自动问题类型检测
- **📊 Enhanced Scoring**: Multi-factor relevance scoring (up to 3.0) | **增强评分**：多因子相关性评分（最高3.0）
- **📝 Smart Excerpts**: Intelligent content extraction | **智能摘录**：智能内容提取

## 🔒 Security Notes | 安全说明

**⚠️ Important | 重要**: This project contains sensitive configuration files that should NOT be shared:

本项目包含不应共享的敏感配置文件：

- `config.env` - Contains API keys | 包含API密钥
- `config/google_drive_credentials.json` - Contains Google service account credentials | 包含Google服务账户凭证

These files are excluded from version control via `.gitignore`. Always use the `.example` files as templates.

这些文件通过`.gitignore`从版本控制中排除。请始终使用`.example`文件作为模板。

## 🧪 Testing | 测试

```bash
# Run unit tests | 运行单元测试
python -m pytest tests/

# Test with Chinese questions | 用中文问题测试
python cli_interface.py --test

# Test specific functionality | 测试特定功能
python tests/test_chatbot.py
```

## 📚 Documentation | 文档

- [`QUICK_START.md`](QUICK_START.md) - Quick start guide | 快速开始指南
- [`docs/`](docs/) - Detailed documentation | 详细文档
- API documentation in source code docstrings | 源代码docstrings中的API文档

## 🤝 Contributing | 贡献

1. Fork the repository | Fork仓库
2. Create a feature branch | 创建功能分支
3. Make your changes | 进行更改
4. Add tests for new functionality | 为新功能添加测试
5. Submit a pull request | 提交pull request

## 📄 License | 许可证

This project is licensed under the MIT License - see the LICENSE file for details.

本项目采用MIT许可证 - 详见LICENSE文件。

## 🆘 Support | 支持

For questions or issues | 如有问题：
1. Check the documentation in `docs/` | 查看`docs/`中的文档
2. Review existing issues | 查看现有issues
3. Create a new issue with detailed information | 创建包含详细信息的新issue

## 🔄 Version History | 版本历史

- **v1.2** - Enhanced Chinese search algorithm | 增强中文搜索算法
- **v1.1** - Google Drive integration | Google Drive集成
- **v1.0** - Initial release with basic chatbot functionality | 初始版本基础聊天功能 