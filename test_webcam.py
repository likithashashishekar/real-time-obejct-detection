import cv2

def test_webcam():
    # Test different camera indices
    for i in range(3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera {i} is available")
            ret, frame = cap.read()
            if ret:
                print(f"Camera {i} can read frames")
            else:
                print(f"Camera {i} cannot read frames")
            cap.release()
        else:
            print(f"Camera {i} is not available")
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_webcam()