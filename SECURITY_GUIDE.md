# 🔒 隐私安全指南 | Privacy & Security Guide

在将此项目上传到GitHub之前，请仔细阅读此安全指南以确保隐私信息得到保护。

Before uploading this project to GitHub, please carefully read this security guide to ensure privacy information is protected.

## ✅ 安全检查清单 | Security Checklist

### 🔍 **运行隐私检查** | **Run Privacy Check**

```bash
# 扫描整个项目
python privacy_check.py

# 只检查即将提交的文件
python privacy_check.py --staged

# 生成详细报告
python privacy_check.py --report privacy_report.json
```

### 📁 **已保护的敏感文件** | **Protected Sensitive Files**

以下类型的文件已通过 `.gitignore` 自动排除：

The following types of files are automatically excluded via `.gitignore`:

```
🔑 API密钥和凭证 | API Keys & Credentials
├── config.env                          # 实际配置文件
├── .env, .env.local, .env.production   # 环境变量文件
├── *credentials*.json                  # 凭证文件
├── *api_key*, *secret*, *token*        # 密钥文件
└── *.pem, *.key, *.crt                # 证书文件

📊 数据和日志 | Data & Logs
├── data/downloaded_documents/          # 下载的文档
├── data/temp/, data/cache/            # 临时和缓存数据
├── logs/, *.log                       # 日志文件
├── user_data/, personal_data/         # 用户个人数据
└── conversations/, history/           # 对话历史

🛠️ 开发文件 | Development Files
├── token.json                         # OAuth令牌
├── test_data/, mock_data/             # 测试数据
└── *_secret.yaml                      # 部署密钥
```

### ✅ **安全的示例文件** | **Safe Example Files**

这些文件是安全的，包含在版本控制中：

These files are safe and included in version control:

- ✅ `config/config.env.example` - 配置模板
- ✅ `config/google_drive_credentials.json.example` - 凭证模板
- ✅ 所有源代码 (.py文件) - 不包含硬编码密钥
- ✅ 文档文件 (.md文件)
- ✅ 测试脚本和示例

## 🚨 **需要手动检查的项目** | **Items to Manually Check**

### 1. **环境变量** | **Environment Variables**

确认以下文件不存在或已在 `.gitignore` 中：

Confirm the following files don't exist or are in `.gitignore`:

```bash
# 检查是否存在敏感配置文件
ls -la config.env 2>/dev/null && echo "⚠️ config.env exists!" || echo "✅ config.env not found"
ls -la .env 2>/dev/null && echo "⚠️ .env exists!" || echo "✅ .env not found"
ls -la config/google_drive_credentials.json 2>/dev/null && echo "⚠️ credentials file exists!" || echo "✅ credentials file not found"
```

### 2. **代码中的硬编码信息** | **Hardcoded Information in Code**

搜索可能的硬编码敏感信息：

Search for potentially hardcoded sensitive information:

```bash
# 搜索可能的API密钥
grep -r "sk-[a-zA-Z0-9]" src/ || echo "✅ No OpenAI keys found"
grep -r "AIza[a-zA-Z0-9]" src/ || echo "✅ No Google API keys found"

# 搜索邮箱地址
grep -r "@gmail\|@outlook\|@qq" src/ || echo "✅ No email addresses found"
```

### 3. **Git历史清理** | **Git History Cleanup**

如果之前意外提交了敏感信息：

If sensitive information was previously committed accidentally:

```bash
# 查看提交历史
git log --oneline

# 如需清理历史（谨慎使用）
# git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch path/to/sensitive/file' --prune-empty --tag-name-filter cat -- --all
```

## 🛡️ **最佳实践** | **Best Practices**

### 📝 **配置管理** | **Configuration Management**

1. **使用环境变量**：
   ```python
   # ✅ 正确方式
   api_key = os.getenv('OPENAI_API_KEY')
   
   # ❌ 错误方式
   api_key = "sk-your-api-key-placeholder"
   ```

2. **使用模板文件**：
   - 创建 `.example` 文件作为模板
   - 在实际文件中填入真实值
   - 只提交模板文件到版本控制

### 🔑 **密钥管理** | **Key Management**

1. **本地开发**：
   ```bash
   # 使用 .env 文件（已在.gitignore中）
   echo "OPENAI_API_KEY=your-key-here" > .env
   ```

2. **生产部署**：
   - 使用云服务的密钥管理（AWS Secrets Manager, Azure Key Vault等）
   - 使用环境变量注入
   - 绝不在代码中硬编码

### 📊 **数据保护** | **Data Protection**

1. **测试数据**：
   - 使用虚拟或匿名化数据
   - 避免使用真实用户数据进行测试

2. **日志文件**：
   - 不记录敏感信息
   - 定期清理日志文件

## 🔧 **自动化工具** | **Automation Tools**

### Git Hooks

设置预提交钩子自动检查：

Set up pre-commit hooks for automatic checking:

```bash
# 创建 .git/hooks/pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "🔒 Running privacy check..."
python privacy_check.py --staged --strict
if [ $? -ne 0 ]; then
    echo "❌ Privacy check failed! Commit aborted."
    exit 1
fi
echo "✅ Privacy check passed!"
EOF

chmod +x .git/hooks/pre-commit
```

### CI/CD集成

在GitHub Actions中添加隐私检查：

Add privacy checks to GitHub Actions:

```yaml
# .github/workflows/security-check.yml
name: Security Check
on: [push, pull_request]
jobs:
  privacy-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run Privacy Check
      run: python privacy_check.py --strict
```

## 📋 **提交前检查表** | **Pre-Commit Checklist**

在每次提交前，请确认：

Before each commit, please confirm:

- [ ] ✅ 运行了 `python privacy_check.py`
- [ ] ✅ 没有 `.env` 或 `config.env` 文件在版本控制中
- [ ] ✅ 没有真实的 API 密钥在代码中
- [ ] ✅ 没有个人信息（邮箱、电话等）在文件中
- [ ] ✅ 测试数据是匿名化的
- [ ] ✅ 日志文件已清理或排除
- [ ] ✅ 凭证文件在 `.gitignore` 中

## 🆘 **紧急情况处理** | **Emergency Response**

如果意外提交了敏感信息：

If sensitive information was accidentally committed:

### 1. **立即撤销** | **Immediate Revocation**
```bash
# 撤销最后一次提交（本地）
git reset --hard HEAD~1

# 如果已推送到远程
git revert HEAD
git push
```

### 2. **更换密钥** | **Rotate Keys**
- 立即更换所有泄露的API密钥
- 撤销相关的访问令牌
- 更新所有使用该密钥的服务

### 3. **清理历史** | **Clean History**
```bash
# 使用 git filter-branch 清理历史（谨慎使用）
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch config.env' --prune-empty --tag-name-filter cat -- --all

# 强制推送（会覆盖远程历史）
git push --force-with-lease
```

## 📞 **联系方式** | **Contact**

如有安全相关问题：

For security-related questions:

- 📧 项目维护者
- 🐛 GitHub Issues (用于一般性安全建议)
- 🔒 私密漏洞报告请直接联系维护者

---

**记住：隐私安全是每个人的责任！** | **Remember: Privacy and security are everyone's responsibility!**

🎯 **最终目标**：确保项目可以安全地公开分享，不泄露任何个人或敏感信息。 