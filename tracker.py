import cv2
from object_detector import RealTimeObjectDetector

class ObjectTracker(RealTimeObjectDetector):
    def __init__(self):
        super().__init__()
        self.track_history = {}
        
    def draw_tracking(self, frame, detections, frame_id):
        for det in detections:
            obj_id = f"{det['class_name']}_{hash(det['box'])%1000}"
            x, y, x2, y2 = det['box']
            
            # Store tracking history
            if obj_id not in self.track_history:
                self.track_history[obj_id] = []
            center = ((x + x2) // 2, (y + y2) // 2)
            self.track_history[obj_id].append(center)
            
            # Draw tracking line (last 10 positions)
            points = self.track_history[obj_id][-10:]
            for i in range(1, len(points)):
                cv2.line(frame, points[i-1], points[i], (0, 255, 0), 2)
            
            # Add object ID to label
            label = f"{obj_id} {det['class_name']}: {det['confidence']:.2f}"
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)