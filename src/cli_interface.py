#!/usr/bin/env python3
"""
暑期书院聊天机器人命令行界面

此模块提供了一个简单的CLI来测试和与聊天机器人交互。
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

from chatbot_engine import SummerSchoolChatbot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment():
    """设置聊天机器人环境。"""
    # Load environment variables
    env_file = Path('../config.env.example')
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
        logger.info("从 config.env.example 加载环境变量")

def print_banner():
    """打印聊天机器人横幅。"""
    print("=" * 60)
    print("🎓 唯理暑期书院智能助手")
    print("=" * 60)
    print("欢迎来到唯理书院！我可以回答关于暑期项目的任何问题。")
    print("输入 'help' 查看命令，输入 'quit' 退出。")
    print("=" * 60)

def print_help():
    """打印帮助信息。"""
    print("\n📚 可用命令：")
    print("  help                    - 显示此帮助信息")
    print("  stats                   - 显示聊天机器人统计信息")
    print("  history                 - 显示对话历史")
    print("  clear                   - 清除对话历史")
    print("  update                  - 从Google Drive更新")
    print("  add_faq                 - 添加新的常见问题")
    print("  add_location            - 添加位置信息")
    print("  add_schedule            - 添加日程信息")
    print("  quit/exit               - 退出聊天机器人")
    print("\n💡 示例问题：")
    print("  - 书院的地址在哪里？")
    print("  - 书院的日程安排是什么？")
    print("  - 我需要准备什么床上用品？")
    print("  - 晚间活动是强制参加的吗？")
    print("  - 如何邮寄物品到学校？")

def add_faq_interactive(chatbot):
    """交互式FAQ添加。"""
    print("\n📝 添加新的常见问题")
    print("-" * 30)
    
    category = input("分类 (例如：general, registration, schedule): ").strip()
    question = input("问题: ").strip()
    answer = input("答案: ").strip()
    keywords = input("关键词 (用逗号分隔，可选): ").strip()
    
    if category and question and answer:
        keyword_list = [k.strip() for k in keywords.split(',')] if keywords else None
        chatbot.add_faq(category, question, answer, keyword_list)
        print("✅ FAQ添加成功！")
    else:
        print("❌ 请提供分类、问题和答案。")

def add_location_interactive(chatbot):
    """交互式位置添加。"""
    print("\n📍 添加位置信息")
    print("-" * 30)
    
    name = input("位置名称: ").strip()
    address = input("地址: ").strip()
    details = input("其他详情 (可选): ").strip()
    
    if name and address:
        details_dict = {'details': details} if details else None
        chatbot.add_location(name, address, details_dict)
        print("✅ 位置信息添加成功！")
    else:
        print("❌ 请提供位置名称和地址。")

def add_schedule_interactive(chatbot):
    """交互式日程添加。"""
    print("\n📅 添加日程信息")
    print("-" * 30)
    
    event_name = input("活动名称: ").strip()
    date = input("日期 (YYYY-MM-DD): ").strip()
    time = input("时间 (HH:MM): ").strip()
    details = input("其他详情 (可选): ").strip()
    
    if event_name and date and time:
        details_dict = {'details': details} if details else None
        chatbot.add_schedule(event_name, date, time, details_dict)
        print("✅ 日程信息添加成功！")
    else:
        print("❌ 请提供活动名称、日期和时间。")

def show_statistics(chatbot):
    """显示聊天机器人统计信息。"""
    stats = chatbot.get_statistics()
    
    print("\n📊 聊天机器人统计信息")
    print("-" * 30)
    print(f"知识库：")
    print(f"  文档: {stats['knowledge_base']['documents']}")
    print(f"  常见问题: {stats['knowledge_base']['faqs']}")
    print(f"  位置信息: {stats['knowledge_base']['locations']}")
    print(f"  日程安排: {stats['knowledge_base']['schedules']}")
    if 'conversation_history' in stats:
        print(f"  对话记录: {stats['conversation_history']}")
    if 'last_updated' in stats['knowledge_base']:
        print(f"  最后更新: {stats['knowledge_base']['last_updated']}")

def show_history(chatbot):
    """显示对话历史。"""
    history = chatbot.get_conversation_history()
    
    if not history:
        print("\n📝 暂无对话历史")
        return
    
    print(f"\n📝 对话历史 ({len(history)} 条记录)")
    print("-" * 50)
    
    for i, entry in enumerate(history[-10:], 1):  # Show last 10 entries
        role = "👤 用户" if entry['role'] == 'user' else "🤖 助手"
        content = entry['content'][:100] + "..." if len(entry['content']) > 100 else entry['content']
        timestamp = entry.get('timestamp', 'Unknown')
        print(f"{i}. {role}: {content}")
        print(f"   时间: {timestamp}")
        print()

def main():
    """主函数。"""
    parser = argparse.ArgumentParser(description='唯理暑期书院聊天机器人')
    parser.add_argument('--no-llm', action='store_true', help='禁用LLM响应')
    parser.add_argument('--test', action='store_true', help='运行测试问题')
    args = parser.parse_args()
    
    # Set up environment
    setup_environment()
    
    # Initialize chatbot
    try:
        chatbot = SummerSchoolChatbot()
        print("✅ 聊天机器人初始化成功！")
    except Exception as e:
        print(f"❌ 聊天机器人初始化失败: {e}")
        return
    
    # Run test mode if requested
    if args.test:
        print("\n🧪 运行测试模式")
        print("-" * 30)
        
        test_questions = [
            "你好！",
            "书院的地址在哪里？",
            "书院的日程安排是什么？",
            "我需要准备什么床上用品？",
            "晚间活动是强制参加的吗？",
            "如何邮寄物品到学校？",
            "谢谢！"
        ]
        
        for question in test_questions:
            print(f"\n👤 用户: {question}")
            response = chatbot.ask(question, use_llm=not args.no_llm)
            print(f"🤖 助手: {response}")
        
        show_statistics(chatbot)
        return
    
    # Interactive mode
    print_banner()
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 你: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q', '退出', '再见']:
                print("👋 再见！感谢使用唯理书院智能助手！")
                break
            elif user_input.lower() in ['help', '帮助']:
                print_help()
                continue
            elif user_input.lower() in ['stats', '统计']:
                show_statistics(chatbot)
                continue
            elif user_input.lower() in ['history', '历史']:
                show_history(chatbot)
                continue
            elif user_input.lower() in ['clear', '清除']:
                chatbot.clear_conversation_history()
                print("✅ 对话历史已清除！")
                continue
            elif user_input.lower() in ['update', '更新']:
                print("🔄 正在从Google Drive更新...")
                success = chatbot.update_from_drive()
                if success:
                    print("✅ 成功从Google Drive更新！")
                else:
                    print("❌ 从Google Drive更新失败。")
                continue
            elif user_input.lower() == 'add_faq':
                add_faq_interactive(chatbot)
                continue
            elif user_input.lower() == 'add_location':
                add_location_interactive(chatbot)
                continue
            elif user_input.lower() == 'add_schedule':
                add_schedule_interactive(chatbot)
                continue
            
            # Process regular question
            print("🤖 助手: ", end="")
            response = chatbot.ask(user_input, use_llm=not args.no_llm)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！感谢使用唯理书院智能助手！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            logger.error(f"主循环错误: {e}")

if __name__ == "__main__":
    main() 