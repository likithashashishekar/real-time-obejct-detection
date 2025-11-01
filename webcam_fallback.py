import cv2
import numpy as np
import time
from object_detector import RealTimeObjectDetector

def webcam_fallback():
    print("Trying alternative webcam access methods...")
    
    # Try different backends
    backends = [
        cv2.CAP_ANY,
        cv2.CAP_DSHOW,  # DirectShow (Windows)
        cv2.CAP_MSMF,   # Microsoft Media Foundation
    ]
    
    for backend in backends:
        print(f"Trying backend: {backend}")
        cap = cv2.VideoCapture(0, backend)
        
        if cap.isOpened():
            print(f"Success with backend {backend}!")
            
            # Initialize detector
            detector = RealTimeObjectDetector()
            
            print("Starting detection... Press 'q' to quit, 's' to save screenshot")
            
            screenshot_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Perform detection
                detections = detector.detect_objects(frame)
                frame_with_detections = detector.draw_detections(frame, detections)
                
                # Display info
                cv2.putText(frame_with_detections, f"Objects: {len(detections)}", 
                          (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame_with_detections, "Press 's' to screenshot", 
                          (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                cv2.imshow('Real-Time Detection', frame_with_detections)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):  # SCREENSHOT FEATURE
                    screenshot_count += 1
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"detection_{timestamp}_{screenshot_count}.jpg"
                    success = cv2.imwrite(filename, frame_with_detections)
                    if success:
                        print(f"📸 Screenshot saved: {filename}")
                        print(f"   Detected {len(detections)} objects:")
                        for det in detections:
                            print(f"   - {det['class_name']}: {det['confidence']:.2f}")
                    else:
                        print(f"❌ Failed to save screenshot: {filename}")
            
            cap.release()
            cv2.destroyAllWindows()
            return True
    
    print("All webcam methods failed")
    return False

if __name__ == "__main__":
    webcam_fallback()