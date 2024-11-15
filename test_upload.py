from music_video_creator import ChillMusicVideoCreator
import os
from config import MUSIC_DIR, BACKGROUNDS_DIR

def test_video_creation():
    # Test music file
    music_file = os.path.join(MUSIC_DIR, "Neon Dreams of Paris.mp3")
    
    # Output path
    output_path = os.path.join(MUSIC_DIR, "test_output.mp4")
    
    # Create video with enhanced visualization
    creator = ChillMusicVideoCreator()
    creator.create_video(
        music_file,
        output_path,
        title="Neon Dreams of Paris",
        artist="Chill Vibes"
    )
    
    print(f"Video created at: {output_path}")

if __name__ == "__main__":
    test_video_creation()