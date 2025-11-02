# Digital Fact Collector

An automated tool that discovers, collects, and organizes a unique database of interesting facts from an online API.

## Features

- **Automation**: Automatically fetch facts at scheduled intervals
- **Data Storage**: Facts saved in JSON format for persistence
- **Data Management**: Organized, structured storage with metadata
- **Data Quality**: Duplicate detection ensures unique facts only
- **Data Exchange**: Uses JSON for easy data interchange

## Installation

1. Make sure Python 3.7+ is installed on your system
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the program:

```bash
python fact_collector.py
```

### Menu Options

1. **Collect one fact now**: Fetch a single fact immediately
2. **Run automated collection**: Continuously collect facts every 5 minutes
3. **View all facts**: Display your entire fact database
4. **Exit**: Close the application

## How It Works

1. The program fetches random facts from the Useless Facts API
2. Each fact is checked against the existing database for duplicates
3. If the fact is new, it's added with metadata (timestamp, unique ID)
4. All facts are stored in `facts_database.json`
5. In automated mode, facts are collected every 5 minutes

## Project Learning Objectives

This project demonstrates:

- **Automation**: Using the `schedule` library to run tasks at intervals
- **Data Storage**: Reading/writing JSON files to persist data
- **Data Management**: Organizing facts with IDs and timestamps
- **Data Quality**: Implementing duplicate detection logic
- **Data Exchange**: Working with APIs and JSON format

## File Structure

- `fact_collector.py`: Main application code
- `requirements.txt`: Python dependencies
- `facts_database.json`: Stored facts (created automatically)

## API Source

Facts are fetched from: https://uselessfacts.jsph.pl/api/v2/facts/random
