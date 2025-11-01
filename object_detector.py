import cv2
import numpy as np
import time
import time  # ADD THIS IMPORT
from config import *
from utils.helpers import load_yolo_model, get_output_layers, draw_prediction

class RealTimeObjectDetector:
    def __init__(self):
        print("Loading YOLOv4 model...")
        self.net = load_yolo_model(MODEL_WEIGHTS, MODEL_CONFIG)
        self.classes = self.load_classes()
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.output_layers = get_output_layers(self.net)
        print(f"Model loaded successfully! {len(self.classes)} classes available.")
        
    def load_classes(self):
        with open(COCO_NAMES, 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        return classes
    
    def detect_objects(self, image):
        height, width = image.shape[:2]
        
        # Create blob from image
        blob = cv2.dnn.blobFromImage(image, 1/255.0, INPUT_SIZE, swapRB=True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)
        
        return self.process_detections(outputs, width, height)
    
    def process_detections(self, outputs, width, height):
        boxes = []
        confidences = []
        class_ids = []
        
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > CONFIDENCE_THRESHOLD:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        # Apply Non-Maximum Suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        
        detections = []
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                detections.append({
                    'class_id': class_ids[i],
                    'class_name': self.classes[class_ids[i]],
                    'confidence': confidences[i],
                    'box': (x, y, x + w, y + h)
                })
        
        return detections
    
    def draw_detections(self, image, detections):
        for detection in detections:
            x, y, x2, y2 = detection['box']
            draw_prediction(image, detection['class_id'], detection['confidence'], 
                          x, y, x2, y2, self.classes, self.colors)
        
        return image
    
    def process_video(self, video_source=VIDEO_SOURCE):  # THIS SHOULD BE INSIDE THE CLASS
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            print(f"Error: Could not open video source {video_source}")
            return
        
        print("Starting real-time object detection...")
        print("Press 'q' to quit, 'p' to pause, 's' to save screenshot")
        
        paused = False
        frame_count = 0
        start_time = time.time()
        screenshot_count = 0
        
        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    print("End of video stream")
                    break
                
                # Perform object detection
                detections = self.detect_objects(frame)
                
                # Draw detections on frame
                frame_with_detections = self.draw_detections(frame.copy(), detections)
                
                # Calculate and display FPS
                frame_count += 1
                if frame_count % 30 == 0:
                    fps = frame_count / (time.time() - start_time)
                    cv2.putText(frame_with_detections, f"FPS: {fps:.1f}", 
                              (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame_with_detections, f"Objects: {len(detections)}", 
                              (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow('Real-Time Object Detection', frame_with_detections)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                paused = not paused
                print("Paused" if paused else "Resumed")
            elif key == ord('s'):  # SCREENSHOT FEATURE
                screenshot_count += 1
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"detection_{timestamp}_{screenshot_count}.jpg"
                cv2.imwrite(filename, frame_with_detections)
                print(f"📸 Screenshot saved: {filename}")
                print(f"   Detected {len(detections)} objects with confidence scores:")
                for det in detections:
                    print(f"   - {det['class_name']}: {det['confidence']:.2f}")
        
        cap.release()
        cv2.destroyAllWindows()