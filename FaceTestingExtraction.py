import cv2
import face_recognition
import os

def extract_faces(image_path, output_folder):
    # Load the image
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Find face locations in the image
    face_locations = face_recognition.face_locations(rgb_image)

    # Extract and save smaller face images
    for i, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        cv2.imwrite(f'{output_folder}/face_{i + 1}.jpg', face_image)

# Example usage
image_path = './Testing/WhatsApp Image 2023-12-27 at 4.13.27 PM (3).jpeg'
output_folder = 'output_faces'
os.makedirs(output_folder, exist_ok=True)
extract_faces(image_path, output_folder)
