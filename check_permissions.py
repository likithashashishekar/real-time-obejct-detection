import os
import cv2
import numpy as np

def check_permissions():
    print("Checking file permissions...")
    
    # Test if we can create and write files
    test_files = [
        "test_write.jpg",
        "test_write.png",
        "detection_test.jpg"
    ]
    
    for filename in test_files:
        try:
            # Create a test image
            test_image = np.ones((100, 100, 3), dtype=np.uint8) * 255
            success = cv2.imwrite(filename, test_image)
            
            if success:
                print(f"✅ Can write: {filename}")
                # Try to delete it
                try:
                    os.remove(filename)
                    print(f"✅ Can delete: {filename}")
                except:
                    print(f"❌ Cannot delete: {filename}")
            else:
                print(f"❌ Cannot write: {filename}")
                
        except Exception as e:
            print(f"❌ Error with {filename}: {e}")

if __name__ == "__main__":
    check_permissions()