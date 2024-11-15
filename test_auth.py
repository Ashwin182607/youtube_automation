from youtube_uploader import YouTubeUploader

# Create uploader instance
uploader = YouTubeUploader()

# This will trigger the authentication process
uploader.authenticate()

print("Authentication successful! token.pickle has been created.")