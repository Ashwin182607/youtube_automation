import os
import time
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from music_video_creator import ShortsVideoCreator
from youtube_uploader import YouTubeUploader
from config import MUSIC_DIR, BACKGROUNDS_DIR
import eyed3  # for reading MP3 metadata

# Create directories for content to be processed
TO_PROCESS_DIR = os.path.join(MUSIC_DIR, 'to_process')
PROCESSED_DIR = os.path.join(MUSIC_DIR, 'processed')
UPLOAD_LOG = 'upload_log.json'

class ShortsFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.creator = ShortsVideoCreator()
        self.uploader = YouTubeUploader()
        self.upload_history = self.load_upload_history()
        
        # Create necessary directories
        os.makedirs(TO_PROCESS_DIR, exist_ok=True)
        os.makedirs(PROCESSED_DIR, exist_ok=True)

    def load_upload_history(self):
        if os.path.exists(UPLOAD_LOG):
            with open(UPLOAD_LOG, 'r') as f:
                return json.load(f)
        return {}

    def save_upload_history(self):
        with open(UPLOAD_LOG, 'w') as f:
            json.dump(self.upload_history, f, indent=4)

    def get_metadata(self, audio_path):
        """Extract metadata from audio file"""
        audiofile = eyed3.load(audio_path)
        if audiofile and audiofile.tag:
            return {
                'title': audiofile.tag.title or os.path.splitext(os.path.basename(audio_path))[0],
                'description': audiofile.tag.comment or "",
                'tags': ['shorts', 'viral', 'trending']  # Default tags for Shorts
            }
        return {
            'title': os.path.splitext(os.path.basename(audio_path))[0],
            'description': "Check out this awesome Short! #shorts",
            'tags': ['shorts', 'viral', 'trending']
        }

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.mp3', '.wav', '.m4a')):
            try:
                # Get file info
                audio_path = event.src_path
                filename = os.path.basename(audio_path)
                output_path = os.path.join(PROCESSED_DIR, f"{os.path.splitext(filename)[0]}_short.mp4")

                # Check if already processed
                if filename in self.upload_history:
                    print(f"File {filename} already processed. Skipping...")
                    return

                # Get metadata
                metadata = self.get_metadata(audio_path)
                
                # Create short video
                print(f"Creating Short for {filename}...")
                success = self.creator.create_short(
                    audio_path=audio_path,
                    output_path=output_path,
                    title=metadata['title'],
                    caption=f"#shorts {' '.join(['#' + tag for tag in metadata['tags']])}"
                )

                if success:
                    # Upload to YouTube
                    print(f"Uploading {filename} to YouTube...")
                    video_id = self.uploader.upload(
                        output_path,
                        title=f"{metadata['title']} #shorts",
                        description=metadata['description'],
                        tags=metadata['tags'],
                        made_for_kids=False
                    )

                    if video_id:
                        # Log successful upload
                        self.upload_history[filename] = {
                            'video_id': video_id,
                            'upload_time': datetime.now().isoformat(),
                            'title': metadata['title']
                        }
                        self.save_upload_history()
                        print(f"Successfully uploaded Short: {metadata['title']}")
                        
                        # Move processed file
                        processed_audio = os.path.join(PROCESSED_DIR, filename)
                        os.rename(audio_path, processed_audio)
                    else:
                        print(f"Failed to upload {filename}")
                else:
                    print(f"Failed to create Short for {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

def main():
    handler = ShortsFileHandler()
    observer = Observer()
    observer.schedule(handler, TO_PROCESS_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()