import os
import json
from datetime import datetime
from .lore_extractor import LoreExtractor

def analyze_stories():
    """Generate a comprehensive analysis of all stories and their lore."""
    stories_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tec_stories')
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tec_analysis')
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize the lore extractor
    extractor = LoreExtractor(stories_dir)
    
    # Generate timestamp for the analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f'lore_analysis_{timestamp}.json')
    
    # Export the analysis
    extractor.export_to_json(output_file)
    print(f"Analysis exported to: {output_file}")

def generate_story_stats():
    """Generate statistics about story progression and themes."""
    stories_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tec_stories')
    stats = {
        'total_stories': 0,
        'status_breakdown': {},
        'theme_frequency': {},
        'character_appearances': {},
        'medium_breakdown': {},
        'timeline': []
    }
    
    for filename in os.listdir(stories_dir):
        if filename.endswith('.json'):
            with open(os.path.join(stories_dir, filename), 'r', encoding='utf-8') as f:
                story = json.load(f)
                
                # Increment total stories
                stats['total_stories'] += 1
                
                # Update status breakdown
                status = story.get('status', 'Unknown')
                stats['status_breakdown'][status] = stats['status_breakdown'].get(status, 0) + 1
                
                # Update theme frequency
                for theme in story.get('key_themes', []):
                    stats['theme_frequency'][theme] = stats['theme_frequency'].get(theme, 0) + 1
                
                # Update character appearances
                for char in story.get('characters', []):
                    char_name = char.get('name', '')
                    if char_name:
                        stats['character_appearances'][char_name] = stats['character_appearances'].get(char_name, 0) + 1
                
                # Update medium breakdown
                medium = story.get('medium', 'Unknown')
                stats['medium_breakdown'][medium] = stats['medium_breakdown'].get(medium, 0) + 1
                
                # Add to timeline
                stats['timeline'].append({
                    'title': story.get('title', 'Untitled'),
                    'last_updated': story.get('last_updated', ''),
                    'status': status,
                    'version': story.get('version', '0.1.0')
                })
    
    # Sort timeline by last_updated date
    stats['timeline'].sort(key=lambda x: x['last_updated'] if x['last_updated'] else '')
    
    return stats

def main():
    """Main function to run all analysis tools."""
    print("Starting TEC lore analysis...")
    analyze_stories()
    
    print("\nGenerating story statistics...")
    stats = generate_story_stats()
    
    # Print summary
    print("\n=== TEC Story Analysis Summary ===")
    print(f"Total Stories: {stats['total_stories']}")
    print("\nStatus Breakdown:")
    for status, count in stats['status_breakdown'].items():
        print(f"  {status}: {count}")
    
    print("\nMost Common Themes:")
    sorted_themes = sorted(stats['theme_frequency'].items(), key=lambda x: x[1], reverse=True)[:5]
    for theme, count in sorted_themes:
        print(f"  {theme}: {count}")
    
    print("\nMost Frequent Characters:")
    sorted_chars = sorted(stats['character_appearances'].items(), key=lambda x: x[1], reverse=True)[:5]
    for char, count in sorted_chars:
        print(f"  {char}: {count} appearances")

if __name__ == "__main__":
    main()
