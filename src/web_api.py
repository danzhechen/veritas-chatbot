#!/usr/bin/env python3
"""
唯理书院聊天机器人 Web API

提供HTTP接口，方便在论坛或网站上集成聊天机器人功能。
"""

import os
import sys
import logging
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime

# Add the parent directory to the path to import modules
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

from chatbot_engine import SummerSchoolChatbot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Global chatbot instance
chatbot = None

def initialize_chatbot():
    """初始化聊天机器人"""
    global chatbot
    try:
        chatbot = SummerSchoolChatbot()
        logger.info("✅ 聊天机器人初始化成功")
        return True
    except Exception as e:
        logger.error(f"❌ 聊天机器人初始化失败: {e}")
        return False

# HTML template for testing the API
TEST_PAGE_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>唯理书院智能助手 - 测试页面</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        .chat-container {
            border: 1px solid #ddd;
            border-radius: 8px;
            height: 400px;
            overflow-y: auto;
            padding: 15px;
            margin-bottom: 20px;
            background-color: #fafafa;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
        }
        .user-message {
            background-color: #007bff;
            color: white;
            text-align: right;
            margin-left: 20%;
        }
        .bot-message {
            background-color: #e9ecef;
            color: #333;
            margin-right: 20%;
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        .input-field {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
        }
        .send-button {
            padding: 12px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }
        .send-button:hover {
            background-color: #0056b3;
        }
        .send-button:disabled {
            background-color: #6c757d;
            cursor: not-allowed;
        }
        .status {
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 6px;
        }
        .status.online {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.offline {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .api-info {
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
            font-size: 12px;
            color: #1565c0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 唯理书院智能助手</h1>
            <p>测试页面 - Web API接口演示</p>
        </div>
        
        <div id="status" class="status offline">
            🔄 正在连接聊天机器人...
        </div>
        
        <div id="chatContainer" class="chat-container">
            <div class="message bot-message">
                <strong>🤖 助手:</strong> 你好！我是唯理书院智能助手。有什么可以帮助你的吗？
            </div>
        </div>
        
        <div class="input-group">
            <input type="text" id="messageInput" class="input-field" 
                   placeholder="请输入你的问题..." 
                   onkeypress="handleKeyPress(event)">
            <button id="sendButton" class="send-button" onclick="sendMessage()">
                发送
            </button>
        </div>
        
        <div class="api-info">
            <strong>📡 API接口信息:</strong><br>
            • POST /api/chat - 发送消息到聊天机器人<br>
            • GET /api/status - 检查聊天机器人状态<br>
            • GET /api/stats - 获取统计信息<br>
            • GET / - 此测试页面
        </div>
    </div>

    <script>
        let isOnline = false;
        
        // Check chatbot status on page load
        window.onload = function() {
            checkStatus();
        };
        
        function checkStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const statusDiv = document.getElementById('status');
                    if (data.status === 'online') {
                        statusDiv.className = 'status online';
                        statusDiv.innerHTML = '✅ 聊天机器人在线';
                        isOnline = true;
                    } else {
                        statusDiv.className = 'status offline';
                        statusDiv.innerHTML = '❌ 聊天机器人离线';
                        isOnline = false;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    const statusDiv = document.getElementById('status');
                    statusDiv.className = 'status offline';
                    statusDiv.innerHTML = '❌ 连接失败';
                });
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function sendMessage() {
            if (!isOnline) {
                alert('聊天机器人当前离线，请稍后再试。');
                return;
            }
            
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            
            // Clear input and disable button
            input.value = '';
            const sendButton = document.getElementById('sendButton');
            sendButton.disabled = true;
            sendButton.textContent = '发送中...';
            
            // Send to API
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    use_llm: false  // Set to true if you want LLM responses
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
            })
            .finally(() => {
                sendButton.disabled = false;
                sendButton.textContent = '发送';
            });
        }
        
        function addMessage(message, sender) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            
            if (sender === 'user') {
                messageDiv.className = 'message user-message';
                messageDiv.innerHTML = `<strong>👤 你:</strong> ${message}`;
            } else {
                messageDiv.className = 'message bot-message';
                messageDiv.innerHTML = `<strong>🤖 助手:</strong> ${message}`;
            }
            
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def test_page():
    """测试页面"""
    return render_template_string(TEST_PAGE_HTML)

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取聊天机器人状态"""
    global chatbot
    
    status = {
        'status': 'online' if chatbot else 'offline',
        'timestamp': datetime.now().isoformat(),
        'message': '聊天机器人运行正常' if chatbot else '聊天机器人未初始化'
    }
    
    return jsonify(status)

@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天接口"""
    global chatbot
    
    if not chatbot:
        return jsonify({
            'success': False,
            'error': '聊天机器人未初始化',
            'message': 'Chatbot not initialized'
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': '无效的请求格式',
                'message': 'Invalid request format'
            }), 400
        
        user_message = data['message'].strip()
        use_llm = data.get('use_llm', False)
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': '消息不能为空',
                'message': 'Message cannot be empty'
            }), 400
        
        # Generate response
        response = chatbot.ask(user_message, use_llm=use_llm)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'used_llm': use_llm
        })
        
    except Exception as e:
        logger.error(f"Chat API error: {e}")
        return jsonify({
            'success': False,
            'error': '处理消息时出现错误',
            'message': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    global chatbot
    
    if not chatbot:
        return jsonify({
            'success': False,
            'error': '聊天机器人未初始化'
        }), 500
    
    try:
        stats = chatbot.get_statistics()
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Stats API error: {e}")
        return jsonify({
            'success': False,
            'error': '获取统计信息时出现错误',
            'message': str(e)
        }), 500

@app.route('/api/update', methods=['POST'])
def update_knowledge():
    """更新知识库"""
    global chatbot
    
    if not chatbot:
        return jsonify({
            'success': False,
            'error': '聊天机器人未初始化'
        }), 500
    
    try:
        success = chatbot.update_from_drive()
        return jsonify({
            'success': success,
            'message': '知识库更新成功' if success else '知识库更新失败',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Update API error: {e}")
        return jsonify({
            'success': False,
            'error': '更新知识库时出现错误',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': '唯理书院智能助手 API',
        'version': '1.0'
    })

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'error': '接口不存在',
        'message': 'API endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'success': False,
        'error': '服务器内部错误',
        'message': 'Internal server error'
    }), 500

def main():
    """主函数"""
    print("🚀 启动唯理书院智能助手 Web API")
    print("=" * 50)
    
    # Initialize chatbot
    if not initialize_chatbot():
        print("❌ 无法启动：聊天机器人初始化失败")
        return
    
    # Get configuration
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('API_DEBUG', 'false').lower() == 'true'
    
    print(f"🌐 服务器地址: http://{host}:{port}")
    print(f"📱 测试页面: http://{host}:{port}/")
    print(f"📡 API文档:")
    print(f"   POST http://{host}:{port}/api/chat")
    print(f"   GET  http://{host}:{port}/api/status")
    print(f"   GET  http://{host}:{port}/api/stats")
    print("=" * 50)
    
    # Start server
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")

if __name__ == '__main__':
    main() 