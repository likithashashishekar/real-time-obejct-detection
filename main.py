from object_detector import RealTimeObjectDetector
import argparse
import os
import cv2

def test_video_source(source):
    """Test if video source is accessible"""
    cap = cv2.VideoCapture(source)
    if cap.isOpened():
        ret, frame = cap.read()
        cap.release()
        return ret
    return False

def main():
    parser = argparse.ArgumentParser(description='Real-Time Object Detection System')
    parser.add_argument('--source', type=str, default='0',
                       help='Video source (0 for webcam, or path to video file)')
    args = parser.parse_args()
    
    print("=== Real-Time Object Detection System ===")
    
    # Test video source
    video_source = args.source
    if video_source.isdigit():
        video_source = int(video_source)  # Convert to int for camera index
    
    print(f"Testing video source: {video_source}")
    
    if not test_video_source(video_source):
        print(f"ERROR: Cannot access video source {video_source}")
        print("\nTroubleshooting tips:")
        print("1. For webcam: Try --source 1 or --source 2")
        print("2. Make sure no other app is using the webcam")
        print("3. For video files: Make sure test_video.mp4 exists in current directory")
        print("4. Try using a sample video from your phone or download one")
        return
    
    print("Video source is accessible!")
    print("Initializing object detector...")
    
    try:
        # Initialize detector
        detector = RealTimeObjectDetector()
        
        print("\nStarting video processing...")
        print("Press 'q' to quit, 'p' to pause")
        detector.process_video(video_source)
        
    except KeyboardInterrupt:
        print("\nStopping detection...")
    except Exception as e:
        print(f"Error during detection: {e}")

if __name__ == "__main__":
    main()