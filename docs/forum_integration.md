# 论坛集成指南 | Forum Integration Guide

本文档介绍如何将唯理书院智能助手API集成到你的论坛或网站中。

This document explains how to integrate the Veritas Summer School Chatbot API into your forum or website.

## 🚀 快速开始 | Quick Start

### 1. 启动API服务器 | Start API Server

```bash
# 进入项目目录 | Navigate to project directory
cd summer-school-chatbot/src

# 启动Web API服务器 | Start web API server
python web_api.py
```

服务器将在 `http://localhost:5000` 启动。

The server will start at `http://localhost:5000`.

### 2. 测试连接 | Test Connection

访问 `http://localhost:5000` 查看测试页面，确保API正常工作。

Visit `http://localhost:5000` to see the test page and ensure the API is working.

## 📡 API接口说明 | API Endpoints

### 主要接口 | Main Endpoints

| 方法 Method | 路径 Path | 描述 Description |
|-------------|-----------|------------------|
| GET | `/` | 测试页面 Test page |
| POST | `/api/chat` | 发送消息到聊天机器人 Send message to chatbot |
| GET | `/api/status` | 检查聊天机器人状态 Check chatbot status |
| GET | `/api/stats` | 获取统计信息 Get statistics |
| POST | `/api/update` | 更新知识库 Update knowledge base |
| GET | `/api/health` | 健康检查 Health check |

### 聊天接口详情 | Chat API Details

**POST** `/api/chat`

请求格式 Request Format:
```json
{
    "message": "书院的地址在哪里？",
    "use_llm": false
}
```

响应格式 Response Format:
```json
{
    "success": true,
    "response": "书院位于上海市浦东新区申启路...",
    "timestamp": "2024-07-24T12:00:00.000Z",
    "user_message": "书院的地址在哪里？",
    "used_llm": false
}
```

## 🔧 论坛集成示例 | Forum Integration Examples

### 基础JavaScript集成 | Basic JavaScript Integration

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>论坛聊天机器人集成</title>
    <style>
        .chatbot-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            height: 500px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            flex-direction: column;
            z-index: 1000;
        }
        
        .chatbot-header {
            background: #007bff;
            color: white;
            padding: 15px;
            border-radius: 10px 10px 0 0;
            font-weight: bold;
        }
        
        .chatbot-messages {
            flex: 1;
            padding: 10px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .chatbot-input {
            display: flex;
            padding: 10px;
            border-top: 1px solid #ddd;
        }
        
        .chatbot-input input {
            flex: 1;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-right: 10px;
        }
        
        .chatbot-input button {
            padding: 8px 15px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        
        .message {
            margin-bottom: 10px;
            padding: 8px;
            border-radius: 6px;
        }
        
        .user-message {
            background: #007bff;
            color: white;
            margin-left: 20%;
            text-align: right;
        }
        
        .bot-message {
            background: white;
            border: 1px solid #ddd;
            margin-right: 20%;
        }
        
        .chatbot-toggle {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 24px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1001;
        }
    </style>
</head>
<body>
    <!-- 论坛页面内容 -->
    <div id="forum-content">
        <h1>论坛首页</h1>
        <p>这里是论坛的主要内容...</p>
    </div>

    <!-- 聊天机器人切换按钮 -->
    <button id="chatbot-toggle" class="chatbot-toggle" onclick="toggleChatbot()">🤖</button>

    <!-- 聊天机器人组件 -->
    <div id="chatbot-widget" class="chatbot-widget" style="display: none;">
        <div class="chatbot-header">
            🎓 唯理书院智能助手
            <button onclick="toggleChatbot()" style="float: right; background: none; border: none; color: white; cursor: pointer;">×</button>
        </div>
        <div id="chatbot-messages" class="chatbot-messages">
            <div class="message bot-message">
                <strong>🤖 助手:</strong> 你好！我是唯理书院智能助手。有什么可以帮助你的吗？
            </div>
        </div>
        <div class="chatbot-input">
            <input type="text" id="chatbot-input" placeholder="请输入你的问题..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">发送</button>
        </div>
    </div>

    <script>
        // 配置API地址
        const API_BASE_URL = 'http://localhost:5000';
        
        // 切换聊天机器人显示/隐藏
        function toggleChatbot() {
            const widget = document.getElementById('chatbot-widget');
            const toggle = document.getElementById('chatbot-toggle');
            
            if (widget.style.display === 'none') {
                widget.style.display = 'flex';
                toggle.style.display = 'none';
            } else {
                widget.style.display = 'none';
                toggle.style.display = 'block';
            }
        }
        
        // 处理回车键
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // 发送消息
        function sendMessage() {
            const input = document.getElementById('chatbot-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // 添加用户消息到界面
            addMessage(message, 'user');
            
            // 清空输入框
            input.value = '';
            
            // 发送到API
            fetch(`${API_BASE_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    use_llm: false
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addMessage(data.response, 'bot');
                } else {
                    addMessage('抱歉，处理您的消息时出现错误。', 'bot');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                addMessage('抱歉，网络连接出现问题。', 'bot');
            });
        }
        
        // 添加消息到聊天界面
        function addMessage(message, sender) {
            const messagesContainer = document.getElementById('chatbot-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            if (sender === 'user') {
                messageDiv.innerHTML = `<strong>👤 你:</strong> ${message}`;
            } else {
                messageDiv.innerHTML = `<strong>🤖 助手:</strong> ${message}`;
            }
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        // 页面加载时检查API状态
        window.onload = function() {
            fetch(`${API_BASE_URL}/api/status`)
                .then(response => response.json())
                .then(data => {
                    if (data.status !== 'online') {
                        console.warn('聊天机器人服务离线');
                    }
                })
                .catch(error => {
                    console.error('无法连接到聊天机器人服务:', error);
                });
        };
    </script>
</body>
</html>
```

### WordPress集成示例 | WordPress Integration

```php
<?php
// 在functions.php中添加以下代码

// 添加聊天机器人脚本到footer
function add_chatbot_scripts() {
    ?>
    <script>
        // WordPress聊天机器人集成
        (function() {
            const API_BASE_URL = 'http://your-server.com:5000'; // 替换为你的API地址
            
            // 创建聊天机器人HTML
            const chatbotHTML = `
                <div id="wp-chatbot-toggle" class="wp-chatbot-toggle">🤖</div>
                <div id="wp-chatbot-widget" class="wp-chatbot-widget" style="display: none;">
                    <div class="wp-chatbot-header">
                        🎓 唯理书院智能助手
                        <button onclick="wpToggleChatbot()">×</button>
                    </div>
                    <div id="wp-chatbot-messages" class="wp-chatbot-messages">
                        <div class="wp-message wp-bot-message">
                            <strong>🤖 助手:</strong> 你好！我是唯理书院智能助手。有什么可以帮助你的吗？
                        </div>
                    </div>
                    <div class="wp-chatbot-input">
                        <input type="text" id="wp-chatbot-input" placeholder="请输入你的问题...">
                        <button onclick="wpSendMessage()">发送</button>
                    </div>
                </div>
            `;
            
            // 添加CSS样式
            const chatbotCSS = `
                <style>
                .wp-chatbot-toggle {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    width: 60px;
                    height: 60px;
                    background: #0073aa;
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    z-index: 99999;
                    font-size: 24px;
                }
                
                .wp-chatbot-widget {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    width: 350px;
                    height: 500px;
                    background: white;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    z-index: 99999;
                    display: flex;
                    flex-direction: column;
                }
                
                .wp-chatbot-header {
                    background: #0073aa;
                    color: white;
                    padding: 15px;
                    border-radius: 10px 10px 0 0;
                }
                
                .wp-chatbot-messages {
                    flex: 1;
                    padding: 10px;
                    overflow-y: auto;
                    background: #f9f9f9;
                }
                
                .wp-message {
                    margin-bottom: 10px;
                    padding: 8px;
                    border-radius: 6px;
                }
                
                .wp-bot-message {
                    background: white;
                    border: 1px solid #ddd;
                }
                
                .wp-user-message {
                    background: #0073aa;
                    color: white;
                    margin-left: 20%;
                }
                </style>
            `;
            
            // 插入到页面
            document.body.insertAdjacentHTML('beforeend', chatbotCSS + chatbotHTML);
            
            // 全局函数
            window.wpToggleChatbot = function() {
                const widget = document.getElementById('wp-chatbot-widget');
                const toggle = document.getElementById('wp-chatbot-toggle');
                
                if (widget.style.display === 'none') {
                    widget.style.display = 'flex';
                    toggle.style.display = 'none';
                } else {
                    widget.style.display = 'none';
                    toggle.style.display = 'flex';
                }
            };
            
            window.wpSendMessage = function() {
                const input = document.getElementById('wp-chatbot-input');
                const message = input.value.trim();
                
                if (!message) return;
                
                // 添加到界面
                const messagesContainer = document.getElementById('wp-chatbot-messages');
                messagesContainer.innerHTML += `<div class="wp-message wp-user-message"><strong>👤 你:</strong> ${message}</div>`;
                
                input.value = '';
                
                // 发送到API
                fetch(`${API_BASE_URL}/api/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        use_llm: false
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        messagesContainer.innerHTML += `<div class="wp-message wp-bot-message"><strong>🤖 助手:</strong> ${data.response}</div>`;
                    } else {
                        messagesContainer.innerHTML += `<div class="wp-message wp-bot-message"><strong>🤖 助手:</strong> 抱歉，处理您的消息时出现错误。</div>`;
                    }
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                })
                .catch(error => {
                    messagesContainer.innerHTML += `<div class="wp-message wp-bot-message"><strong>🤖 助手:</strong> 抱歉，网络连接出现问题。</div>`;
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                });
            };
        })();
    </script>
    <?php
}
add_action('wp_footer', 'add_chatbot_scripts');
?>
```

### React集成示例 | React Integration

```jsx
import React, { useState, useEffect } from 'react';

