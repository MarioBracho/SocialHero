#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.database.db_manager import DatabaseManager

db = DatabaseManager()
db.connect()
influencers = db.get_all_influencers()

for i in influencers:
    print(f"ID: {i['id']}, Jméno: {i['jmeno']}, Handle: {i.get('instagram_handle', 'N/A')}")

db.close()
