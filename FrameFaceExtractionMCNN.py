import cv2
from mtcnn import MTCNN
import os

# Path to the input image
input_image_path = "./old/Testing/WhatsApp Image 2023-12-27 at 4.13.27 PM (1).jpeg"

# Path to the output directory
output_directory = "./output"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Load the input image
image = cv2.imread(input_image_path)

# Convert the image to RGB (required by MTCNN)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Load the MTCNN face detection model
face_detector = MTCNN()

# Detect faces in the image
faces = face_detector.detect_faces(rgb_image)

# Iterate over detected faces
for i, face_info in enumerate(faces):
    # Get the coordinates of the face rectangle
    x, y, w, h = face_info['box']

    # Extract the face from the image
    face_image = image[y:y + h, x:x + w]

    # Save each face to the output directory
    output_path = os.path.join(output_directory, f"face_{i + 1}.jpg")
    cv2.imwrite(output_path, face_image)

    print(f"Face {i + 1} saved to {output_path}")
