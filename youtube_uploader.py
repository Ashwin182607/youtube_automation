import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import json
import pickle
from pathlib import Path

class YouTubeUploader:
    def __init__(self):
        self.youtube = None
        self.credentials = None
        self.token_file = "token.pickle"
        self.client_secrets_file = "client_secrets.json"
        
    def authenticate(self):
        """Authenticate with YouTube API"""
        if os.path.exists(self.token_file):
            with open(self.token_file, "rb") as token:
                self.credentials = pickle.load(token)
                
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                if not os.path.exists(self.client_secrets_file):
                    raise FileNotFoundError(
                        f"Client secrets file not found. Please place your OAuth 2.0 Client ID file as {self.client_secrets_file}"
                    )
                    
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file,
                    ["https://www.googleapis.com/auth/youtube.upload"]
                )
                self.credentials = flow.run_local_server(port=0)
                
            with open(self.token_file, "wb") as token:
                pickle.dump(self.credentials, token)
        
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", credentials=self.credentials
        )
        return True
        
    def upload_video(self, file_path, title, description="", tags=None,
                    privacy_status="private", category="10", 
                    notify_subscribers=True):
        """
        Upload a video to YouTube
        
        Args:
            file_path (str): Path to the video file
            title (str): Video title
            description (str): Video description
            tags (list): List of tags
            privacy_status (str): Privacy status (private/public/unlisted)
            category (str): Video category ID
            notify_subscribers (bool): Whether to notify subscribers
            
        Returns:
            dict: Response from YouTube API
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Video file not found: {file_path}")
            
        if not self.youtube:
            self.authenticate()
            
        tags = tags or []
        
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False,
                "notifySubscribers": notify_subscribers
            }
        }
        
        insert_request = self.youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(
                file_path, 
                chunksize=-1, 
                resumable=True
            )
        )
        
        response = None
        while response is None:
            try:
                _, response = insert_request.next_chunk()
                if response:
                    return response
                    
            except googleapiclient.errors.HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    # Retry on server errors
                    continue
                else:
                    raise
                    
        return response
        
    def get_upload_progress(self, video_id):
        """Get the processing status of an uploaded video"""
        try:
            request = self.youtube.videos().list(
                part="status,processingDetails",
                id=video_id
            )
            response = request.execute()
            
            if response["items"]:
                status = response["items"][0]["status"]
                processing = response["items"][0].get("processingDetails", {})
                return {
                    "uploadStatus": status["uploadStatus"],
                    "privacyStatus": status["privacyStatus"],
                    "processingStatus": processing.get("processingStatus"),
                    "processingProgress": processing.get("processingProgress", {})
                }
        except Exception as e:
            return {"error": str(e)}
            
        return None

if __name__ == "__main__":
    # Example usage
    uploader = YouTubeUploader()
    video_id = uploader.upload_video(
        file_path='output_video.mp4',
        title='Chill Music Video',
        description='A relaxing music video',
        tags=['chill', 'music', 'relaxing'],
        privacy_status='private',  # Start with private to verify the upload
        notify_subscribers=False
    )