import argparse
import lyricsgenius
from typing import Optional
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API token from environment variable
GENIUS_API_TOKEN = os.getenv('GENIUS_API_TOKEN')

if not GENIUS_API_TOKEN:
    raise ValueError("GENIUS_API_TOKEN not found in environment variables. Please check your .env file.")

def fetch_lyrics(song_name: str, artist_name: Optional[str] = None) -> Optional[str]:
    """
    Fetch lyrics for a given song and optionally filter by artist
    """
    genius = lyricsgenius.Genius(GENIUS_API_TOKEN)
    
    try:
        if artist_name:
            song = genius.search_song(song_name, artist_name)
        else:
            song = genius.search_song(song_name)
        
        if song:
            return song.lyrics
        return None
    except Exception as e:
        print(f"Error fetching lyrics: {e}")
        return None

def save_lyrics(lyrics: str, song_name: str):
    """
    Save lyrics to a file named after the song in the songs directory
    """
    # Create songs directory if it doesn't exist
    songs_dir = os.path.abspath('songs')
    os.makedirs(songs_dir, exist_ok=True)
    
    # Replace spaces with underscores and remove any special characters
    filename = song_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    filepath = os.path.join(songs_dir, f"{filename}.txt")
    
    print(f"Saving lyrics to: {filepath}")  # Debug info
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(lyrics)
    return filepath


def process_song_list(file_path: str):
    """
    Process a text file containing song names and optional artists
    Format: 'song_name' or 'song_name|artist_name' (one per line)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_songs = len(lines)
        successful = 0
        
        print(f"Found {total_songs} songs to process")
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            parts = line.split('|')
            song_name = parts[0].strip()
            artist_name = parts[1].strip() if len(parts) > 1 else None
            
            print(f"\nProcessing {i}/{total_songs}: {song_name}" + 
                  (f" by {artist_name}" if artist_name else ""))
            
            lyrics = fetch_lyrics(song_name, artist_name)
            if lyrics:
                filename = save_lyrics(lyrics, song_name)
                print(f"✓ Saved lyrics to {filename}")
                successful += 1
            else:
                print(f"✗ Could not find lyrics for {song_name}")
            
            # Add a small delay to avoid hitting API rate limits
            time.sleep(1)
        
        print(f"\nProcessing complete! Successfully fetched {successful}/{total_songs} songs")
        
    except FileNotFoundError:
        print(f"Error: Could not find file {file_path}")
    except Exception as e:
        print(f"Error processing song list: {e}")

def main():
    parser = argparse.ArgumentParser(description='Fetch song lyrics and save them to files')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--song', help='Name of the song')
    group.add_argument('--file', help='Path to text file containing list of songs')
    parser.add_argument('--artist', help='Name of the artist (optional)', default=None)
    
    args = parser.parse_args()
    
    if args.file:
        process_song_list(args.file)
    else:
        lyrics = fetch_lyrics(args.song, args.artist)
        if lyrics:
            filename = save_lyrics(lyrics, args.song)
            print(f"Lyrics saved to {filename}")
        else:
            print("Could not find lyrics for the specified song")

if __name__ == "__main__":
    main()