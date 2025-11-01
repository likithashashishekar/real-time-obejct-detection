import cv2
import time
from object_detector import RealTimeObjectDetector

def test_screenshot():
    print("Testing screenshot functionality...")
    
    # Create a simple test image
    test_image = cv2.imread('sample_video.mp4')  # Try to use your video as source
    
    # If video frame doesn't work, create a synthetic image
    if test_image is None:
        print("Creating synthetic test image...")
        test_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
        # Add some colored rectangles
        cv2.rectangle(test_image, (100, 100), (200, 200), (0, 0, 255), -1)  # Red
        cv2.rectangle(test_image, (300, 150), (400, 250), (255, 0, 0), -1)  # Blue
    
    # Initialize detector
    detector = RealTimeObjectDetector()
    
    # Detect objects
    detections = detector.detect_objects(test_image)
    result_image = detector.draw_detections(test_image, detections)
    
    # Try to save screenshot
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"test_screenshot_{timestamp}.jpg"
    
    success = cv2.imwrite(filename, result_image)
    if success:
        print(f"✅ Screenshot saved successfully: {filename}")
        print(f"   File size: {os.path.getsize(filename)} bytes")
        print(f"   Detected {len(detections)} objects")
    else:
        print(f"❌ Failed to save screenshot: {filename}")
        print("Trying different format...")
        
        # Try PNG format
        filename_png = f"test_screenshot_{timestamp}.png"
        success_png = cv2.imwrite(filename_png, result_image)
        if success_png:
            print(f"✅ PNG screenshot saved: {filename_png}")
        else:
            print("❌ Both JPG and PNG formats failed")

if __name__ == "__main__":
    test_screenshot()