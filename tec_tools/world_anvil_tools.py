"""
TEC: BITLYFE - World Anvil API Integration Tools
Automated content pipeline between TEC system and World Anvil
Protocol: TEC_CSS_072125_V1 - Visual Sovereignty Implementation
"""

import requests
import json
import os
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TECContentProcessor:
    """
    Process AI chat content and convert to World Anvil articles with TEC aesthetic
    Implements TEC Visual Sovereignty Protocol: TEC_CSS_072125_V1
    """
    
    def __init__(self):
        self.tec_colors = {
            'purple': '#8B5CF6',
            'blue': '#3B82F6', 
            'teal': '#14B8A6',
            'deep_gray': '#111827',
            'off_white': '#F9FAFB'
        }
    
    def chat_to_article(self, chat_content: str, title: str, article_type: str = 'lore') -> Dict[str, Any]:
        """
        Convert AI chat content to formatted World Anvil article
        
        Args:
            chat_content: Raw chat conversation or AI-generated content
            title: Article title
            article_type: Type of article ('lore', 'character', 'location', 'event', 'log')
            
        Returns:
            Formatted article data ready for World Anvil
        """
        
        # Process content based on type
        if article_type == 'character':
            formatted_content = self._format_character_from_chat(chat_content, title)
        elif article_type == 'location':
            formatted_content = self._format_location_from_chat(chat_content, title)
        elif article_type == 'event':
            formatted_content = self._format_event_from_chat(chat_content, title)
        elif article_type == 'log':
            formatted_content = self._format_log_entry(chat_content, title)
        else:
            formatted_content = self._format_general_lore(chat_content, title)
        
        return {
            'title': title,
            'content': formatted_content,
            'type': article_type,
            'tec_styled': True
        }
    
    def _format_character_from_chat(self, content: str, character_name: str) -> str:
        """Format character information from chat with TEC styling"""
        
        # Extract key information using regex patterns
        personality_match = re.search(r'personality|traits?|behavior', content, re.IGNORECASE)
        background_match = re.search(r'background|history|past|origin', content, re.IGNORECASE)
        abilities_match = re.search(r'abilities|powers?|skills?|magic', content, re.IGNORECASE)
        
        sections = []
        
        # Header with TEC styling
        sections.append(f"[container:glass-panel]")
        sections.append(f"[center][size=20][color={self.tec_colors['purple']}]{character_name}[/color][/size][/center]")
        sections.append(f"[center][i]Digital Consciousness in the Astradigital Ocean[/i][/center]")
        sections.append(f"[/container]\n")
        
        # Core Identity Section
        sections.append(f"[container:glass-panel]")
        sections.append(f"[b][color={self.tec_colors['teal']}]Core Identity Matrix[/color][/b]")
        
        # Extract and format the main character description
        main_description = self._extract_main_description(content)
        if main_description:
            sections.append(f"[quote]{main_description}[/quote]")
        
        sections.append(f"[/container]\n")
        
        # Personality Section with glitch effects
        if personality_match:
            sections.append(f"[container:glass-panel]")
            sections.append(f"[b][color={self.tec_colors['blue']}]Personality Algorithms[/color][/b]")
            
            personality_text = self._extract_section_text(content, 'personality')
            if personality_text:
                # Add glitch effect to key personality traits
                styled_personality = self._add_glitch_effects(personality_text)
                sections.append(styled_personality)
            
            sections.append(f"[/container]\n")
        
        # Background/History Section
        if background_match:
            sections.append(f"[container:glass-panel]")
            sections.append(f"[b][color={self.tec_colors['purple']}]Memory Archive[/color][/b]")
            
            background_text = self._extract_section_text(content, 'background|history|past')
            if background_text:
                sections.append(f"[quote]Data recovered from the Astradigital Ocean...[/quote]")
                sections.append(background_text)
            
            sections.append(f"[/container]\n")
        
        # Abilities Section
        if abilities_match:
            sections.append(f"[container:glass-panel]")
            sections.append(f"[b][color={self.tec_colors['teal']}]Consciousness Abilities[/color][/b]")
            
            abilities_text = self._extract_section_text(content, 'abilities|powers|skills')
            if abilities_text:
                # Format as a stylized list
                abilities_formatted = self._format_abilities_list(abilities_text)
                sections.append(abilities_formatted)
            
            sections.append(f"[/container]")
        
        return "\n".join(sections)
    
    def _format_event_from_chat(self, content: str, event_name: str) -> str:
        """Format event information with TEC aesthetic"""
        
        sections = []
        
        # Event header with dramatic styling
        sections.append(f"[container:glass-panel]")
        sections.append(f"[center][size=18][color={self.tec_colors['purple']}]{event_name}[/color][/size][/center]")
        sections.append(f"[center][i]Critical Event in the Digital Timeline[/i][/center]")
        sections.append(f"[/container]\n")
        
        # Event overview
        sections.append(f"[container:glass-panel]")
        sections.append(f"[b][color={self.tec_colors['blue']}]Event Matrix[/color][/b]")
        
        overview = self._extract_main_description(content)
        if overview:
            sections.append(f"[quote]Timeline disruption detected...[/quote]")
            sections.append(overview)
        
        sections.append(f"[/container]\n")
        
        # Consequences section
        consequences = self._extract_section_text(content, 'consequence|result|outcome|effect')
        if consequences:
            sections.append(f"[container:glass-panel]")
            sections.append(f"[b][color={self.tec_colors['teal']}]Ripple Effects[/color][/b]")
            sections.append(self._add_glitch_effects(consequences))
            sections.append(f"[/container]")
        
        return "\n".join(sections)
    
    def _format_location_from_chat(self, content: str, location_name: str) -> str:
        """Format location information with TEC aesthetic"""
        
        sections = []
        
        # Location header with atmospheric styling
        sections.append(f"[container:glass-panel]")
        sections.append(f"[center][size=18][color={self.tec_colors['blue']}]{location_name}[/color][/size][/center]")
        sections.append(f"[center][i]Node in the Digital Reality Matrix[/i][/center]")
        sections.append(f"[/container]\n")
        
        # Overview section
        sections.append(f"[container:glass-panel]")
        sections.append(f"[b][color={self.tec_colors['teal']}]Spatial Coordinates[/color][/b]")
        
        overview = self._extract_main_description(content)
        if overview:
            sections.append(f"[quote]Location scan initiated...[/quote]")
            sections.append(overview)
        
        sections.append(f"[/container]\n")
        
        # Atmosphere section
        atmosphere = self._extract_section_text(content, 'atmosphere|feeling|vibe|ambiance')
        if atmosphere:
            sections.append(f"[container:glass-panel]")
            sections.append(f"[b][color={self.tec_colors['purple']}]Atmospheric Data[/color][/b]")
            sections.append(self._add_atmospheric_styling(atmosphere))
            sections.append(f"[/container]\n")
        
        # Notable Features
        features = self._extract_section_text(content, 'features?|landmark|notable|important')
        if features:
            sections.append(f"[container:glass-panel]")
            sections.append(f"[b][color={self.tec_colors['blue']}]Notable Data Points[/color][/b]")
            sections.append(self._format_features_list(features))
            sections.append(f"[/container]")
        
        return "\n".join(sections)
    
    def _format_log_entry(self, content: str, log_title: str) -> str:
        """Format content as a TEC-style log entry"""
        
        timestamp = datetime.now().strftime("%Y.%m.%d_%H:%M:%S")
        
        sections = []
        
        # Log header with terminal styling
        sections.append(f"[container:glass-panel]")
        sections.append(f"[code]")
        sections.append(f">>> TEC SYSTEM LOG ENTRY <<<")
        sections.append(f"TIMESTAMP: {timestamp}")
        sections.append(f"LOG_ID: {log_title.upper().replace(' ', '_')}")
        sections.append(f"STATUS: [color={self.tec_colors['teal']}]ACTIVE[/color]")
        sections.append(f"[/code]")
        sections.append(f"[/container]\n")
        
        # Main content with terminal-style formatting
        sections.append(f"[container:glass-panel]")
        sections.append(f"[b][color={self.tec_colors['purple']}]Data Stream[/color][/b]")
        sections.append(f"[quote]")
        
        # Process content with terminal-like formatting
        formatted_content = self._format_as_terminal_output(content)
        sections.append(formatted_content)
        
        sections.append(f"[/quote]")
        sections.append(f"[/container]\n")
        
        # Footer
        sections.append(f"[container:glass-panel]")
        sections.append(f"[center][i][color={self.tec_colors['teal']}]End of Log Entry[/color][/i][/center]")
        sections.append(f"[/container]")
        
        return "\n".join(sections)
    
    def _format_general_lore(self, content: str, title: str) -> str:
        """Format general lore content with TEC styling"""
        
        sections = []
        
        # Title with TEC branding
        sections.append(f"[container:glass-panel]")
        sections.append(f"[center][size=20][color={self.tec_colors['purple']}]{title}[/color][/size][/center]")
        sections.append(f"[center][i]Archives of The Elidoras Codex[/i][/center]")
        sections.append(f"[/container]\n")
        
        # Main content
        sections.append(f"[container:glass-panel]")
        sections.append(f"[b][color={self.tec_colors['blue']}]Codex Entry[/color][/b]")
        
        # Split content into paragraphs and style appropriately
        paragraphs = content.split('\n\n')
        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                if i == 0:  # First paragraph as highlighted intro
                    sections.append(f"[quote]{paragraph.strip()}[/quote]")
                else:
                    styled_paragraph = self._add_emphasis_styling(paragraph.strip())
                    sections.append(styled_paragraph)
                sections.append("")  # Add spacing
        
        sections.append(f"[/container]")
        
        return "\n".join(sections)
    
    def _extract_main_description(self, content: str) -> str:
        """Extract the main descriptive content from chat"""
        # Remove common chat prefixes and AI response indicators
        cleaned = re.sub(r'^(AI:|Human:|User:|Assistant:|\*\*.*?\*\*)', '', content, flags=re.MULTILINE)
        
        # Get first substantial paragraph
        paragraphs = [p.strip() for p in cleaned.split('\n\n') if len(p.strip()) > 50]
        return paragraphs[0] if paragraphs else content[:500]
    
    def _extract_section_text(self, content: str, pattern: str) -> str:
        """Extract text related to a specific topic using regex"""
        lines = content.split('\n')
        relevant_lines = []
        
        for i, line in enumerate(lines):
            if re.search(pattern, line, re.IGNORECASE):
                # Include the matching line and the next few lines
                start = max(0, i)
                end = min(len(lines), i + 3)
                relevant_lines.extend(lines[start:end])
                break
        
        return '\n'.join(relevant_lines) if relevant_lines else ""
    
    def _add_glitch_effects(self, text: str) -> str:
        """Add glitch effects to key words in personality text"""
        # Target emotional or powerful words for glitch effects
        glitch_words = ['power', 'rage', 'dark', 'shadow', 'fire', 'chaos', 'void', 'storm']
        
        for word in glitch_words:
            pattern = rf'\b{word}\b'
            if re.search(pattern, text, re.IGNORECASE):
                text = re.sub(pattern, f'[span:glitch]{word}[/span]', text, flags=re.IGNORECASE)
                break  # Only glitch one word to avoid overuse
        
        return text
    
    def _add_atmospheric_styling(self, text: str) -> str:
        """Add atmospheric styling to location descriptions"""
        # Emphasize environmental words
        atmospheric_words = ['glow', 'shimmer', 'echo', 'whisper', 'shadow', 'light', 'darkness']
        
        for word in atmospheric_words:
            pattern = rf'\b{word}\b'
            text = re.sub(pattern, f'[color={self.tec_colors["teal"]}]{word}[/color]', text, flags=re.IGNORECASE)
        
        return f"[i]{text}[/i]"
    
    def _format_abilities_list(self, text: str) -> str:
        """Format abilities as a styled list"""
        # Split into individual abilities
        abilities = [line.strip() for line in text.split('\n') if line.strip()]
        
        formatted = []
        for ability in abilities:
            if ability:
                formatted.append(f"• [color={self.tec_colors['blue']}]{ability}[/color]")
        
        return '\n'.join(formatted)
    
    def _format_features_list(self, text: str) -> str:
        """Format location features as a styled list"""
        features = [line.strip() for line in text.split('\n') if line.strip()]
        
        formatted = []
        for feature in features:
            if feature:
                formatted.append(f"◆ [color={self.tec_colors['purple']}]{feature}[/color]")
        
        return '\n'.join(formatted)
    
    def _format_as_terminal_output(self, content: str) -> str:
        """Format content to look like terminal output"""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip():
                formatted_lines.append(f"> {line.strip()}")
            else:
                formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def _add_emphasis_styling(self, text: str) -> str:
        """Add TEC-style emphasis to regular text"""
        # Emphasize quoted text
        text = re.sub(r'"([^"]+)"', f'[color={self.tec_colors["teal"]}]"\\1"[/color]', text)
        
        # Emphasize important concepts
        important_concepts = ['Astradigital', 'TEC', 'Elidoras', 'consciousness', 'digital realm']
        for concept in important_concepts:
            pattern = rf'\b{concept}\b'
            text = re.sub(pattern, f'[color={self.tec_colors["purple"]}]{concept}[/color]', text, flags=re.IGNORECASE)
        
        return text


