# 论坛聊天机器人集成示例 | Forum Chatbot Integration Examples

本目录包含了如何将唯理书院智能助手集成到论坛或网站中的示例。

This directory contains examples of how to integrate the Veritas Summer School Chatbot into forums or websites.

## 📁 文件说明 | File Description

### `forum_widget.html`
完整的论坛集成示例，包含：
- 🎨 **美观的UI设计** - 现代化的聊天界面
- 🧪 **测试功能** - 内置测试按钮，方便快速测试
- 📱 **响应式设计** - 支持桌面和移动设备
- 🔄 **状态监控** - 实时显示聊天机器人连接状态
- ⌨️ **键盘快捷键** - Ctrl+Shift+C 快速切换

A complete forum integration example including:
- 🎨 **Beautiful UI Design** - Modern chat interface
- 🧪 **Test Features** - Built-in test buttons for quick testing
- 📱 **Responsive Design** - Desktop and mobile support
- 🔄 **Status Monitoring** - Real-time chatbot connection status
- ⌨️ **Keyboard Shortcuts** - Ctrl+Shift+C for quick toggle

## 🚀 快速开始 | Quick Start

### 1. 测试HTML文件 | Test HTML File

```bash
# 运行测试脚本 | Run test script
python test_widget.py

# 或者直接在浏览器中打开 | Or open directly in browser
open examples/forum_widget.html
```

### 2. 启动API服务器 | Start API Server

```bash
# 启动聊天机器人API服务器 | Start chatbot API server
python run_server.py

# 如果端口5000被占用，使用其他端口 | If port 5000 is in use, use another port
API_PORT=5001 python run_server.py
```

### 3. 完整测试 | Full Testing

1. **启动服务器** | **Start Server**：
   ```bash
   python run_server.py
   ```

2. **打开测试页面** | **Open Test Page**：
   - 访问 `http://localhost:5000` (API内置测试页面)
   - 或运行 `python test_widget.py` (独立测试)

3. **测试功能** | **Test Features**：
   - 点击右下角🤖图标打开聊天窗口
   - 使用测试按钮发送预设问题
   - 手动输入问题测试

## 🔧 自定义配置 | Customization

### 修改API地址 | Change API URL

在 `forum_widget.html` 中找到配置部分：
In `forum_widget.html`, find the configuration section:

```javascript
const CONFIG = {
    apiBaseUrl: 'http://localhost:5000',  // 修改为你的API服务器地址
    maxRetries: 3,
    retryDelay: 1000
};
```

### 自定义样式 | Custom Styling

主要CSS类名：
Main CSS classes:

- `.chatbot-toggle` - 聊天机器人切换按钮
- `.chatbot-widget` - 聊天窗口主体
- `.chatbot-header` - 聊天窗口头部
- `.chatbot-messages` - 消息显示区域
- `.chatbot-input` - 输入区域

### 修改测试问题 | Modify Test Questions

在HTML中找到测试按钮部分：
Find the test buttons section in HTML:

```html
<button class="test-btn" onclick="testQuestion('你的问题')">按钮文字</button>
```

## 📱 集成到论坛 | Forum Integration

### 基本集成步骤 | Basic Integration Steps

1. **复制CSS和JavaScript** | **Copy CSS and JavaScript**
   - 从 `forum_widget.html` 复制样式和脚本代码
   - 根据论坛主题调整颜色和样式

2. **添加HTML结构** | **Add HTML Structure**
   ```html
   <!-- 聊天机器人切换按钮 -->
   <button id="chatbot-toggle" class="chatbot-toggle" onclick="toggleChatbot()">🤖</button>
   
   <!-- 聊天机器人组件 -->
   <div id="chatbot-widget" class="chatbot-widget" style="display: none;">
       <!-- 聊天窗口内容 -->
   </div>
   ```

3. **配置API地址** | **Configure API URL**
   - 修改 `CONFIG.apiBaseUrl` 为你的服务器地址
   - 确保CORS配置正确

### 不同平台集成 | Platform-Specific Integration

#### WordPress
```php
// 在 functions.php 中添加
function add_chatbot_widget() {
    // 添加聊天机器人代码
}
add_action('wp_footer', 'add_chatbot_widget');
```

#### Discourse
在管理面板中添加自定义HTML/CSS

#### Vanilla Forums
通过主题自定义功能添加

## 🐛 故障排除 | Troubleshooting

### 常见问题 | Common Issues

1. **聊天机器人显示离线** | **Chatbot Shows Offline**
   - 检查API服务器是否运行
   - 确认API地址配置正确
   - 查看浏览器控制台错误信息

2. **无法发送消息** | **Cannot Send Messages**
   - 检查网络连接
   - 确认API服务器响应正常
   - 检查CORS配置

3. **样式显示异常** | **Style Display Issues**
   - 检查CSS文件加载
   - 确认无CSS冲突
   - 调整z-index值

### 调试方法 | Debugging Methods

1. **浏览器控制台** | **Browser Console**
   - 按F12打开开发者工具
   - 查看Console标签页的错误信息
   - 检查Network标签页的API请求

2. **API测试** | **API Testing**
   ```bash
   # 测试API健康状态
   curl http://localhost:5000/api/health
   
   # 测试聊天接口
   curl -X POST http://localhost:5000/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "你好", "use_llm": false}'
   ```

## 📞 技术支持 | Technical Support

如有问题，请参考：
For issues, please refer to:

- 📖 [主文档](../README.md) - 项目主要文档
- 📚 [集成指南](../docs/forum_integration.md) - 详细集成文档
- 🧪 测试脚本：`python test_widget.py`
- 🔗 API测试页面：`http://localhost:5000`

## 📝 更新日志 | Changelog

- **v1.2** - 添加测试模式和调试功能
- **v1.1** - 增强错误处理和状态监控
- **v1.0** - 初始版本 