import urllib.request
import os

def download_sample_video():
    # Download a sample video for testing
    video_url = "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4"
    video_path = "sample_video.mp4"
    
    if not os.path.exists(video_path):
        print("Downloading sample video...")
        try:
            urllib.request.urlretrieve(video_url, video_path)
            print("Sample video downloaded successfully!")
        except Exception as e:
            print(f"Could not download sample video: {e}")
            print("Please manually place a video file in the current directory")
    else:
        print("Sample video already exists!")
    
    return video_path

if __name__ == "__main__":
    download_sample_video()