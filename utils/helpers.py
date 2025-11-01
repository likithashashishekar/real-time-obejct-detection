import cv2
import numpy as np

def load_yolo_model(weights_path, config_path):
    """Load YOLO model from weights and config files"""
    net = cv2.dnn.readNet(weights_path, config_path)
    
    # Try to enable GPU if available
    try:
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            print("Using GPU acceleration")
        else:
            print("Using CPU")
    except:
        print("Using CPU (GPU not available)")
    
    return net

def get_output_layers(net):
    """Get output layer names from YOLO network"""
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes, colors):
    """Draw bounding box and label on image"""
    label = f"{classes[class_id]}: {confidence:.2f}"
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)