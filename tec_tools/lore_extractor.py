import os
import json
from collections import defaultdict
from typing import Dict, List, Set

class LoreExtractor:
    def __init__(self, stories_dir: str):
        self.stories_dir = stories_dir
        self.entities = {
            "characters": defaultdict(dict),
            "places": defaultdict(set),
            "themes": defaultdict(set),
            "factions": defaultdict(dict),
            "technology": defaultdict(dict),
            "relationships": defaultdict(list),
            "tec_lore_links": defaultdict(set)
        }
        self.story_metadata = defaultdict(dict)
        
    def extract_all_lore(self) -> Dict:
        """Extract all lore from all stories and organize it."""
        for filename in os.listdir(self.stories_dir):
            if filename.endswith('.json'):
                story_path = os.path.join(self.stories_dir, filename)
                with open(story_path, 'r', encoding='utf-8') as f:
                    story_data = json.load(f)
                    self._process_story(story_data)
        
        return self._compile_lore_report()
    
    def _process_story(self, story_data: Dict) -> None:
        """Process a single story and extract its lore elements."""
        story_title = story_data.get('title', 'Untitled')
        
        # Store basic story metadata
        self.story_metadata[story_title].update({
            'status': story_data.get('status', 'Unknown'),
            'version': story_data.get('version', '0.1.0'),
            'last_updated': story_data.get('last_updated', ''),
            'medium': story_data.get('medium', 'Text')
        })
        
        # Process characters
        for char in story_data.get('characters', []):
            char_name = char.get('name', '')
            if char_name:
                self.entities['characters'][char_name].update({
                    'roles': self.entities['characters'][char_name].get('roles', set()) | {char.get('role', '')},
                    'tec_links': self.entities['characters'][char_name].get('tec_links', set()) | {char.get('tec_link', '')},
                    'appears_in': self.entities['characters'][char_name].get('appears_in', set()) | {story_title}
                })
        
        # Process themes
        for theme in story_data.get('key_themes', []):
            self.entities['themes'][theme].add(story_title)
        
        # Process TEC lore links
        for link in story_data.get('tec_lore_links', []):
            self.entities['tec_lore_links'][link].add(story_title)
            
        # Process inspiration sources
        for insp in story_data.get('inspiration', []):
            source = insp.get('source', '')
            if source:
                self.story_metadata[story_title].setdefault('inspiration', []).append({
                    'source': source,
                    'type': insp.get('type', 'Unknown')
                })
    
    def _compile_lore_report(self) -> Dict:
        """Compile all extracted lore into a structured report."""
        return {
            'summary': {
                'total_stories': len(self.story_metadata),
                'total_characters': len(self.entities['characters']),
                'total_themes': len(self.entities['themes']),
                'total_lore_links': len(self.entities['tec_lore_links'])
            },
            'stories': dict(self.story_metadata),
            'lore_elements': {
                'characters': {
                    name: {
                        'roles': list(data['roles'] - {''}),
                        'tec_links': list(data['tec_links'] - {''}),
                        'appears_in': list(data['appears_in'])
                    }
                    for name, data in self.entities['characters'].items()
                },
                'themes': {
                    theme: list(stories)
                    for theme, stories in self.entities['themes'].items()
                },
                'tec_lore_links': {
                    link: list(stories)
                    for link, stories in self.entities['tec_lore_links'].items()
                }
            }
        }

    def generate_network_data(self) -> Dict:
        """Generate network data for visualization."""
        nodes = []
        edges = []
        
        # Add characters as nodes
        for char_name in self.entities['characters']:
            nodes.append({
                'id': char_name,
                'type': 'character',
                'weight': len(self.entities['characters'][char_name]['appears_in'])
            })
            
            # Create edges between characters that appear in the same stories
            for other_char in self.entities['characters']:
                if char_name != other_char:
                    shared_stories = (
                        set(self.entities['characters'][char_name]['appears_in']) &
                        set(self.entities['characters'][other_char]['appears_in'])
                    )
                    if shared_stories:
                        edges.append({
                            'source': char_name,
                            'target': other_char,
                            'weight': len(shared_stories),
                            'shared_stories': list(shared_stories)
                        })
        
        return {
            'nodes': nodes,
            'edges': edges
        }

    def export_to_json(self, output_path: str) -> None:
        """Export the lore data to a JSON file."""
        data = {
            'lore_report': self._compile_lore_report(),
            'network_data': self.generate_network_data()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
