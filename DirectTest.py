import os
import cv2
import numpy as np
import face_recognition
from sklearn.preprocessing import LabelEncoder
import pickle

def predict_image(image_name):
    image_path = "./uploads/" + image_name

    # Load the trained model
    with open('./Models/model9/friend_face_recognition_model.pkl', 'rb') as model_file:
        classifier = pickle.load(model_file)

    # Load the label encoder
    label_encoder = LabelEncoder()
    label_encoder.classes_ = np.load('./Models/model10/label_encoder_classes.npy')

    # Load the image and find face locations and embeddings
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)

    # Create an empty array for storing face embeddings
    face_embeddings = []

    # Extract embeddings for each face in the image
    for face_location in face_locations:
        face_encoding = face_recognition.face_encodings(image, known_face_locations=[face_location])[0]
        face_embeddings.append(face_encoding)

    # Convert the list of face embeddings to a numpy array
    face_embeddings = np.array(face_embeddings)

    # Predict the labels for the faces using the trained classifier
    predicted_labels = classifier.predict(face_embeddings)

    # Create a dictionary to store label and image path for each face
    result_dict_list = []

    # Save each predicted face with a unique filename
    for idx, (top, right, bottom, left) in enumerate(face_locations):
        label = predicted_labels[idx]

        # Create a unique filename for each predicted face
        new_image_name = f"{image_name.split('.')[0]}_predicted_{idx}.jpg"
        output_path = os.path.join('./uploads', new_image_name)

        # Save the face as a separate image
        face_image = image[top:bottom, left:right]
        # Convert the color format to RGB before saving
        cv2.imwrite(output_path, cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))

        # Add label and image path to the result dictionary
        result_dict = {
            'label': label,
            'image_path': new_image_name
        }
        result_dict_list.append(result_dict)

    
    # Draw rectangles and labels on the image
    for (top, right, bottom, left), label in zip(face_locations, predicted_labels):
        cv2.rectangle(image, (left, top), (right, bottom), (0,143,255), 2)
        cv2.putText(image, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,143,255), 2)

    # Save the result image
    newImageName = image_name.split(".")[0]
    newImageName = newImageName+"_predicted.jpg"
    output_path = f'./uploads/{newImageName}'
    cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    return {"data":result_dict_list,"labels":predicted_labels}

