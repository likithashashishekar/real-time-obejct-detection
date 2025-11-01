import cv2
import time
from object_detector import RealTimeObjectDetector

class AdvancedDetector(RealTimeObjectDetector):
    def __init__(self):
        super().__init__()
        self.detection_times = []
        
    def process_video(self, video_source):
        cap = cv2.VideoCapture(video_source)
        frame_count = 0
        total_detections = 0
        
        while True:
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break
                
            # Detection
            detections = self.detect_objects(frame)
            total_detections += len(detections)
            
            # Draw results
            frame = self.draw_detections(frame, detections)
            
            # Calculate FPS
            fps = 1 / (time.time() - start_time)
            
            # Display advanced info
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Objects: {len(detections)}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Total Detections: {total_detections}", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Advanced Object Detection', frame)
            frame_count += 1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = AdvancedDetector()
    detector.process_video("sample_video.mp4")