const ChatbotWidget = ({ apiBaseUrl = 'http://localhost:5000' }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        { type: 'bot', content: '你好！我是唯理书院智能助手。有什么可以帮助你的吗？' }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const sendMessage = async () => {
        if (!inputValue.trim()) return;

        const userMessage = inputValue.trim();
        setInputValue('');
        
        // 添加用户消息
        setMessages(prev => [...prev, { type: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const response = await fetch(`${apiBaseUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userMessage,
                    use_llm: false
                })
            });

            const data = await response.json();
            
            if (data.success) {
                setMessages(prev => [...prev, { type: 'bot', content: data.response }]);
            } else {
                setMessages(prev => [...prev, { type: 'bot', content: '抱歉，处理您的消息时出现错误。' }]);
            }
        } catch (error) {
            setMessages(prev => [...prev, { type: 'bot', content: '抱歉，网络连接出现问题。' }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };

    return (
        <>
            {/* 切换按钮 */}
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    style={{
                        position: 'fixed',
                        bottom: '20px',
                        right: '20px',
                        width: '60px',
                        height: '60px',
                        borderRadius: '50%',
                        backgroundColor: '#007bff',
                        color: 'white',
                        border: 'none',
                        fontSize: '24px',
                        cursor: 'pointer',
                        zIndex: 1000
                    }}
                >
                    🤖
                </button>
            )}

            {/* 聊天组件 */}
            {isOpen && (
                <div style={{
                    position: 'fixed',
                    bottom: '20px',
                    right: '20px',
                    width: '350px',
                    height: '500px',
                    backgroundColor: 'white',
                    border: '1px solid #ddd',
                    borderRadius: '10px',
                    display: 'flex',
                    flexDirection: 'column',
                    zIndex: 1000
                }}>
                    {/* 头部 */}
                    <div style={{
                        backgroundColor: '#007bff',
                        color: 'white',
                        padding: '15px',
                        borderRadius: '10px 10px 0 0',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                    }}>
                        <span>🎓 唯理书院智能助手</span>
                        <button
                            onClick={() => setIsOpen(false)}
                            style={{
                                background: 'none',
                                border: 'none',
                                color: 'white',
                                fontSize: '20px',
                                cursor: 'pointer'
                            }}
                        >
                            ×
                        </button>
                    </div>

                    {/* 消息区域 */}
                    <div style={{
                        flex: 1,
                        padding: '10px',
                        overflowY: 'auto',
                        backgroundColor: '#f8f9fa'
                    }}>
                        {messages.map((message, index) => (
                            <div
                                key={index}
                                style={{
                                    marginBottom: '10px',
                                    padding: '8px',
                                    borderRadius: '6px',
                                    backgroundColor: message.type === 'user' ? '#007bff' : 'white',
                                    color: message.type === 'user' ? 'white' : '#333',
                                    marginLeft: message.type === 'user' ? '20%' : '0',
                                    marginRight: message.type === 'bot' ? '20%' : '0',
                                    border: message.type === 'bot' ? '1px solid #ddd' : 'none'
                                }}
                            >
                                <strong>{message.type === 'user' ? '👤 你:' : '🤖 助手:'}</strong> {message.content}
                            </div>
                        ))}
                        {isLoading && (
                            <div style={{ textAlign: 'center', color: '#666' }}>
                                🤖 正在思考中...
                            </div>
                        )}
                    </div>

                    {/* 输入区域 */}
                    <div style={{
                        display: 'flex',
                        padding: '10px',
                        borderTop: '1px solid #ddd'
                    }}>
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="请输入你的问题..."
                            style={{
                                flex: 1,
                                padding: '8px',
                                border: '1px solid #ddd',
                                borderRadius: '4px',
                                marginRight: '10px'
                            }}
                            disabled={isLoading}
                        />
                        <button
                            onClick={sendMessage}
                            disabled={isLoading || !inputValue.trim()}
                            style={{
                                padding: '8px 15px',
                                backgroundColor: '#007bff',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: 'pointer'
                            }}
                        >
                            发送
                        </button>
                    </div>
                </div>
            )}
        </>
    );
};

export default ChatbotWidget;
```

## 🔧 配置说明 | Configuration

### 环境变量 | Environment Variables

```bash
# API服务器配置
API_HOST=0.0.0.0          # 服务器监听地址
API_PORT=5000             # 服务器端口
API_DEBUG=false           # 调试模式

# 聊天机器人配置
GOOGLE_DRIVE_CREDENTIALS_FILE=config/google_drive_credentials.json
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
DEFAULT_LLM_PROVIDER=openai
```

### 生产环境部署 | Production Deployment

```bash
# 使用gunicorn部署
pip install gunicorn

# 启动生产服务器
gunicorn --bind 0.0.0.0:5000 --workers 4 web_api:app

# 或使用docker (如果有Dockerfile)
docker build -t chatbot-api .
docker run -p 5000:5000 chatbot-api
```

## 🛡️ 安全建议 | Security Recommendations

1. **CORS配置**: 在生产环境中限制CORS来源
2. **认证**: 为API添加认证机制
3. **速率限制**: 防止API滥用
4. **HTTPS**: 在生产环境中使用HTTPS
5. **防火墙**: 只开放必要的端口

## 📞 技术支持 | Technical Support

如有集成问题，请参考：
For integration issues, please refer to:

- 📖 [README.md](../README.md) - 项目主文档 Main documentation
- ⚡ [QUICK_START.md](../QUICK_START.md) - 快速开始指南 Quick start guide
- 🧪 测试页面 Test page: `http://localhost:5000`

## 📝 更新日志 | Changelog

- **v1.0** - 初始API版本 Initial API version
- **v1.1** - 添加中文支持 Added Chinese support
- **v1.2** - 增强错误处理 Enhanced error handling 