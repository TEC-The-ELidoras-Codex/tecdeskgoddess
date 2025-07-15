"""
TEC Data Analytics System
Provides comprehensive analytics and insights for user data
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from collections import Counter, defaultdict

logger = logging.getLogger(__name__)

@dataclass
class AnalyticsReport:
    """Analytics report structure"""
    report_type: str
    user_id: str
    date_range: Dict[str, datetime]
    metrics: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    charts_data: Dict[str, Any]

class TECAnalytics:
    """Comprehensive analytics for TEC data"""
    
    def __init__(self, db_path: str = "data/tec_memory.db"):
        self.db_path = db_path
    
    def generate_user_report(self, user_id: str, days: int = 30) -> AnalyticsReport:
        """Generate comprehensive user analytics report"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get user data
        memories = self._get_user_memories(user_id, start_date, end_date)
        shared_content = self._get_user_shared_content(user_id, start_date, end_date)
        
        # Calculate metrics
        metrics = self._calculate_user_metrics(memories, shared_content, days)
        
        # Generate insights
        insights = self._generate_insights(metrics, memories, shared_content)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, insights)
        
        # Prepare chart data
        charts_data = self._prepare_chart_data(memories, shared_content, start_date, end_date)
        
        return AnalyticsReport(
            report_type="user_activity",
            user_id=user_id,
            date_range={"start": start_date, "end": end_date},
            metrics=metrics,
            insights=insights,
            recommendations=recommendations,
            charts_data=charts_data
        )
    
    def generate_memory_analysis(self, user_id: str) -> AnalyticsReport:
        """Analyze user's memory patterns and content"""
        memories = self._get_all_user_memories(user_id)
        
        # Analyze memory patterns
        memory_types = Counter(m['memory_type'] for m in memories)
        importance_dist = [m['importance'] for m in memories]
        
        # Topic analysis
        all_tags = []
        for memory in memories:
            tags = json.loads(memory['tags']) if memory['tags'] else []
            all_tags.extend(tags)
        
        tag_frequency = Counter(all_tags)
        
        # Time patterns
        creation_times = [datetime.fromisoformat(m['created_at']) for m in memories]
        monthly_counts = defaultdict(int)
        for dt in creation_times:
            month_key = dt.strftime("%Y-%m")
            monthly_counts[month_key] += 1
        
        metrics = {
            "total_memories": len(memories),
            "memory_types": dict(memory_types),
            "avg_importance": sum(importance_dist) / len(importance_dist) if importance_dist else 0,
            "top_tags": dict(tag_frequency.most_common(10)),
            "memories_per_month": dict(monthly_counts),
            "most_accessed": self._get_most_accessed_memories(memories)
        }
        
        insights = [
            f"You have {len(memories)} total memories stored",
            f"Your most common memory type is '{memory_types.most_common(1)[0][0]}'" if memory_types else "No memories yet",
            f"Average memory importance: {metrics['avg_importance']:.2f}/1.0",
            f"Most frequent topic: '{tag_frequency.most_common(1)[0][0]}'" if tag_frequency else "No topics tagged"
        ]
        
        recommendations = [
            "Consider adding more tags to your memories for better organization",
            "Try to balance different types of memories (facts, preferences, experiences)",
            "Review and update importance scores for better memory retrieval"
        ]
        
        return AnalyticsReport(
            report_type="memory_analysis",
            user_id=user_id,
            date_range={"start": min(creation_times) if creation_times else datetime.now(),
                       "end": max(creation_times) if creation_times else datetime.now()},
            metrics=metrics,
            insights=insights,
            recommendations=recommendations,
            charts_data=self._prepare_memory_charts(memories)
        )
    
    def generate_sharing_analysis(self, user_id: str) -> AnalyticsReport:
        """Analyze user's content sharing patterns"""
        shared_content = self._get_all_user_shared_content(user_id)
        
        if not shared_content:
            return AnalyticsReport(
                report_type="sharing_analysis",
                user_id=user_id,
                date_range={"start": datetime.now(), "end": datetime.now()},
                metrics={"total_shares": 0},
                insights=["No content shared yet"],
                recommendations=["Start sharing content to build your digital presence"],
                charts_data={}
            )
        
        # Analyze sharing patterns
        content_types = Counter(s['content_type'] for s in shared_content)
        total_views = sum(s['view_count'] for s in shared_content)
        
        # Time analysis
        share_times = [datetime.fromisoformat(s['created_at']) for s in shared_content]
        
        # Performance analysis
        top_performing = sorted(shared_content, key=lambda x: x['view_count'], reverse=True)[:5]
        
        metrics = {
            "total_shares": len(shared_content),
            "total_views": total_views,
            "avg_views_per_share": total_views / len(shared_content),
            "content_types": dict(content_types),
            "public_shares": len([s for s in shared_content if s['is_public']]),
            "top_performing": [{"title": s['title'], "views": s['view_count'], "type": s['content_type']} 
                              for s in top_performing]
        }
        
        insights = [
            f"You've shared {len(shared_content)} pieces of content",
            f"Total views across all content: {total_views}",
            f"Most popular content type: '{content_types.most_common(1)[0][0]}'" if content_types else "No content shared",
            f"Average views per share: {metrics['avg_views_per_share']:.1f}"
        ]
        
        recommendations = []
        if metrics['avg_views_per_share'] < 5:
            recommendations.append("Try sharing more engaging content to increase views")
        if metrics['public_shares'] < len(shared_content) * 0.5:
            recommendations.append("Consider making more content public to reach wider audience")
        
        return AnalyticsReport(
            report_type="sharing_analysis",
            user_id=user_id,
            date_range={"start": min(share_times), "end": max(share_times)},
            metrics=metrics,
            insights=insights,
            recommendations=recommendations,
            charts_data=self._prepare_sharing_charts(shared_content)
        )
    
    def generate_ai_interaction_analysis(self, user_id: str, days: int = 30) -> AnalyticsReport:
        """Analyze user's AI interaction patterns"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get conversation memories
        conversation_memories = self._get_user_memories(
            user_id, start_date, end_date, memory_type="conversation"
        )
        
        if not conversation_memories:
            return AnalyticsReport(
                report_type="ai_interaction",
                user_id=user_id,
                date_range={"start": start_date, "end": end_date},
                metrics={"total_interactions": 0},
                insights=["No AI interactions in the selected period"],
                recommendations=["Start chatting with Daisy to build your AI relationship"],
                charts_data={}
            )
        
        # Analyze interaction patterns
        daily_interactions = defaultdict(int)
        for memory in conversation_memories:
            date_key = datetime.fromisoformat(memory['created_at']).strftime("%Y-%m-%d")
            daily_interactions[date_key] += 1
        
        # Analyze conversation topics
        all_content = " ".join(m['content'] for m in conversation_memories)
        topics = self._extract_conversation_topics(all_content)
        
        # Calculate engagement metrics
        avg_daily = len(conversation_memories) / days
        most_active_day = max(daily_interactions.items(), key=lambda x: x[1]) if daily_interactions else ("N/A", 0)
        
        metrics = {
            "total_interactions": len(conversation_memories),
            "avg_daily_interactions": avg_daily,
            "most_active_day": {"date": most_active_day[0], "count": most_active_day[1]},
            "conversation_topics": topics,
            "daily_breakdown": dict(daily_interactions)
        }
        
        insights = [
            f"You had {len(conversation_memories)} AI interactions in the last {days} days",
            f"Average of {avg_daily:.1f} interactions per day",
            f"Most active day: {most_active_day[0]} with {most_active_day[1]} interactions",
            f"Most discussed topic: '{topics[0]}'" if topics else "No specific topics identified"
        ]
        
        recommendations = []
        if avg_daily < 1:
            recommendations.append("Try interacting with Daisy more regularly to build a stronger AI relationship")
        if len(topics) < 3:
            recommendations.append("Explore different conversation topics to expand your AI's understanding")
        
        return AnalyticsReport(
            report_type="ai_interaction",
            user_id=user_id,
            date_range={"start": start_date, "end": end_date},
            metrics=metrics,
            insights=insights,
            recommendations=recommendations,
            charts_data=self._prepare_interaction_charts(conversation_memories, daily_interactions)
        )
    
    def _get_user_memories(self, user_id: str, start_date: datetime, end_date: datetime, 
                          memory_type: Optional[str] = None) -> List[Dict]:
        """Get user memories within date range"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if memory_type:
            cursor.execute('''
                SELECT * FROM memories 
                WHERE user_id = ? AND memory_type = ? 
                AND created_at BETWEEN ? AND ?
                ORDER BY created_at DESC
            ''', (user_id, memory_type, start_date.isoformat(), end_date.isoformat()))
        else:
            cursor.execute('''
                SELECT * FROM memories 
                WHERE user_id = ? AND created_at BETWEEN ? AND ?
                ORDER BY created_at DESC
            ''', (user_id, start_date.isoformat(), end_date.isoformat()))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def _get_all_user_memories(self, user_id: str) -> List[Dict]:
        """Get all memories for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM memories WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def _get_user_shared_content(self, user_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get user shared content within date range"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM shared_content 
            WHERE user_id = ? AND created_at BETWEEN ? AND ?
            ORDER BY created_at DESC
        ''', (user_id, start_date.isoformat(), end_date.isoformat()))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def _get_all_user_shared_content(self, user_id: str) -> List[Dict]:
        """Get all shared content for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM shared_content WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def _calculate_user_metrics(self, memories: List[Dict], shared_content: List[Dict], days: int) -> Dict:
        """Calculate comprehensive user metrics"""
        return {
            "total_memories": len(memories),
            "total_shared_content": len(shared_content),
            "avg_memories_per_day": len(memories) / days,
            "avg_shares_per_day": len(shared_content) / days,
            "memory_types": Counter(m['memory_type'] for m in memories),
            "content_types": Counter(s['content_type'] for s in shared_content),
            "total_content_views": sum(s['view_count'] for s in shared_content),
            "engagement_score": self._calculate_engagement_score(memories, shared_content)
        }
    
    def _calculate_engagement_score(self, memories: List[Dict], shared_content: List[Dict]) -> float:
        """Calculate user engagement score (0-100)"""
        score = 0
        
        # Memory contribution (40 points max)
        memory_score = min(len(memories) * 2, 40)
        
        # Sharing contribution (30 points max)  
        sharing_score = min(len(shared_content) * 5, 30)
        
        # View contribution (30 points max)
        total_views = sum(s['view_count'] for s in shared_content)
        view_score = min(total_views, 30)
        
        return memory_score + sharing_score + view_score
    
    def _generate_insights(self, metrics: Dict, memories: List[Dict], shared_content: List[Dict]) -> List[str]:
        """Generate insights based on user data"""
        insights = []
        
        if metrics['engagement_score'] > 80:
            insights.append("🔥 You're a highly engaged TEC user!")
        elif metrics['engagement_score'] > 50:
            insights.append("📈 You're actively using TEC features")
        else:
            insights.append("🌱 You're just getting started with TEC")
        
        if metrics['avg_memories_per_day'] > 5:
            insights.append("💭 You create a lot of memories - great for building AI understanding")
        
        if metrics['total_content_views'] > 50:
            insights.append("👁️ Your shared content is getting good visibility")
        
        return insights
    
    def _generate_recommendations(self, metrics: Dict, insights: List[str]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        if metrics['total_memories'] < 10:
            recommendations.append("💡 Create more memories to help Daisy understand you better")
        
        if metrics['total_shared_content'] < 5:
            recommendations.append("🔗 Try sharing interesting URLs and content")
        
        if metrics['engagement_score'] < 30:
            recommendations.append("🚀 Explore more TEC features like quests and journaling")
        
        return recommendations
    
    def _prepare_chart_data(self, memories: List[Dict], shared_content: List[Dict], 
                           start_date: datetime, end_date: datetime) -> Dict:
        """Prepare data for charts and visualizations"""
        # Daily activity chart
        daily_activity = defaultdict(lambda: {"memories": 0, "shares": 0})
        
        for memory in memories:
            date_key = datetime.fromisoformat(memory['created_at']).strftime("%Y-%m-%d")
            daily_activity[date_key]["memories"] += 1
        
        for share in shared_content:
            date_key = datetime.fromisoformat(share['created_at']).strftime("%Y-%m-%d")
            daily_activity[date_key]["shares"] += 1
        
        return {
            "daily_activity": dict(daily_activity),
            "memory_types": dict(Counter(m['memory_type'] for m in memories)),
            "content_types": dict(Counter(s['content_type'] for s in shared_content))
        }
    
    def _prepare_memory_charts(self, memories: List[Dict]) -> Dict:
        """Prepare memory-specific chart data"""
        return {
            "importance_distribution": [m['importance'] for m in memories],
            "creation_timeline": [m['created_at'] for m in memories],
            "access_frequency": [m['access_count'] for m in memories]
        }
    
    def _prepare_sharing_charts(self, shared_content: List[Dict]) -> Dict:
        """Prepare sharing-specific chart data"""
        return {
            "view_distribution": [s['view_count'] for s in shared_content],
            "content_timeline": [s['created_at'] for s in shared_content],
            "popularity_trend": [(s['title'], s['view_count']) for s in shared_content]
        }
    
    def _prepare_interaction_charts(self, conversations: List[Dict], daily_interactions: Dict) -> Dict:
        """Prepare AI interaction chart data"""
        return {
            "daily_interactions": daily_interactions,
            "interaction_timeline": [c['created_at'] for c in conversations],
            "conversation_length": [len(c['content']) for c in conversations]
        }
    
    def _get_most_accessed_memories(self, memories: List[Dict]) -> List[Dict]:
        """Get most frequently accessed memories"""
        sorted_memories = sorted(memories, key=lambda x: x['access_count'], reverse=True)
        return [{"content": m['content'][:100], "access_count": m['access_count']} 
                for m in sorted_memories[:5]]
    
    def _extract_conversation_topics(self, text: str) -> List[str]:
        """Extract topics from conversation text"""
        # Simple topic extraction based on keywords
        topics = []
        text_lower = text.lower()
        
        topic_keywords = {
            "technology": ["code", "programming", "software", "tech", "computer"],
            "finance": ["money", "investment", "crypto", "finance", "trading"],
            "personal": ["feel", "think", "life", "personal", "experience"],
            "help": ["help", "question", "how", "what", "why"],
            "creative": ["creative", "art", "design", "music", "writing"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics[:5]

# Initialize global analytics
tec_analytics = TECAnalytics()
