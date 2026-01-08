#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.api.meta_api import MetaAPIClient
import json

api = MetaAPIClient()

print("Načítám stories...")
stories = api.get_instagram_stories()

if stories:
    print(f"\nNalezeno {len(stories)} stories:\n")
    for i, story in enumerate(stories, 1):
        print(f"Story {i}:")
        print(f"  ID: {story.get('id')}")
        print(f"  Caption: '{story.get('caption', '')}'")
        print(f"  Timestamp: {story.get('timestamp')}")
        print(f"  Media Type: {story.get('media_type')}")
        print()

        # Získat detaily
        details = api.get_story_details_with_tags(story.get('id'))
        if details:
            print(f"  Details:")
            print(f"    Caption (from details): '{details.get('caption', '')}'")
            print(f"    Owner: {details.get('owner')}")
            print(f"    Username: {details.get('username')}")
        print("-" * 60)
else:
    print("Žádné aktivní stories")
