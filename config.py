import os

# Model configuration
MODEL_WEIGHTS = "models/yolov4.weights"
MODEL_CONFIG = "models/yolov4.cfg"
COCO_NAMES = "models/coco.names"

# Video configuration
VIDEO_SOURCE = 0  # 0 for webcam, or "test_video.mp4" for file
CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
INPUT_SIZE = (416, 416)

# Performance settings
USE_GPU = False  # Set to True if you have OpenCV with CUDA support