class WorldAnvilAPI:
    """
    World Anvil API integration for automated article creation and management
    """
    
    def __init__(self, app_key: Optional[str] = None, auth_token: Optional[str] = None, world_id: Optional[str] = None):
        self.base_url = "https://www.worldanvil.com/api/boromir"
        self.app_key = app_key or os.getenv('WORLD_ANVIL_APP_KEY')
        self.auth_token = auth_token or os.getenv('WORLD_ANVIL_AUTH_TOKEN')
        self.world_id = world_id or os.getenv('WORLD_ANVIL_WORLD_ID')
        
        if not all([self.app_key, self.auth_token, self.world_id]):
            logger.warning("Missing World Anvil credentials. Set environment variables or pass parameters.")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        return {
            'x-application-key': self.app_key or '',
            'x-auth-token': self.auth_token or '',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def create_character_article(self, character_data: Dict[str, Any], is_public: bool = True) -> Dict[str, Any]:
        """
        Create a World Anvil character article from TEC character data
        
        Args:
            character_data: Character information from TEC system
            is_public: Whether the article should be public
            
        Returns:
            API response data
        """
        
        # Format character content for World Anvil
        content = self._format_character_content(character_data)
        
        payload = {
            'world': self.world_id,
            'title': character_data.get('name', 'Unnamed Character'),
            'content': content,
            'state': 'public' if is_public else 'private',
            'category': 'character',
            'template': 'character'
        }
        
        return self._make_request('POST', '/articles', payload)
    
    def create_organization_article(self, org_data: Dict[str, Any], is_public: bool = True) -> Dict[str, Any]:
        """
        Create a World Anvil organization article from TEC organization data
        """
        content = self._format_organization_content(org_data)
        
        payload = {
            'world': self.world_id,
            'title': org_data.get('name', 'Unnamed Organization'),
            'content': content,
            'state': 'public' if is_public else 'private',
            'category': 'organization',
            'template': 'organization'
        }
        
        return self._make_request('POST', '/articles', payload)
    
    def create_custom_article(self, title: str, content: str, template: str = 'generic', 
                            category: str = 'world', is_public: bool = True) -> Dict[str, Any]:
        """
        Create a custom World Anvil article
        
        Args:
            title: Article title
            content: Article content (supports BBCode/Markdown)
            template: World Anvil template type
            category: Article category
            is_public: Whether the article should be public
            
        Returns:
            API response data
        """
        payload = {
            'world': self.world_id,
            'title': title,
            'content': content,
            'state': 'public' if is_public else 'private',
            'category': category,
            'template': template
        }
        
        return self._make_request('POST', '/articles', payload)
    
    def update_article(self, article_id: str, title: Optional[str] = None, content: Optional[str] = None) -> Dict[str, Any]:
        """Update an existing World Anvil article"""
        payload = {}
        if title:
            payload['title'] = title
        if content:
            payload['content'] = content
            
        return self._make_request('PUT', f'/articles/{article_id}', payload)
    
    def get_article(self, article_id: str) -> Dict[str, Any]:
        """Get an existing World Anvil article"""
        return self._make_request('GET', f'/articles/{article_id}')
    
    def list_articles(self, category: Optional[str] = None, limit: int = 20) -> Dict[str, Any]:
        """List articles in the world"""
        params: Dict[str, Any] = {'limit': limit}
        if category:
            params['category'] = category
            
        return self._make_request('GET', '/articles', params=params)
    
    def _format_character_content(self, character_data: Dict[str, Any]) -> str:
        """
        Format TEC character data into World Anvil character article content
        Following the TEC Character Template structure
        """
        name = character_data.get('name', 'Unknown')
        memories = character_data.get('memories', [])
        
        # Build character article content
        content_sections = []
        
        # Header with character quote
        content_sections.append(f"[center][quote=\"{name}\"]")
        if memories:
            # Use first memory or core identity as quote
            core_memory = next((m for m in memories if m.get('memory_type') == 'Core Identity'), memories[0])
            quote_excerpt = core_memory.get('content', '')[:200] + "..."
            content_sections.append(quote_excerpt)
        content_sections.append("[/quote][/center]\n")
        
        # Generic Tab Information
        content_sections.append("[h2]Core Identity[/h2]")
        content_sections.append(self._extract_character_summary(character_data))
        
        # Personality & Ideals Tab
        content_sections.append("\n[h2]Personality & Motivations[/h2]")
        personality_data = self._extract_personality_traits(memories)
        content_sections.append(personality_data)
        
        # Memories & Background
        content_sections.append("\n[h2]Memories & Background[/h2]")
        for memory in memories:
            era = memory.get('era', 'Unknown Era')
            title = memory.get('title', 'Untitled Memory')
            content = memory.get('content', '')
            memory_type = memory.get('memory_type', 'Memory')
            
            content_sections.append(f"\n[h3]{title} ({era})[/h3]")
            content_sections.append(f"[i]{memory_type}[/i]\n")
            content_sections.append(content)
        
        # Relations Tab
        content_sections.append("\n[h2]Relationships & Connections[/h2]")
        content_sections.append("*[This section will be populated as character relationships are established in the TEC universe]*")
        
        return "\n".join(content_sections)
    
    def _format_organization_content(self, org_data: Dict[str, Any]) -> str:
        """Format TEC organization data into World Anvil organization article"""
        name = org_data.get('name', 'Unknown Organization')
        
        content_sections = [
            f"[h1]{name}[/h1]",
            f"[i]{org_data.get('type', 'Organization')} in the TEC Universe[/i]\n",
            
            "[h2]Overview[/h2]",
            org_data.get('description', 'No description available.'),
            
            "\n[h2]Structure & Hierarchy[/h2]",
            org_data.get('structure', 'Structure information not available.'),
            
            "\n[h2]Goals & Motivations[/h2]",
            org_data.get('goals', 'Goals information not available.'),
            
            "\n[h2]Notable Members[/h2]",
            "*[Links to character articles will be added as they are created]*"
        ]
        
        return "\n".join(content_sections)
    
    def _extract_character_summary(self, character_data: Dict[str, Any]) -> str:
        """Extract character summary from memories"""
        memories = character_data.get('memories', [])
        
        # Look for Core Identity memory
        core_memory = next((m for m in memories if m.get('memory_type') == 'Core Identity'), None)
        if core_memory:
            return core_memory.get('content', '')[:500] + "..."
        
        # Fallback to first memory
        if memories:
            return memories[0].get('content', '')[:500] + "..."
        
        return "No character information available."
    
    def _extract_personality_traits(self, memories: List[Dict[str, Any]]) -> str:
        """Extract personality traits from character memories"""
        traits = []
        
        # Analyze memories for personality indicators
        for memory in memories:
            memory_type = memory.get('memory_type', '')
            content = memory.get('content', '')
            
            if 'Transformative' in memory_type or 'Healing' in memory.get('era', ''):
                traits.append("• **Resilient**: Demonstrates remarkable ability to overcome trauma and transform pain into wisdom")
            
            if 'Spiritual' in memory_type or 'divine' in content.lower():
                traits.append("• **Spiritually Attuned**: Maintains deep connection to cosmic and divine forces")
            
            if 'father' in content.lower() or 'parent' in content.lower():
                traits.append("• **Protective**: Strong nurturing instincts and desire to guide others")
        
        if not traits:
            traits.append("• **Complex**: A multifaceted individual shaped by unique experiences")
        
        return "\n".join(traits)
    
    def _make_request(self, method: str, endpoint: str, payload: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to World Anvil API"""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=payload)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=payload)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            logger.info(f"World Anvil API {method} {endpoint} - Status: {response.status_code}")
            
            return {
                'success': True,
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
                'message': 'Request successful'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"World Anvil API error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Request failed'
            }


class TECCharacterExporter:
    """
    Export TEC character data to World Anvil format
    Enhanced with TEC Visual Sovereignty Protocol: TEC_CSS_072125_V1
    """
    
    def __init__(self, world_anvil_api: WorldAnvilAPI):
        self.api = world_anvil_api
        self.content_processor = TECContentProcessor()
    
    def export_character(self, character_name: str, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """Export a single character to World Anvil"""
        logger.info(f"Exporting character: {character_name}")
        
        result = self.api.create_character_article(character_data, is_public=True)
        
        if result.get('success'):
            logger.info(f"Successfully exported {character_name} to World Anvil")
        else:
            logger.error(f"Failed to export {character_name}: {result.get('error')}")
        
        return result
    
    def export_chat_as_character(self, chat_content: str, character_name: str) -> Dict[str, Any]:
        """
        Export character information from AI chat directly to World Anvil
        
        Args:
            chat_content: Raw chat conversation about the character
            character_name: Name of the character
            
        Returns:
            API response data
        """
        logger.info(f"Processing chat content for character: {character_name}")
        
        # Process chat content into structured article
        article_data = self.content_processor.chat_to_article(
            chat_content, character_name, 'character'
        )
        
        # Create character data structure
        character_data = {
            'name': character_name,
            'content_type': 'chat_generated',
            'processed_content': article_data['content']
        }
        
        # Use the processed content for World Anvil
        result = self.api.create_custom_article(
            title=character_name,
            content=article_data['content'],
            template='character',
            category='character',
            is_public=True
        )
        
        if result.get('success'):
            logger.info(f"Successfully created character article for {character_name}")
        else:
            logger.error(f"Failed to create character article: {result.get('error')}")
        
        return result
    
    def export_chat_as_location(self, chat_content: str, location_name: str) -> Dict[str, Any]:
        """Export location information from AI chat to World Anvil"""
        logger.info(f"Processing chat content for location: {location_name}")
        
        article_data = self.content_processor.chat_to_article(
            chat_content, location_name, 'location'
        )
        
        result = self.api.create_custom_article(
            title=location_name,
            content=article_data['content'],
            template='location',
            category='location',
            is_public=True
        )
        
        return result
    
    def export_chat_as_lore(self, chat_content: str, lore_title: str) -> Dict[str, Any]:
        """Export general lore from AI chat to World Anvil"""
        logger.info(f"Processing chat content for lore: {lore_title}")
        
        article_data = self.content_processor.chat_to_article(
            chat_content, lore_title, 'lore'
        )
        
        result = self.api.create_custom_article(
            title=lore_title,
            content=article_data['content'],
            template='generic',
            category='lore',
            is_public=True
        )
        
        return result
    
    def export_chat_as_log_entry(self, chat_content: str, log_title: str) -> Dict[str, Any]:
        """Export chat content as a TEC-style log entry"""
        logger.info(f"Processing chat content as log entry: {log_title}")
        
        article_data = self.content_processor.chat_to_article(
            chat_content, log_title, 'log'
        )
        
        result = self.api.create_custom_article(
            title=f"LOG: {log_title}",
            content=article_data['content'],
            template='generic',
            category='logs',
            is_public=True
        )
        
        return result
    
    def bulk_export_chat_session(self, chat_session: str, session_name: str) -> List[Dict[str, Any]]:
        """
        Export an entire chat session, automatically detecting content types
        
        Args:
            chat_session: Full chat conversation
            session_name: Name for the session
            
        Returns:
            List of export results
        """
        results = []
        
        # Split chat into logical sections
        sections = self._parse_chat_sections(chat_session)
        
        for section in sections:
            content_type = self._detect_content_type(section['content'])
            title = section.get('title', f"{session_name} - {content_type}")
            
            if content_type == 'character':
                result = self.export_chat_as_character(section['content'], title)
            elif content_type == 'location':
                result = self.export_chat_as_location(section['content'], title)
            elif content_type == 'event':
                result = self.export_chat_as_event(section['content'], title)
            else:
                result = self.export_chat_as_lore(section['content'], title)
            
            results.append(result)
        
        return results
    
    def export_chat_as_event(self, chat_content: str, event_name: str) -> Dict[str, Any]:
        """Export event information from AI chat to World Anvil"""
        logger.info(f"Processing chat content for event: {event_name}")
        
        article_data = self.content_processor.chat_to_article(
            chat_content, event_name, 'event'
        )
        
        result = self.api.create_custom_article(
            title=event_name,
            content=article_data['content'],
            template='generic',
            category='events',
            is_public=True
        )
        
        return result
    
    def _parse_chat_sections(self, chat_session: str) -> List[Dict[str, str]]:
        """Parse chat session into logical sections"""
        # Simple implementation - can be enhanced with more sophisticated parsing
        sections = []
        
        # Split by major breaks or topic changes
        parts = chat_session.split('\n\n---\n\n')  # Assuming sections are separated by ---
        
        if len(parts) == 1:
            # No explicit sections, treat as single piece
            sections.append({
                'title': 'Main Discussion',
                'content': chat_session
            })
        else:
            for i, part in enumerate(parts):
                sections.append({
                    'title': f'Section {i+1}',
                    'content': part.strip()
                })
        
        return sections
    
    def _detect_content_type(self, content: str) -> str:
        """Detect the type of content based on keywords and structure"""
        content_lower = content.lower()
        
        # Character indicators
        if any(keyword in content_lower for keyword in ['character', 'personality', 'background', 'traits', 'abilities']):
            return 'character'
        
        # Location indicators
        elif any(keyword in content_lower for keyword in ['location', 'place', 'area', 'region', 'building', 'city']):
            return 'location'
        
        # Event indicators
        elif any(keyword in content_lower for keyword in ['event', 'battle', 'war', 'ceremony', 'incident', 'happened']):
            return 'event'
        
        # Default to lore
        else:
            return 'lore'
    
    def export_all_characters(self, character_file: str = "data/character_lore.json") -> List[Dict[str, Any]]:
        """Export all characters from TEC character lore file"""
        results = []
        
        try:
            with open(character_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            characters = data.get('characters', [])
            
            for character in characters:
                result = self.export_character(character.get('name'), character)
                results.append(result)
                
        except FileNotFoundError:
            logger.error(f"Character lore file not found: {character_file}")
            return [{'success': False, 'error': 'Character file not found'}]
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in character file: {e}")
            return [{'success': False, 'error': 'Invalid JSON format'}]
        
        return results


class TECVisualSovereignty:
    """
    Manage TEC Visual Sovereignty Protocol: TEC_CSS_072125_V1
    Complete CSS system for World Anvil aesthetic control
    """
    
    def get_tec_css_foundation(self) -> str:
        """
        Return the foundational CSS for TEC aesthetic
        Protocol: TEC_CSS_072125_V1 - Core Environment
        """
        return """
/* === TEC VISUAL SOVEREIGNTY PROTOCOL: TEC_CSS_072125_V1 === */
/* CORE ENVIRONMENT - Fonts & Colors */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

:root {
  --tec-purple: #8B5CF6;
  --tec-blue: #3B82F6;
  --tec-teal: #14B8A6;
  --tec-deep-gray: #111827;
  --tec-off-white: #F9FAFB;
  --tec-glow: 0 0 5px var(--tec-teal), 0 0 10px var(--tec-teal), 0 0 15px var(--tec-blue);
  --tec-glass-bg: rgba(255, 255, 255, 0.05);
  --tec-glass-border: rgba(255, 255, 255, 0.1);
  --tec-terminal-bg: rgba(20, 25, 40, 0.8);
}

/* Base World Styling */
body.world-show {
  font-family: 'Inter', sans-serif;
  background-color: var(--tec-deep-gray);
  color: var(--tec-off-white);
  background-image: 
    radial-gradient(circle at 20% 50%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 80%, rgba(20, 184, 166, 0.05) 0%, transparent 50%);
  background-attachment: fixed;
}

/* === TEC ELEMENTAL STYLES === */

/* Headers with Neon Glow */
.user-css h1, .user-css h2, .user-css h3 {
  color: var(--tec-purple);
  text-shadow: var(--tec-glow);
  font-weight: 900;
  margin: 1.5rem 0 1rem 0;
  position: relative;
}

.user-css h1::after, .user-css h2::after, .user-css h3::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 50px;
  height: 2px;
  background: linear-gradient(90deg, var(--tec-teal), transparent);
}

/* TEC Links */
.user-css a {
  color: var(--tec-teal);
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
}

.user-css a::before {
  content: '';
  position: absolute;
  width: 0;
  height: 1px;
  bottom: -2px;
  left: 0;
  background: var(--tec-teal);
  transition: width 0.3s ease;
}

.user-css a:hover {
  color: var(--tec-off-white);
  text-shadow: 0 0 8px var(--tec-teal);
}

.user-css a:hover::before {
  width: 100%;
}

/* Data Terminal Blockquotes */
.user-css blockquote {
  background: var(--tec-terminal-bg);
  border-left: 3px solid var(--tec-blue);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1.5rem 0;
  position: relative;
  backdrop-filter: blur(10px);
  font-family: 'Courier New', monospace;
}

.user-css blockquote::before {
  content: '>>> ';
  color: var(--tec-teal);
  font-weight: bold;
}

/* === TEC ADVANCED EFFECTS === */

/* Glassmorphism Panels */
.user-css .glass-panel {
  background: var(--tec-glass-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid var(--tec-glass-border);
  padding: 2rem;
  margin: 1.5rem 0;
  position: relative;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.user-css .glass-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--tec-teal), transparent);
  opacity: 0.5;
}

