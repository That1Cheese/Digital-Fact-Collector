"""
Digital Fact Collector
A tool that automatically fetches, stores, and manages interesting facts from an API.
"""

import requests
import json
import os
from datetime import datetime
import time
import schedule


class FactCollector:
    def __init__(self, storage_file="facts_database.json"):
        """Initialize the Fact Collector with a storage file."""
        self.storage_file = storage_file
        self.facts = self.load_facts()

    def load_facts(self):
        """Load existing facts from the JSON storage file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not read {self.storage_file}. Starting with empty database.")
                return []
        return []

    def save_facts(self):
        """Save facts to the JSON storage file."""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.facts, f, indent=2, ensure_ascii=False)
        print(f"Database saved: {len(self.facts)} facts stored")

    def fetch_fact_from_api(self):
        """Fetch a random fact from an online API."""
        try:
            # Using the "uselessfacts" API - free and no authentication required
            response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random", timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('text', '').strip()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching fact: {e}")
            return None

    def is_duplicate(self, new_fact):
        """Check if a fact already exists in the database."""
        # Normalize the fact text for comparison (lowercase, strip whitespace)
        normalized_new = new_fact.lower().strip()

        for fact_entry in self.facts:
            normalized_existing = fact_entry.get('fact', '').lower().strip()
            if normalized_new == normalized_existing:
                return True
        return False

    def add_fact(self, fact_text):
        """Add a new fact to the database if it's not a duplicate."""
        if not fact_text:
            print("Empty fact received, skipping.")
            return False

        if self.is_duplicate(fact_text):
            print(f"Duplicate detected: '{fact_text[:50]}...'")
            return False

        # Create a fact entry with metadata
        fact_entry = {
            "fact": fact_text,
            "date_added": datetime.now().isoformat(),
            "id": len(self.facts) + 1
        }

        self.facts.append(fact_entry)
        self.save_facts()
        print(f"✓ New fact added! (#{fact_entry['id']})")
        print(f"  {fact_text[:100]}...")
        return True

    def collect_fact(self):
        """Fetch a fact from the API and add it to the database."""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Collecting fact...")
        fact = self.fetch_fact_from_api()

        if fact:
            self.add_fact(fact)
        else:
            print("Failed to fetch a fact.")

    def display_stats(self):
        """Display statistics about the fact collection."""
        print("\n" + "="*60)
        print("DIGITAL FACT COLLECTOR - STATISTICS")
        print("="*60)
        print(f"Total facts in database: {len(self.facts)}")

        if self.facts:
            first_fact = self.facts[0]
            last_fact = self.facts[-1]
            print(f"First fact added: {first_fact.get('date_added', 'Unknown')}")
            print(f"Latest fact added: {last_fact.get('date_added', 'Unknown')}")
            print(f"\nMost recent fact:")
            print(f"  {last_fact.get('fact', 'N/A')}")
        print("="*60 + "\n")

    def run_scheduled(self, interval_minutes=5):
        """Run the fact collector on a schedule."""
        print(f"Starting Digital Fact Collector...")
        print(f"Will fetch a new fact every {interval_minutes} minute(s)")
        print("Press Ctrl+C to stop\n")

        # Collect one fact immediately
        self.collect_fact()
        self.display_stats()

        # Schedule regular collections
        schedule.every(interval_minutes).minutes.do(self.collect_fact)

        # Keep the scheduler running
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nStopping Digital Fact Collector...")
            self.display_stats()
            print("Goodbye!")


def main():
    """Main entry point for the application."""
    print("="*60)
    print("     DIGITAL FACT COLLECTOR")
    print("="*60)

    collector = FactCollector()

    # Display current stats
    if collector.facts:
        collector.display_stats()

    # Menu
    print("\nOptions:")
    print("1. Collect one fact now")
    print("2. Run automated collection (every 5 minutes)")
    print("3. View all facts")
    print("4. Exit")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "1":
        collector.collect_fact()
        collector.display_stats()
    elif choice == "2":
        collector.run_scheduled(interval_minutes=5)
    elif choice == "3":
        if collector.facts:
            print("\n" + "="*60)
            print("ALL FACTS IN DATABASE")
            print("="*60)
            for fact_entry in collector.facts:
                print(f"\n[{fact_entry.get('id')}] {fact_entry.get('date_added', 'Unknown')}")
                print(f"  {fact_entry.get('fact')}")
            print("="*60)
        else:
            print("\nNo facts in database yet!")
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
