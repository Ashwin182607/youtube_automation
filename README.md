An automated system for creating and uploading chill music videos to YouTube with a modern GUI interface. 
(NOT A PERFECT PROJECT STILL HAS MY TESTING BITS)
(Note: You can devlop it however you like The project may not be updated frequently due to my current exam schedule, but contributions are still welcome and will be reviewed as time permits!)
## Features

- Modern dark-themed GUI interface
- Video creation with customizable effects:
  - Fade in/out
  - Zoom effects
  - Blur
  - Color adjustments
  - Vignette
  - Wave effects
- Direct YouTube upload integration
- Support for low-end devices
- Background image customization
- Multiple resolution support (480p, 720p, 1080p)

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd youtube_automation
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up YouTube API:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable YouTube Data API v3
   - Create OAuth 2.0 credentials
   - Download the client secrets file and save as `client_secrets.json` in the project root

## Directory Structure

```
youtube_automation/
├── media/
│   ├── music/
│   │   ├── to_process/    # Place your MP3 files here
│   │   └── processed/     # Processed videos will be here
│   └── backgrounds/       # Background images
├── src/
│   ├── music_video_creator.py
│   ├── video_effects.py
│   └── youtube_uploader.py
├── config.py
├── requirements.txt
└── README.md
```

## Usage

1. Run the GUI:
```bash
python gui.py
```

2. Select an MP3 file using the "Browse" button
3. (Optional) Choose a custom background image
4. Adjust video settings and effects
5. Click "Create Video" to generate the video
6. (Optional) Upload directly to YouTube

## Configuration

- Edit `config.py` to change default settings
- Place default background images in `media/backgrounds/`
- Supported music formats: MP3
- Supported image formats: JPG, PNG

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