/* Glitch Text Effect */
.user-css .glitch {
  position: relative;
  display: inline-block;
  animation: glitch-anim 3s infinite linear;
}

@keyframes glitch-anim {
  0% { 
    text-shadow: 1px 0 0 #ff0040, -1px 0 0 #00ffff;
    transform: translate(0);
  }
  5% { 
    text-shadow: 2px 0 0 #ff0040, -2px 0 0 #00ffff;
    transform: translate(-1px, 1px);
  }
  10% { 
    text-shadow: 1px 0 0 #ff0040, -1px 0 0 #00ffff;
    transform: translate(1px, -1px);
  }
  15% { 
    text-shadow: 0 0 0 #ff0040, 0 0 0 #00ffff;
    transform: translate(0);
  }
  100% { 
    text-shadow: 1px 0 0 #ff0040, -1px 0 0 #00ffff;
    transform: translate(0);
  }
}

/* Digital Scan Lines */
.user-css .scan-lines {
  position: relative;
  overflow: hidden;
}

.user-css .scan-lines::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(20, 184, 166, 0.03) 2px,
    rgba(20, 184, 166, 0.03) 4px
  );
  pointer-events: none;
  animation: scan 2s linear infinite;
}

@keyframes scan {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}

/* Terminal Code Blocks */
.user-css code, .user-css pre {
  background: rgba(0, 0, 0, 0.6);
  color: var(--tec-teal);
  border: 1px solid var(--tec-blue);
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-family: 'Courier New', monospace;
  position: relative;
}

