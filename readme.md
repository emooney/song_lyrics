# Lyrics Fetcher

A simple Python application that fetches song lyrics using the Genius API and saves them to text files.

## Features

- Fetch lyrics for any song from Genius
- Optional artist name filtering
- Batch processing of multiple songs from a text file
- Automatically saves lyrics to text files named after each song
- Handles special characters and spaces in filenames
- Supports Unicode for international songs
- Progress tracking for batch operations
- Secure API token management using .env

## Run
python fetch_lyrics.py --file songs.list

## Prerequisites

- Python 3.6 or higher
- Genius API token (get it from https://genius.com/api-clients)

## Installation

1. Clone this repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt