import os
from moviepy.editor import AudioFileClip, ImageClip, TextClip, CompositeVideoClip
from config import DEFAULT_BG, BACKGROUNDS_DIR
from PIL import Image

class ChillMusicVideoCreator:
    def __init__(self, background_image_path=None):
        if background_image_path:
            self.background_image_path = background_image_path
        else:
            default_bg = os.path.join(BACKGROUNDS_DIR, DEFAULT_BG)
            if not os.path.exists(default_bg):
                raise FileNotFoundError(f"Background image not found at {default_bg}")
            self.background_image_path = default_bg

    def create_video(self, audio_path, output_path, title="", artist="", 
                    width=1280, fps=24, title_size=60, artist_size=30, 
                    text_color="white"):
        """
        Create a music video with customizable settings.
        
        Parameters:
        - audio_path: Path to the MP3 file
        - output_path: Where to save the video
        - title: Song title
        - artist: Artist name
        - width: Video width (height will be calculated)
        - fps: Frames per second
        - title_size: Font size for title
        - artist_size: Font size for artist name
        - text_color: Color for text overlays
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found at {audio_path}")
        if not os.path.exists(self.background_image_path):
            raise FileNotFoundError(f"Background image not found at {self.background_image_path}")

        try:
            # Load audio
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration

            # Create background - handle ANTIALIAS deprecation
            bg_img = Image.open(self.background_image_path)
            ratio = width / bg_img.width
            target_height = int(bg_img.height * ratio)
            resampling_method = getattr(Image, 'Resampling', Image).LANCZOS
            bg_img = bg_img.resize((width, target_height), resampling_method)
            bg_img.save('temp_bg.jpg')
            
            background = ImageClip('temp_bg.jpg')
            background = background.set_duration(duration)

            # Create text clips
            clips = [background]
            
            if title:
                title_clip = TextClip(
                    title, 
                    fontsize=title_size, 
                    color=text_color, 
                    font='Arial',
                    stroke_color='black', 
                    stroke_width=2
                ).set_position(('center', 0.4), relative=True).set_duration(duration)
                clips.append(title_clip)

            if artist:
                artist_clip = TextClip(
                    artist, 
                    fontsize=artist_size, 
                    color=text_color, 
                    font='Arial',
                    stroke_color='black', 
                    stroke_width=1
                ).set_position(('center', 0.5), relative=True).set_duration(duration)
                clips.append(artist_clip)

            # Compose final video
            video = CompositeVideoClip(clips)
            video = video.set_audio(audio_clip)

            # Create output directory if needed
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

            # Write video with minimal settings
            print("Creating video...")
            video.write_videofile(
                output_path,
                fps=fps,
                codec='libx264',
                audio_codec='aac',
                bitrate='2000k',
                threads=2,
                preset='ultrafast'
            )
            
            # Clean up temporary file
            if os.path.exists('temp_bg.jpg'):
                os.remove('temp_bg.jpg')
            
        except Exception as e:
            print(f"Error creating video: {str(e)}")
            # Clean up temporary file in case of error
            if os.path.exists('temp_bg.jpg'):
                os.remove('temp_bg.jpg')
            raise

class ShortsVideoCreator:
    def __init__(self, background_image_path=None):
        if background_image_path:
            self.background_image_path = background_image_path
        else:
            default_bg = os.path.join(BACKGROUNDS_DIR, DEFAULT_BG)
            if not os.path.exists(default_bg):
                raise FileNotFoundError(f"Background image not found at {default_bg}")
            self.background_image_path = default_bg

    def create_short(self, audio_path, output_path, title="", caption="", max_duration=60):
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found at {audio_path}")
        if not os.path.exists(self.background_image_path):
            raise FileNotFoundError(f"Background image not found at {self.background_image_path}")

        try:
            # Load and trim audio if needed
            audio_clip = AudioFileClip(audio_path)
            if audio_clip.duration > max_duration:
                audio_clip = audio_clip.subclip(0, max_duration)
            duration = audio_clip.duration

            # Create background with vertical orientation (1080x1920 for best quality)
            bg_img = Image.open(self.background_image_path)
            target_height = 1920
            target_width = 1080
            
            if bg_img.width / bg_img.height > 9/16:  # image is too wide
                new_height = target_height
                new_width = int(new_height * (bg_img.width / bg_img.height))
                bg_img = bg_img.resize((new_width, new_height))
                # Center crop
                x_center = new_width // 2
                bg_img = bg_img.crop((x_center - target_width//2, 0, x_center + target_width//2, target_height))
            else:  # image is too tall
                new_width = target_width
                new_height = int(new_width / (bg_img.width / bg_img.height))
                bg_img = bg_img.resize((new_width, new_height))
                # Center crop
                y_center = new_height // 2
                bg_img = bg_img.crop((0, y_center - target_height//2, target_width, y_center + target_height//2))

            bg_img.save('temp_bg.jpg')
            
            background = ImageClip('temp_bg.jpg')
            background = background.set_duration(duration)

            # Create text clips
            clips = [background]
            
            if title:
                title_clip = TextClip(
                    title, fontsize=80, color='white', font='Arial',
                    stroke_color='black', stroke_width=2,
                    size=(1000, None), method='caption'
                ).set_position(('center', 0.1), relative=True).set_duration(duration)
                clips.append(title_clip)

            if caption:
                caption_clip = TextClip(
                    caption, fontsize=50, color='white', font='Arial',
                    stroke_color='black', stroke_width=1,
                    size=(900, None), method='caption'
                ).set_position(('center', 0.85), relative=True).set_duration(duration)
                clips.append(caption_clip)

            # Compose final video
            video = CompositeVideoClip(clips, size=(1080, 1920))
            video = video.set_audio(audio_clip)

            # Write the final video
            video.write_videofile(
                output_path,
                fps=30,
                codec='libx264',
                audio_codec='aac',
                preset='medium'
            )
            
            # Clean up
            video.close()
            audio_clip.close()
            background.close()
            if title:
                title_clip.close()
            if caption:
                caption_clip.close()

            # Clean up temporary file
            if os.path.exists('temp_bg.jpg'):
                os.remove('temp_bg.jpg')

            return True

        except Exception as e:
            print(f"Error creating video: {str(e)}")
            # Clean up temporary file in case of error
            if os.path.exists('temp_bg.jpg'):
                os.remove('temp_bg.jpg')
            return False

if __name__ == "__main__":
    # Example usage
    creator = ChillMusicVideoCreator()
    creator.create_video(
        audio_path="path_to_your_music.mp3",
        output_path="output_video.mp4",
        title="Chill Vibes",
        artist="Artist Name"
    )

    # Example usage for ShortsVideoCreator
    shorts_creator = ShortsVideoCreator()
    shorts_creator.create_short(
        audio_path="path/to/audio.mp3",
        output_path="output_short.mp4",
        title="Amazing Short!",
        caption="#shorts #viral #trending"
    )