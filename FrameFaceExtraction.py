import cv2
import os
import dlib

total = 0
def extract_frames(video_path, output_folder, frame_rate):
    global total
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Get video information
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate the frame interval based on the desired rate
    frame_interval = int(fps / frame_rate)
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Loop through the frames and save every nth frame
    frame_number = 0
    while frame_number < frame_count:
        ret, frame = cap.read()
        if not ret:
            break
        # Save the frame
        frame_name = f"{output_folder}/frame_{frame_number // frame_interval}.jpg"
        cv2.imwrite(frame_name, frame)
        total+=1
        # Increment frame number
        frame_number += frame_interval
    
    # Release the video capture object
    cap.release()

def process_videos(videos_folder, output_root_folder, frame_rate):
    # List all video files in the specified folder
    video_files = [f for f in os.listdir(videos_folder) if f.endswith(('.mp4', '.avi', '.mkv', '.MOV', '.mov'))]
    # video_files = [f for f in os.listdir(videos_folder) if f.endswith(('.MOV'))]
    # Process each video
    for video_file in video_files:
        video_path = os.path.join(videos_folder, video_file)
        output_folder = os.path.join(output_root_folder, video_file.split(".")[0])
        
        # Extract frames from the video
        print(output_folder)
        extract_frames(video_path, output_folder, frame_rate)

# Detect the Face in an Images and Cut off the Background "Remove Noise"
def extract_faces_from_images(input_folder, output_folder):
    face_detector = dlib.get_frontal_face_detector()
    
    # Loop through each subdirectory in the input folder
    for subfolder in os.listdir(input_folder):
        subfolder_path = os.path.join(input_folder, subfolder)

        # Check if the subfolder is a directory
        if os.path.isdir(subfolder_path):
            # Create a corresponding subdirectory in the output folder
            output_subfolder_path = os.path.join(output_folder, subfolder)
            os.makedirs(output_subfolder_path, exist_ok=True)

            # Loop through each image file in the subdirectory
            for image_name in os.listdir(subfolder_path):
                if image_name.lower().endswith('.jpg'):
                    # Read the image
                    image_path = os.path.join(subfolder_path, image_name)
                    image = cv2.imread(image_path)

                    # Convert the image to grayscale for face detection
                    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    # Detect faces in the image using dlib face detector
                    faces = face_detector(gray_image)

                    # Extract and save each face
                    for i, face in enumerate(faces):
                        # Get the coordinates of the face rectangle
                        x, y, w, h = face.left(), face.top(), face.width(), face.height()

                        # Extract the face from the image
                        face_image = image[y:y + h, x:x + w]

                        # Save the face to the output folder
                        output_face_path = os.path.join(output_subfolder_path, f"{image_name.replace('.jpg', f'_face_{i + 1}.jpg')}")
                        cv2.imwrite(output_face_path, face_image)

                        print(f"Face {i + 1} extracted from {image_name} and saved to {output_face_path}")


# Specify the input videos folder, output root folder, and frame rate
input_videos_folder = "./videos"
output_root_folder = "./dataset"
frame_rate = 4  # Extract every 20th frame

# Process videos and extract frames
process_videos(input_videos_folder, output_root_folder, frame_rate)
print("Total Number of Images is :",total)


input_dataset_folder  =  output_root_folder
output_cleaned_folder = "./cleanedDataset"

# Call the function to extract faces from images
extract_faces_from_images(input_dataset_folder, output_cleaned_folder)