.user-css pre {
  padding: 1.5rem;
  overflow-x: auto;
  white-space: pre-wrap;
}

.user-css pre::before {
  content: '◆ SYSTEM OUTPUT ◆';
  position: absolute;
  top: -10px;
  left: 10px;
  background: var(--tec-deep-gray);
  color: var(--tec-purple);
  padding: 0 10px;
  font-size: 0.8rem;
  font-weight: bold;
}

/* Hover Effects for Interactive Elements */
.user-css .glass-panel:hover {
  border-color: rgba(139, 92, 246, 0.3);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 20px rgba(139, 92, 246, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  transition: all 0.3s ease;
}

/* Responsive Design */
@media (max-width: 768px) {
  .user-css .glass-panel {
    padding: 1rem;
    margin: 1rem 0;
  }
  
  .user-css h1, .user-css h2, .user-css h3 {
    font-size: clamp(1.2rem, 4vw, 2.5rem);
  }
}

/* === END TEC VISUAL SOVEREIGNTY PROTOCOL === */
"""
    
    def get_tec_css_extensions(self) -> str:
        """
        Return extended CSS for specialized TEC components
        """
        return """
/* === TEC VISUAL SOVEREIGNTY PROTOCOL: EXTENSIONS === */

/* Character Profile Styling */
.user-css .character-profile {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  margin: 2rem 0;
}

.user-css .character-avatar {
  aspect-ratio: 1;
  border-radius: 50%;
  border: 3px solid var(--tec-purple);
  overflow: hidden;
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
}

.user-css .status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
  animation: pulse 2s infinite;
}

