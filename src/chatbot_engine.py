#!/usr/bin/env python3
"""
Summer School Chatbot Engine

This module provides the main chatbot functionality, integrating
LLM responses with knowledge base and Google Drive information.
"""

import os
import logging
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
import sys

# Add the parent directory to the path to import tools
sys.path.append(str(Path(__file__).parent.parent.parent))

from drive_connector import GoogleDriveConnector
from knowledge_base import KnowledgeBase

# Import LLM tools from existing tools directory
try:
    from tools.llm_api import query_llm
except ImportError:
    print("Warning: LLM API tools not available. Install dependencies first.")
    query_llm = None

logger = logging.getLogger(__name__)

class SummerSchoolChatbot:
    """Main chatbot class that integrates all components."""
    
    def __init__(self, 
                 llm_provider: str = None,
                 knowledge_base_path: str = None,
                 drive_credentials: str = None,
                 drive_folder_id: str = None):
        """
        Initialize the summer school chatbot.
        
        Args:
            llm_provider: LLM provider to use (openai, anthropic, google_ai)
            knowledge_base_path: Path to knowledge base data
            drive_credentials: Path to Google Drive credentials
            drive_folder_id: Google Drive folder ID
        """
        self.llm_provider = llm_provider or os.getenv('DEFAULT_LLM_PROVIDER', 'openai')
        kb_path = knowledge_base_path or os.getenv('KNOWLEDGE_BASE_PATH', 'data/knowledge_base.json')
        self.knowledge_base = KnowledgeBase(kb_path)
        self.drive_connector = None
        self.conversation_history = []
        
        # Initialize Google Drive connector if credentials are available
        if drive_credentials or os.getenv('GOOGLE_DRIVE_CREDENTIALS_FILE'):
            try:
                self.drive_connector = GoogleDriveConnector(
                    credentials_file=drive_credentials,
                    folder_id=drive_folder_id
                )
                logger.info("Google Drive connector initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Drive connector: {e}")
        
        # Load default responses
        self._load_default_responses()
        
        logger.info(f"Summer School Chatbot initialized with LLM provider: {self.llm_provider}")
    
    def _load_default_responses(self) -> None:
        """加载常见问题的默认响应。"""
        self.default_responses = {
            'greeting': [
                "你好！我是唯理书院智能助手。有什么可以帮助你的吗？",
                "欢迎来到唯理书院！我可以回答关于暑期项目的任何问题。",
                "你好！我是书院的AI助手，有什么想了解的吗？"
            ],
            'farewell': [
                "感谢使用唯理书院智能助手。祝你度过美好的一天！",
                "再见！如果还有问题随时可以来询问。",
                "回头见！有任何疑问都可以再来找我。"
            ],
            'unknown': [
                "抱歉，我还不太确定这个问题。你可以换个方式问问吗？",
                "我暂时没有这方面的信息。你可以询问关于课程安排、地点或住宿等问题。",
                "我还在学习这个话题。有其他我可以帮助你的吗？"
            ]
        }
    
    def ask(self, question: str, use_llm: bool = True) -> str:
        """
        处理用户问题并返回响应。
        
        Args:
            question: 用户问题
            use_llm: 是否使用LLM生成响应
            
        Returns:
            生成的响应
        """
        # Add to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': question,
            'timestamp': self._get_timestamp()
        })
        
        # Check for greetings and farewells
        if self._is_greeting(question):
            response = self._get_random_response('greeting')
        elif self._is_farewell(question):
            response = self._get_random_response('farewell')
        else:
            # Search knowledge base
            kb_results = self.knowledge_base.search(question, max_results=3)
            
            if kb_results and kb_results[0]['score'] > 0.5:
                # Use knowledge base result
                response = self._format_kb_response(kb_results[0])
            elif use_llm and query_llm:
                # Try LLM response with context
                response = self._generate_llm_response(question, kb_results)
            else:
                # Default fallback
                response = self._get_random_response('unknown')
        
        # Add response to conversation history
        self.conversation_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': self._get_timestamp()
        })
        
        return response
    
    def _is_greeting(self, text: str) -> bool:
        """检查文本是否为问候语。"""
        greetings = [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
            '你好', '您好', '嗨', '早上好', '下午好', '晚上好', '晚安'
        ]
        return any(greeting in text.lower() for greeting in greetings)
    
    def _is_farewell(self, text: str) -> bool:
        """检查文本是否为告别语。"""
        farewells = [
            'goodbye', 'bye', 'see you', 'thank you', 'thanks',
            '再见', '拜拜', '谢谢', '感谢', '回头见', '下次见'
        ]
        return any(farewell in text.lower() for farewell in farewells)
    
    def _get_random_response(self, category: str) -> str:
        """Get a random response from the specified category."""
        import random
        responses = self.default_responses.get(category, self.default_responses['unknown'])
        return random.choice(responses)
    
    def _format_kb_response(self, result: Dict[str, Any]) -> str:
        """Format knowledge base result into a response."""
        if result['type'] == 'faq':
            return f"Q: {result['question']}\nA: {result['answer']}"
        elif result['type'] == 'location':
            return f"Location: {result['name']}\nAddress: {result['address']}"
        elif result['type'] == 'schedule':
            return f"Event: {result['name']}\nDate: {result['date']}\nTime: {result['time']}"
        elif result['type'] == 'document':
            return f"From document '{result['name']}':\n{result['content']}"
        else:
            return result.get('content', 'Information found but unable to format.')
    
    def _generate_llm_response(self, question: str, kb_results: List[Dict[str, Any]]) -> str:
        """Generate response using LLM with context from knowledge base."""
        try:
            # Build context from knowledge base results
            context = self._build_context(kb_results)
            
            # Create prompt for LLM
            prompt = self._create_llm_prompt(question, context)
            
            # Query LLM
            response = query_llm(
                prompt=prompt,
                provider=self.llm_provider
            )
            
            if response:
                return response
            else:
                return self._get_random_response('unknown')
                
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return self._get_random_response('unknown')
    
    def _build_context(self, kb_results: List[Dict[str, Any]]) -> str:
        """Build context string from knowledge base results."""
        if not kb_results:
            return "No specific information found in the knowledge base."
        
        context_parts = []
        for result in kb_results:
            if result['type'] == 'faq':
                context_parts.append(f"FAQ: {result['question']} - {result['answer']}")
            elif result['type'] == 'location':
                context_parts.append(f"Location: {result['name']} at {result['address']}")
            elif result['type'] == 'schedule':
                context_parts.append(f"Schedule: {result['name']} on {result['date']} at {result['time']}")
            elif result['type'] == 'document':
                context_parts.append(f"Document '{result['name']}': {result['content']}")
        
        return "\n".join(context_parts)
    
    def _create_llm_prompt(self, question: str, context: str) -> str:
        """Create a prompt for the LLM."""
        return f"""You are a helpful assistant for a summer school program. Answer the user's question based on the provided context and your general knowledge about educational programs.

Context from knowledge base:
{context}

User question: {question}

Please provide a helpful, accurate, and friendly response. If the context doesn't contain enough information, you can provide general guidance but clearly indicate when information is not specific to this program.

Response:"""
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def update_from_drive(self) -> bool:
        """
        Update knowledge base from Google Drive documents.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.drive_connector:
            logger.warning("Google Drive connector not available")
            return False
        
        try:
            # Get all documents from Drive
            documents = self.drive_connector.get_all_document_contents()
            
            if documents:
                # Update knowledge base
                self.knowledge_base.update_from_drive_documents(documents)
                logger.info(f"Updated knowledge base with {len(documents)} documents from Google Drive")
                return True
            else:
                logger.warning("No documents found in Google Drive")
                return False
                
        except Exception as e:
            logger.error(f"Error updating from Google Drive: {e}")
            return False
    
    def add_faq(self, category: str, question: str, answer: str, keywords: List[str] = None) -> None:
        """Add a FAQ to the knowledge base."""
        self.knowledge_base.add_faq(category, question, answer, keywords)
    
    def add_location(self, name: str, address: str, details: Dict = None) -> None:
        """Add location information to the knowledge base."""
        self.knowledge_base.add_location(name, address, details)
    
    def add_schedule(self, event_name: str, date: str, time: str, details: Dict = None) -> None:
        """Add schedule information to the knowledge base."""
        self.knowledge_base.add_schedule(event_name, date, time, details)
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history."""
        return self.conversation_history
    
    def clear_conversation_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get chatbot statistics."""
        kb_stats = self.knowledge_base.get_statistics()
        return {
            'knowledge_base': kb_stats,
            'conversation_history_length': len(self.conversation_history),
            'llm_provider': self.llm_provider,
            'drive_connected': self.drive_connector is not None
        }

def main():
    """Test the chatbot engine."""
    chatbot = SummerSchoolChatbot()
    
    # Add some test data
    chatbot.add_location("Main Campus", "123 University Ave, City, State 12345")
    chatbot.add_schedule("Orientation", "2024-06-15", "9:00 AM")
    chatbot.add_faq("general", "What should I bring?", "Bring comfortable clothes and a notebook.")
    
    # Test questions
    test_questions = [
        "Hello!",
        "Where is the school located?",
        "What's the schedule for orientation?",
        "What should I bring?",
        "How do I register?",
        "Goodbye!"
    ]
    
    print("🤖 Summer School Chatbot Test")
    print("=" * 40)
    
    for question in test_questions:
        print(f"\nUser: {question}")
        response = chatbot.ask(question)
        print(f"Bot: {response}")
    
    # Show statistics
    stats = chatbot.get_statistics()
    print(f"\n📊 Chatbot Statistics:")
    print(f"  Knowledge Base: {stats['knowledge_base']['total_documents']} documents")
    print(f"  Conversation History: {stats['conversation_history_length']} messages")
    print(f"  LLM Provider: {stats['llm_provider']}")
    print(f"  Drive Connected: {stats['drive_connected']}")

if __name__ == "__main__":
    main() 