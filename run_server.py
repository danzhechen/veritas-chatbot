#!/usr/bin/env python3
"""
启动唯理书院智能助手Web API服务器

Simple server runner for the chatbot web API
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(current_dir.parent))

def main():
    """启动Web API服务器"""
    print("🚀 启动唯理书院智能助手Web API")
    print("=" * 60)
    
    try:
        # Change to src directory
        os.chdir(src_dir)
        
        # Import and run the web API
        from web_api import main as web_main
        web_main()
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装所有依赖包:")
        print("  pip install -r requirements.txt")
        return 1
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 