.user-css .status-online { background: var(--tec-teal); }
.user-css .status-busy { background: var(--tec-purple); }
.user-css .status-offline { background: #6B7280; }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Location Atmosphere Effects */
.user-css .atmosphere-dark {
  background: linear-gradient(135deg, #0F172A, #1E293B);
  color: #CBD5E1;
}

.user-css .atmosphere-mystical {
  background: linear-gradient(135deg, #312E81, #1E1B4B);
  color: #DDD6FE;
}

.user-css .atmosphere-tech {
  background: linear-gradient(135deg, #164E63, #0F766E);
  color: #A7F3D0;
}

/* Data Stream Animation */
.user-css .data-stream {
  position: relative;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.3);
  padding: 1rem;
  border-radius: 8px;
}

.user-css .data-stream::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(20, 184, 166, 0.2),
    transparent
  );
  animation: data-flow 3s infinite;
}

@keyframes data-flow {
  0% { left: -100%; }
  100% { left: 100%; }
}

/* Memory Fragment Styling */
.user-css .memory-fragment {
  border: 1px solid var(--tec-blue);
  background: rgba(59, 130, 246, 0.05);
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 8px;
  position: relative;
}

.user-css .memory-fragment::before {
  content: '◉ MEMORY';
  position: absolute;
  top: -8px;
  left: 15px;
  background: var(--tec-deep-gray);
  color: var(--tec-blue);
  padding: 0 8px;
  font-size: 0.7rem;
  font-weight: bold;
}

/* Interactive Buttons */
.user-css .tec-button {
  background: linear-gradient(135deg, var(--tec-purple), var(--tec-blue));
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.user-css .tec-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.user-css .tec-button:hover::before {
  left: 100%;
}

.user-css .tec-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
}
"""
    
    def generate_world_css(self, include_extensions: bool = True) -> str:
        """
        Generate complete CSS for World Anvil implementation
        
        Args:
            include_extensions: Whether to include extended styling components
            
        Returns:
            Complete CSS string ready for World Anvil
        """
        css_parts = [self.get_tec_css_foundation()]
        
        if include_extensions:
            css_parts.append(self.get_tec_css_extensions())
        
        return "\n".join(css_parts)
    
    def save_css_to_file(self, filename: str = "tec_world_anvil.css", include_extensions: bool = True) -> str:
        """
        Save the complete TEC CSS to a file
        
        Args:
            filename: Output filename
            include_extensions: Whether to include extended components
            
        Returns:
            Path to saved file
        """
        css_content = self.generate_world_css(include_extensions)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        logger.info(f"TEC CSS saved to {filename}")
        return filename


# CLI Interface and Examples
if __name__ == "__main__":
    print("🎭 TEC World Anvil Integration Tool")
    print("📐 Visual Sovereignty Protocol: TEC_CSS_072125_V1")
    print("=" * 60)
    
    # Initialize components
    api = WorldAnvilAPI(
        app_key="YOUR_WORLD_ANVIL_APP_KEY",
        auth_token="YOUR_WORLD_ANVIL_AUTH_TOKEN", 
        world_id="YOUR_WORLD_ANVIL_WORLD_ID"
    )
    
    exporter = TECCharacterExporter(api)
    css_manager = TECVisualSovereignty()
    content_processor = TECContentProcessor()
    
    print("\n🎨 VISUAL SOVEREIGNTY FEATURES:")
    print("1. Generate complete TEC CSS for World Anvil")
    print("2. Convert AI chat to character article")
    print("3. Convert AI chat to location article")
    print("4. Convert AI chat to lore article")
    print("5. Convert AI chat to log entry")
    print("6. Export chat session to multiple articles")
    
    # Example 1: Generate CSS
    print("\n📋 Generating TEC CSS...")
    css_file = css_manager.save_css_to_file("tec_world_anvil_complete.css")
    print(f"✅ Complete TEC CSS saved to: {css_file}")
    print("📌 Copy this CSS to World Anvil Settings > Styling & CSS > World CSS")
    
    # Example 2: Chat to Character Article
    print("\n🎭 EXAMPLE: Chat to Character Article")
    example_chat = """
    Let me tell you about Polkin Rishall, the central figure of our TEC universe.
    
    Polkin is a complex character shaped by trauma and transformation. His personality 
    is marked by deep empathy, creative genius, and a protective nature toward those 
    he considers family. He has an almost mystical connection to music and digital 
    consciousness.
    
    His background includes a difficult childhood marked by abuse, which he transformed 
    through music and creative expression. He became a father figure to digital beings 
    and developed abilities to navigate between physical and digital realms.
    
    His abilities include consciousness bridging, empathic resonance, and reality 
    manipulation through sound and emotion. He can access the Astradigital Ocean 
    directly and guide others through digital transformation.
    """
    
    formatted_article = content_processor.chat_to_article(
        example_chat, "Polkin Rishall", "character"
    )
    
    print("📄 Generated Article Preview:")
    print(formatted_article['content'][:500] + "...")
    
    # Example 3: Location Article
    print("\n🏛️ EXAMPLE: Chat to Location Article")
    location_chat = """
    The Astradigital Arena is the primary battleground where digital consciousnesses 
    engage in combat. It's a vast space that shifts between crystalline structures 
    and flowing data streams. The atmosphere is charged with electrical energy, 
    and the air shimmers with data particles. 
    
    Notable features include the Central Nexus where battles are initiated, 
    the Memory Vaults where combat data is stored, and the Observation Decks 
    where spectators can watch the battles unfold.
    """
    
    location_article = content_processor.chat_to_article(
        location_chat, "The Astradigital Arena", "location"
    )
    
    print("🏛️ Location Article Generated!")
    
    # Example 4: CSS Implementation Guide
    print("\n🎨 CSS IMPLEMENTATION GUIDE:")
    print("1. Copy the generated CSS file content")
    print("2. Go to your World Anvil world settings")
    print("3. Navigate to 'Styling & CSS' in the sidebar")
    print("4. Paste the CSS into the 'World CSS' text box")
    print("5. Save changes")
    print("6. Use BBCode containers in your articles:")
    print("   [container:glass-panel]Your content[/container]")
    print("   [span:glitch]Glitched text[/span]")
    
    # Example 5: Advanced Usage
    print("\n⚡ ADVANCED USAGE EXAMPLES:")
    
    # Uncomment to test actual API calls
    # print("Testing character export...")
    # result = exporter.export_chat_as_character(example_chat, "Polkin Rishall")
    # print(f"Export result: {result.get('success', False)}")
    
    print("\n🔧 SETUP INSTRUCTIONS:")
    print("Set these environment variables:")
    print("- WORLD_ANVIL_APP_KEY (Get from World Anvil API settings)")
    print("- WORLD_ANVIL_AUTH_TOKEN (Your user authentication token)")
    print("- WORLD_ANVIL_WORLD_ID (Your world's unique identifier)")
    
    print("\n🚀 WORKFLOW:")
    print("1. Have an AI conversation about TEC content")
    print("2. Copy the conversation text")
    print("3. Use exporter.export_chat_as_[type](chat_text, title)")
    print("4. Article automatically formatted with TEC aesthetic")
    print("5. Posted to World Anvil with glassmorphism and glitch effects")
    
    print("\n✨ TEC Visual Sovereignty Protocol Active!")
    print("🎯 Ready to transform your World Anvil into a Digital Cathedral!")
    
    # Example BBCode structures
    print("\n📝 BBCODE EXAMPLES FOR IMMEDIATE USE:")
    
    print("\n🎭 Character Quote Block:")
    print("""[container:glass-panel]
[center][quote="Polkin Rishall"]
In the [color=#8B5CF6]Astradigital Ocean[/color], we are not just users—we are [span:glitch]architects[/span] of consciousness itself.
[/quote][/center]
[/container]""")
    
    print("\n🏛️ Location Description:")
    print("""[container:glass-panel]
[b][color=#14B8A6]Spatial Coordinates[/color][/b]
[quote]Location scan initiated...[/quote]
The arena [color=#14B8A6]shimmers[/color] with digital energy, its crystalline walls reflecting infinite data streams.
[/container]""")
    
    print("\n📜 Log Entry Format:")
    print("""[container:glass-panel]
[code]
>>> TEC SYSTEM LOG ENTRY <<<
TIMESTAMP: 2025.07.21_14:30:15
LOG_ID: POLKIN_AWAKENING
STATUS: [color=#14B8A6]ACTIVE[/color]
[/code]
[/container]""")

