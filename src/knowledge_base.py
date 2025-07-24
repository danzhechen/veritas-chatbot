#!/usr/bin/env python3
"""
Knowledge Base Manager for Summer School Chatbot

This module handles the organization, storage, and retrieval of
summer school program information from various sources.
"""

import hashlib
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """
    Enhanced knowledge base with improved search capabilities for Chinese text.
    """
    
    def __init__(self, knowledge_base_path: str = "data/knowledge_base.json"):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.knowledge_base = self._load_knowledge_base()
        
        # Enhanced keyword mappings for better Chinese search
        self.semantic_mappings = {
            # 地址相关
            'address': ['地址', '地点', '位置', '校园', '学校', '举办地', '场地', '在哪里', '哪里'],
            'location': ['地址', '地点', '位置', '校园', '学校', '举办地', '场地', '在哪里', '哪里'],
            
            # 时间相关
            'time': ['时间', '开始', '结束', '日期', '什么时候', '几点', '报到', '签到'],
            'schedule': ['时间安排', '日程', '课表', '活动安排', '时间表'],
            
            # 行为相关
            'behavior': ['行为', '不当', '守则', '规则', '行为准则', '违规', '纪律'],
            'misconduct': ['不当行为', '违规', '性骚扰', '歧视', '威胁', '恐吓'],
            
            # 住宿相关
            'accommodation': ['住宿', '床垫', '床上用品', '枕头', '被子', '宿舍', '居住'],
            'bedding': ['床垫', '床上用品', '枕头', '被子', '床单', '毛巾被'],
            
            # 活动相关
            'activity': ['活动', '晚间活动', '参与', '参加', '出席', '必须'],
            'evening': ['晚间活动', '晚上', '夜晚', '晚间'],
            
            # 邮寄相关
            'mailing': ['邮寄', '快递', '寄送', '邮递', '运送', '物流'],
            'shipping': ['邮寄', '快递', '寄送', '邮递', '运送', '物流']
        }
        
        # Question pattern matching for better intent recognition
        self.question_patterns = {
            'location_question': [
                r'.*在哪里.*', r'.*地址.*', r'.*地点.*', r'.*位置.*',
                r'.*举办地.*', r'.*校园.*', r'.*学校.*'
            ],
            'time_question': [
                r'.*什么时候.*', r'.*开始时间.*', r'.*结束时间.*',
                r'.*几点.*', r'.*日期.*', r'.*时间.*'
            ],
            'behavior_question': [
                r'.*行为.*定义.*', r'.*不当行为.*', r'.*行为守则.*',
                r'.*违规.*', r'.*规则.*'
            ],
            'accommodation_question': [
                r'.*床垫.*', r'.*住宿.*', r'.*床上用品.*',
                r'.*需要.*买.*', r'.*自己.*准备.*'
            ],
            'activity_question': [
                r'.*晚间活动.*', r'.*可以.*不参加.*', r'.*必须.*参与.*',
                r'.*出席.*', r'.*活动.*参加.*'
            ],
            'mailing_question': [
                r'.*邮寄.*', r'.*快递.*', r'.*寄送.*',
                r'.*怎么寄.*', r'.*如何.*寄.*'
            ]
        }

    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load knowledge base from file."""
        if self.knowledge_base_path.exists():
            try:
                with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Loaded knowledge base from {self.knowledge_base_path}")
                return data
            except Exception as e:
                logger.error(f"Error loading knowledge base: {e}")
        
        # Default structure
        return {
            'documents': {},
            'faqs': {},
            'locations': {},
            'schedules': {},
            'metadata': {
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
        }

    def _save_knowledge_base(self) -> None:
        """Save knowledge base to file."""
        try:
            self.knowledge_base_path.parent.mkdir(parents=True, exist_ok=True)
            self.knowledge_base['metadata']['last_updated'] = datetime.now().isoformat()
            
            with open(self.knowledge_base_path, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved knowledge base to {self.knowledge_base_path}")
        except Exception as e:
            logger.error(f"Error saving knowledge base: {e}")

    def add_document(self, name: str, content: str, metadata: Dict = None) -> None:
        """
        Add a document to the knowledge base.
        
        Args:
            name: Document name
            content: Document content
            metadata: Additional metadata
        """
        doc_id = hashlib.md5(name.encode()).hexdigest()
        
        self.knowledge_base['documents'][doc_id] = {
            'name': name,
            'content': content,
            'metadata': metadata or {},
            'added': datetime.now().isoformat(),
            'keywords': self._extract_keywords(content)
        }
        
        self._save_knowledge_base()
        logger.info(f"Added document: {name}")

    def add_faq(self, category: str, question: str, answer: str, keywords: List[str] = None) -> None:
        """
        Add a FAQ entry to the knowledge base.
        
        Args:
            category: FAQ category
            question: The question
            answer: The answer
            keywords: Search keywords
        """
        if category not in self.knowledge_base['faqs']:
            self.knowledge_base['faqs'][category] = {}
        
        faq_id = hashlib.md5(question.encode()).hexdigest()
        
        self.knowledge_base['faqs'][category][faq_id] = {
            'question': question,
            'answer': answer,
            'keywords': keywords or self._extract_keywords(question + ' ' + answer),
            'added': datetime.now().isoformat()
        }
        
        self._save_knowledge_base()
        logger.info(f"Added FAQ: {question}")

    def add_location(self, name: str, address: str, details: Dict = None) -> None:
        """
        Add location information to the knowledge base.
        
        Args:
            name: Location name
            address: Location address
            details: Additional location details
        """
        self.knowledge_base['locations'][name] = {
            'address': address,
            'details': details or {},
            'added': datetime.now().isoformat()
        }
        
        self._save_knowledge_base()
        logger.info(f"Added location: {name}")

    def add_schedule(self, name: str, date: str, time: str, description: str = "") -> None:
        """
        Add schedule information to the knowledge base.
        
        Args:
            name: Event name
            date: Event date
            time: Event time
            description: Event description
        """
        schedule_id = hashlib.md5((name + date + time).encode()).hexdigest()
        
        self.knowledge_base['schedules'][schedule_id] = {
            'name': name,
            'date': date,
            'time': time,
            'description': description,
            'added': datetime.now().isoformat()
        }
        
        self._save_knowledge_base()
        logger.info(f"Added schedule: {name} on {date}")

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Enhanced search with better Chinese text processing and semantic matching.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of relevant results with scores
        """
        query_lower = query.lower().strip()
        query_keywords = self._extract_keywords_enhanced(query)
        
        # Detect question intent
        question_intent = self._detect_question_intent(query)
        
        results = []
        
        # Search documents with enhanced scoring
        for doc_id, doc in self.knowledge_base['documents'].items():
            score = self._calculate_enhanced_relevance_score(
                query_lower, query_keywords, doc['content'], 
                doc['keywords'], question_intent, doc['name']
            )
            if score > 0:
                # Get more relevant excerpt
                excerpt = self._extract_relevant_excerpt(doc['content'], query_keywords, query_lower)
                results.append({
                    'type': 'document',
                    'id': doc_id,
                    'name': doc['name'],
                    'content': excerpt,
                    'score': score,
                    'source': 'document'
                })

        # Search FAQs with enhanced matching
        for category, faqs in self.knowledge_base['faqs'].items():
            if isinstance(faqs, dict):
                for faq_id, faq in faqs.items():
                    if isinstance(faq, dict) and 'question' in faq and 'answer' in faq:
                        score = self._calculate_enhanced_relevance_score(
                            query_lower, query_keywords, 
                            faq['question'] + ' ' + faq['answer'], 
                            faq.get('keywords', []), question_intent, faq['question']
                        )
                        if score > 0:
                            results.append({
                                'type': 'faq',
                                'id': faq_id,
                                'category': category,
                                'question': faq['question'],
                                'answer': faq['answer'],
                                'score': score,
                                'source': 'faq'
                            })

        # Search locations with context awareness
        for name, location in self.knowledge_base['locations'].items():
            score = self._calculate_enhanced_relevance_score(
                query_lower, query_keywords, 
                name + ' ' + location['address'], 
                ['location', 'address', 'where'], question_intent, name
            )
            if score > 0:
                results.append({
                    'type': 'location',
                    'id': name,
                    'name': name,
                    'address': location['address'],
                    'score': score,
                    'source': 'location'
                })

        # Search schedules
        for schedule_id, schedule in self.knowledge_base['schedules'].items():
            score = self._calculate_enhanced_relevance_score(
                query_lower, query_keywords, 
                schedule['name'] + ' ' + schedule['date'] + ' ' + schedule['time'], 
                ['schedule', 'time', 'date'], question_intent, schedule['name']
            )
            if score > 0:
                results.append({
                    'type': 'schedule',
                    'id': schedule_id,
                    'name': schedule['name'],
                    'date': schedule['date'],
                    'time': schedule['time'],
                    'score': score,
                    'source': 'schedule'
                })

        # Sort by relevance score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:max_results]

    def _detect_question_intent(self, query: str) -> str:
        """Detect the intent of the question for better matching."""
        query_lower = query.lower()
        
        for intent, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent
        
        return 'general'

    def _extract_keywords_enhanced(self, text: str) -> List[str]:
        """Enhanced keyword extraction for Chinese text."""
        # Basic Chinese character and word extraction
        chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
        english_words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Combine and filter
        keywords = []
        
        # Add Chinese phrases (2+ characters)
        for phrase in chinese_chars:
            if len(phrase) >= 2:
                keywords.append(phrase)
                # Also add individual important characters
                for char in phrase:
                    if char in ['址', '点', '间', '始', '束', '住', '活', '为', '垫', '寄']:
                        keywords.append(char)
        
        # Add English words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        keywords.extend([word for word in english_words if word not in stop_words and len(word) > 2])
        
        return list(set(keywords))

    def _calculate_enhanced_relevance_score(self, query: str, query_keywords: List[str], 
                                         content: str, content_keywords: List[str], 
                                         question_intent: str, title: str = "") -> float:
        """Enhanced relevance scoring with semantic understanding."""
        content_lower = content.lower()
        title_lower = title.lower()
        
        total_score = 0.0
        
        # 1. Exact phrase match (highest priority)
        if query in content_lower:
            total_score += 2.0
        
        # 2. Title relevance
        if any(keyword in title_lower for keyword in query_keywords):
            total_score += 1.5
        
        # 3. Keyword matching with semantic expansion
        expanded_keywords = self._expand_keywords_semantically(query_keywords, question_intent)
        keyword_matches = sum(1 for keyword in expanded_keywords if keyword in content_lower)
        if expanded_keywords:
            total_score += (keyword_matches / len(expanded_keywords)) * 1.2
        
        # 4. Intent-based scoring
        intent_score = self._calculate_intent_score(question_intent, content_lower, title_lower)
        total_score += intent_score
        
        # 5. Content keyword overlap
        if content_keywords:
            content_matches = sum(1 for keyword in content_keywords if any(qk in keyword.lower() for qk in query_keywords))
            total_score += (content_matches / len(content_keywords)) * 0.8
        
        # 6. Question pattern matching
        pattern_score = self._calculate_pattern_score(query, content_lower)
        total_score += pattern_score
        
        return min(total_score, 3.0)  # Cap at 3.0

    def _expand_keywords_semantically(self, keywords: List[str], intent: str) -> List[str]:
        """Expand keywords based on semantic mappings."""
        expanded = set(keywords)
        
        for keyword in keywords:
            for semantic_key, related_words in self.semantic_mappings.items():
                if keyword in related_words:
                    expanded.update(related_words)
        
        # Add intent-specific keywords
        if intent in ['location_question', 'address_question']:
            expanded.update(self.semantic_mappings.get('location', []))
        elif intent in ['time_question']:
            expanded.update(self.semantic_mappings.get('time', []))
        elif intent in ['behavior_question']:
            expanded.update(self.semantic_mappings.get('behavior', []))
        elif intent in ['accommodation_question']:
            expanded.update(self.semantic_mappings.get('accommodation', []))
        elif intent in ['activity_question']:
            expanded.update(self.semantic_mappings.get('activity', []))
        elif intent in ['mailing_question']:
            expanded.update(self.semantic_mappings.get('mailing', []))
        
        return list(expanded)

    def _calculate_intent_score(self, intent: str, content: str, title: str) -> float:
        """Calculate score based on question intent."""
        intent_keywords = {
            'location_question': ['地址', '地点', '位置', '校园', '学校', '举办', '浦东', '上海', '申启路'],
            'time_question': ['时间', '日期', '7月', '8月', '开始', '结束', '报到', '签到', '13:30', '18:00'],
            'behavior_question': ['行为', '不当', '守则', '规则', '违规', '性骚扰', '歧视', '威胁'],
            'accommodation_question': ['床垫', '住宿', '床上用品', '枕头', '被子', '105', '198'],
            'activity_question': ['晚间活动', '参与', '参加', '出席', '21:40', '22:00'],
            'mailing_question': ['邮寄', '快递', '寄送', '7月25', '门卫', '唯理']
        }
        
        if intent in intent_keywords:
            keywords = intent_keywords[intent]
            matches = sum(1 for keyword in keywords if keyword in content or keyword in title)
            return (matches / len(keywords)) * 0.8
        
        return 0.0

    def _calculate_pattern_score(self, query: str, content: str) -> float:
        """Calculate score based on question patterns."""
        # Chinese question patterns
        question_indicators = ['什么', '哪里', '怎么', '如何', '可以', '需要', '应该']
        query_has_question = any(indicator in query for indicator in question_indicators)
        
        if query_has_question:
            # Look for answer patterns in content
            answer_patterns = ['是', '在', '于', '需要', '可以', '应该', '建议']
            answer_matches = sum(1 for pattern in answer_patterns if pattern in content)
            return min(answer_matches * 0.1, 0.3)
        
        return 0.0

    def _extract_relevant_excerpt(self, content: str, keywords: List[str], query: str) -> str:
        """Extract the most relevant excerpt from content."""
        sentences = re.split(r'[。！？\n]', content)
        
        best_sentence = ""
        best_score = 0
        
        for sentence in sentences:
            if len(sentence.strip()) < 10:
                continue
                
            sentence_lower = sentence.lower()
            score = 0
            
            # Direct query match
            if query in sentence_lower:
                score += 10
            
            # Keyword matches
            keyword_matches = sum(1 for keyword in keywords if keyword in sentence_lower)
            score += keyword_matches
            
            if score > best_score and len(sentence.strip()) > 20:
                best_score = score
                best_sentence = sentence.strip()
        
        if best_sentence:
            # Return the best sentence plus some context
            return best_sentence + (content[content.find(best_sentence):content.find(best_sentence)+300] if len(content) > content.find(best_sentence)+300 else "")
        
        # Fallback to beginning of content
        return content[:300] + '...' if len(content) > 300 else content

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text (legacy method for compatibility)."""
        return self._extract_keywords_enhanced(text)

    def get_faq_by_category(self, category: str) -> List[Dict]:
        """Get all FAQs in a specific category."""
        return list(self.knowledge_base['faqs'].get(category, {}).values())

    def get_all_locations(self) -> Dict[str, Dict]:
        """Get all location information."""
        return self.knowledge_base['locations']

    def get_all_schedules(self) -> Dict[str, Dict]:
        """Get all schedule information."""
        return self.knowledge_base['schedules']

    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        return {
            'documents': len(self.knowledge_base['documents']),
            'faqs': sum(len(faqs) for faqs in self.knowledge_base['faqs'].values()),
            'locations': len(self.knowledge_base['locations']),
            'schedules': len(self.knowledge_base['schedules']),
            'last_updated': self.knowledge_base['metadata'].get('last_updated', 'Unknown')
        } 