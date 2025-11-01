import urllib.request
import os

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename)
        print("Download completed!")
    else:
        print(f"{filename} already exists!")

# Create models directory
os.makedirs("models", exist_ok=True)

# Download YOLOv4 files
files = {
    "yolov4.weights": "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights",
    "yolov4.cfg": "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg",
    "coco.names": "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names"
}

for filename, url in files.items():
    download_file(url, f"models/{filename}")

print("All model files are ready!")