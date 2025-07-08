import os
import json
import time
from datetime import datetime
from .lore_extractor import LoreExtractor

LORE_STREAM_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lore_stream.json')

class LoreStream:
    def __init__(self, stories_dir: str):
        self.stories_dir = stories_dir
        self.lore_extractor = LoreExtractor(stories_dir)
        self.last_snapshot = {}

    def scan_and_update(self):
        """Scan stories, update the lore stream with new/changed entries."""
        current_lore = self.lore_extractor.extract_all_lore()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = {
            'timestamp': timestamp,
            'lore_report': current_lore
        }
        # Append to lore_stream.json
        if os.path.exists(LORE_STREAM_FILE):
            with open(LORE_STREAM_FILE, 'r', encoding='utf-8') as f:
                stream = json.load(f)
        else:
            stream = []
        stream.append(entry)
        with open(LORE_STREAM_FILE, 'w', encoding='utf-8') as f:
            json.dump(stream, f, indent=4, ensure_ascii=False)
        print(f"Lore stream updated at {timestamp}.")

    def run_periodic(self, interval=300):
        """Run periodic lore stream updates (default: every 5 minutes)."""
        print(f"Starting lore stream. Updating every {interval} seconds...")
        try:
            while True:
                self.scan_and_update()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Lore stream stopped.")

if __name__ == "__main__":
    stories_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tec_stories')
    lore_stream = LoreStream(stories_dir)
    lore_stream.scan_and_update()
