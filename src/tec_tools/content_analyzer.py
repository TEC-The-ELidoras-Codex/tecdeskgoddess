"""
TEC Content Sharing and Analysis System
Handles URL analysis, social media content, and shareable links
"""

import requests
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ContentAnalysis:
    """Analysis results for shared content"""
    url: str
    title: str
    description: str
    content_type: str
    thumbnail: Optional[str]
    text_content: str
    metadata: Dict[str, Any]
    analysis: Dict[str, Any]

class ContentAnalyzer:
    """Analyzes and extracts content from URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def analyze_url(self, url: str) -> ContentAnalysis:
        """Analyze any URL and extract meaningful content"""
        try:
            # Determine content type from URL
            content_type = self._detect_content_type(url)
            
            if content_type == "instagram":
                return self._analyze_instagram(url)
            elif content_type == "google_docs":
                return self._analyze_google_docs(url)
            elif content_type == "youtube":
                return self._analyze_youtube(url)
            elif content_type == "twitter":
                return self._analyze_twitter(url)
            elif content_type == "reddit":
                return self._analyze_reddit(url)
            else:
                return self._analyze_generic(url)
                
        except Exception as e:
            logger.error(f"Error analyzing URL {url}: {e}")
            return self._create_error_analysis(url, str(e))
    
    def _detect_content_type(self, url: str) -> str:
        """Detect the type of content from URL"""
        domain = urlparse(url).netloc.lower()
        
        if 'instagram.com' in domain:
            return "instagram"
        elif 'docs.google.com' in domain:
            return "google_docs"
        elif 'youtube.com' in domain or 'youtu.be' in domain:
            return "youtube"
        elif 'twitter.com' in domain or 'x.com' in domain:
            return "twitter"
        elif 'reddit.com' in domain:
            return "reddit"
        elif 'github.com' in domain:
            return "github"
        elif 'linkedin.com' in domain:
            return "linkedin"
        else:
            return "webpage"
    
    def _analyze_instagram(self, url: str) -> ContentAnalysis:
        """Analyze Instagram posts/profiles"""
        # Instagram requires special handling due to login requirements
        # For now, extract what we can from the URL
        
        post_id = None
        if '/p/' in url:
            post_id = url.split('/p/')[1].split('/')[0]
        elif '/reel/' in url:
            post_id = url.split('/reel/')[1].split('/')[0]
        
        metadata = {
            "platform": "instagram",
            "post_id": post_id,
            "url_type": "post" if post_id else "profile"
        }
        
        return ContentAnalysis(
            url=url,
            title="Instagram Content",
            description="Instagram post or profile shared",
            content_type="instagram",
            thumbnail=None,
            text_content="Instagram content (login required for full analysis)",
            metadata=metadata,
            analysis={
                "sentiment": "neutral",
                "topics": ["social_media", "instagram"],
                "actionable": False
            }
        )
    
    def _analyze_google_docs(self, url: str) -> ContentAnalysis:
        """Analyze Google Docs/Sheets/Slides"""
        # Extract document ID
        doc_id = None
        doc_type = "document"
        
        if '/document/d/' in url:
            doc_id = url.split('/document/d/')[1].split('/')[0]
            doc_type = "document"
        elif '/spreadsheets/d/' in url:
            doc_id = url.split('/spreadsheets/d/')[1].split('/')[0]
            doc_type = "spreadsheet"
        elif '/presentation/d/' in url:
            doc_id = url.split('/presentation/d/')[1].split('/')[0]
            doc_type = "presentation"
        
        # Try to access public content
        try:
            if doc_type == "document":
                export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
                response = self.session.get(export_url)
                if response.status_code == 200:
                    text_content = response.text[:1000]  # First 1000 chars
                else:
                    text_content = "Document is private or requires authentication"
            else:
                text_content = f"Google {doc_type} (requires authentication for content)"
                
        except Exception as e:
            text_content = f"Could not access document content: {e}"
        
        metadata = {
            "platform": "google",
            "doc_id": doc_id,
            "doc_type": doc_type
        }
        
        return ContentAnalysis(
            url=url,
            title=f"Google {doc_type.title()}",
            description=f"Shared Google {doc_type}",
            content_type="google_docs",
            thumbnail=None,
            text_content=text_content,
            metadata=metadata,
            analysis={
                "sentiment": "neutral",
                "topics": ["document", "google", doc_type],
                "actionable": True
            }
        )
    
    def _analyze_youtube(self, url: str) -> ContentAnalysis:
        """Analyze YouTube videos"""
        # Extract video ID
        video_id = None
        if 'youtube.com/watch?v=' in url:
            video_id = parse_qs(urlparse(url).query).get('v', [None])[0]
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
        
        # Get video info from oEmbed API
        try:
            oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
            response = self.session.get(oembed_url)
            if response.status_code == 200:
                data = response.json()
                title = data.get('title', 'YouTube Video')
                description = data.get('author_name', '')
                thumbnail = data.get('thumbnail_url')
            else:
                title = "YouTube Video"
                description = "Video details unavailable"
                thumbnail = None
        except Exception as e:
            title = "YouTube Video"
            description = f"Error fetching video info: {e}"
            thumbnail = None
        
        metadata = {
            "platform": "youtube",
            "video_id": video_id
        }
        
        return ContentAnalysis(
            url=url,
            title=title,
            description=description,
            content_type="youtube",
            thumbnail=thumbnail,
            text_content=f"YouTube video: {title}",
            metadata=metadata,
            analysis={
                "sentiment": "neutral",
                "topics": ["video", "youtube", "entertainment"],
                "actionable": True
            }
        )
    
    def _analyze_generic(self, url: str) -> ContentAnalysis:
        """Analyze generic webpages"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title = title.get_text().strip() if title else "Webpage"
            
            # Extract description
            description = ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                description = meta_desc.get('content', '')
            
            # Extract Open Graph data
            og_title = soup.find('meta', property='og:title')
            og_desc = soup.find('meta', property='og:description')
            og_image = soup.find('meta', property='og:image')
            
            if og_title:
                title = og_title.get('content', title)
            if og_desc:
                description = og_desc.get('content', description)
            
            thumbnail = og_image.get('content') if og_image else None
            
            # Extract main text content
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text_content = soup.get_text()
            # Clean up text
            lines = (line.strip() for line in text_content.splitlines())
            text_content = ' '.join(line for line in lines if line)[:2000]  # First 2000 chars
            
            # Basic content analysis
            topics = self._extract_topics(text_content)
            sentiment = self._analyze_sentiment(text_content)
            
            metadata = {
                "domain": urlparse(url).netloc,
                "content_length": len(text_content),
                "has_images": len(soup.find_all('img')) > 0
            }
            
            return ContentAnalysis(
                url=url,
                title=title,
                description=description,
                content_type="webpage",
                thumbnail=thumbnail,
                text_content=text_content,
                metadata=metadata,
                analysis={
                    "sentiment": sentiment,
                    "topics": topics,
                    "actionable": True
                }
            )
            
        except Exception as e:
            return self._create_error_analysis(url, str(e))
    
    def _analyze_twitter(self, url: str) -> ContentAnalysis:
        """Analyze Twitter/X posts"""
        # Extract tweet ID if possible
        tweet_id = None
        if '/status/' in url:
            tweet_id = url.split('/status/')[1].split('?')[0]
        
        metadata = {
            "platform": "twitter",
            "tweet_id": tweet_id
        }
        
        return ContentAnalysis(
            url=url,
            title="Twitter/X Post",
            description="Social media post from Twitter/X",
            content_type="twitter",
            thumbnail=None,
            text_content="Twitter/X post (requires authentication for full content)",
            metadata=metadata,
            analysis={
                "sentiment": "neutral",
                "topics": ["social_media", "twitter"],
                "actionable": False
            }
        )
    
    def _analyze_reddit(self, url: str) -> ContentAnalysis:
        """Analyze Reddit posts"""
        try:
            # Add .json to Reddit URL to get JSON data
            json_url = url.rstrip('/') + '.json'
            response = self.session.get(json_url)
            
            if response.status_code == 200:
                data = response.json()
                post_data = data[0]['data']['children'][0]['data']
                
                title = post_data.get('title', 'Reddit Post')
                description = post_data.get('selftext', '')[:200]
                thumbnail = post_data.get('thumbnail')
                if thumbnail and thumbnail.startswith('http'):
                    pass  # Valid thumbnail
                else:
                    thumbnail = None
                
                metadata = {
                    "platform": "reddit",
                    "subreddit": post_data.get('subreddit'),
                    "score": post_data.get('score'),
                    "num_comments": post_data.get('num_comments')
                }
                
                return ContentAnalysis(
                    url=url,
                    title=title,
                    description=description,
                    content_type="reddit",
                    thumbnail=thumbnail,
                    text_content=f"Reddit post in r/{post_data.get('subreddit', 'unknown')}: {title}",
                    metadata=metadata,
                    analysis={
                        "sentiment": "neutral",
                        "topics": ["reddit", "discussion", post_data.get('subreddit', 'unknown')],
                        "actionable": True
                    }
                )
        except Exception as e:
            logger.error(f"Error analyzing Reddit URL: {e}")
        
        return self._create_error_analysis(url, "Could not analyze Reddit post")
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text using simple keyword matching"""
        topics = []
        text_lower = text.lower()
        
        # Topic keywords
        topic_keywords = {
            "technology": ["tech", "software", "computer", "programming", "code", "app", "ai", "artificial intelligence"],
            "finance": ["money", "investment", "crypto", "bitcoin", "finance", "trading", "stock", "market"],
            "health": ["health", "fitness", "medical", "doctor", "exercise", "nutrition", "wellness"],
            "education": ["learn", "education", "course", "tutorial", "study", "school", "university"],
            "business": ["business", "company", "startup", "entrepreneur", "marketing", "sales"],
            "entertainment": ["movie", "music", "game", "gaming", "entertainment", "fun", "comedy"],
            "news": ["news", "breaking", "update", "announcement", "press", "report"],
            "science": ["science", "research", "study", "discovery", "experiment", "scientific"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics[:5]  # Return max 5 topics
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "love", "like", "best", "awesome", "fantastic"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "horrible", "disgusting", "annoying", "frustrating"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _create_error_analysis(self, url: str, error: str) -> ContentAnalysis:
        """Create an analysis object for errors"""
        return ContentAnalysis(
            url=url,
            title="Content Analysis Error",
            description=f"Could not analyze content: {error}",
            content_type="error",
            thumbnail=None,
            text_content=f"Error analyzing {url}: {error}",
            metadata={"error": error},
            analysis={
                "sentiment": "neutral",
                "topics": ["error"],
                "actionable": False
            }
        )

class ShareCodeGenerator:
    """Generates and manages share codes for content"""
    
    @staticmethod
    def create_share_url(share_code: str, base_url: str = "http://localhost:8000") -> str:
        """Create a shareable URL from a share code"""
        return f"{base_url}/share/{share_code}"
    
    @staticmethod
    def create_social_share_text(content: ContentAnalysis, share_url: str) -> Dict[str, str]:
        """Create social media share text"""
        title = content.title
        description = content.description[:100] + "..." if len(content.description) > 100 else content.description
        
        return {
            "twitter": f"Check this out: {title} {share_url} via @TEC_BITLYFE #DigitalSovereignty",
            "facebook": f"{title}\n\n{description}\n\n{share_url}",
            "linkedin": f"{title}\n\n{description}\n\nShared via TEC: BITLYFE\n{share_url}",
            "reddit": f"{title}\n\n{description}\n\nSource: {share_url}",
            "discord": f"**{title}**\n{description}\n{share_url}",
            "email": f"Subject: {title}\n\nI thought you might find this interesting:\n\n{title}\n{description}\n\nView here: {share_url}\n\nShared via TEC: BITLYFE"
        }

# Initialize global content analyzer
content_analyzer = ContentAnalyzer()
