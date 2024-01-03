import os
import face_recognition
import numpy as np
from sklearn.svm import SVC
import pickle
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Set path to the directory containing your dataset
dataset_path = "./cleanedDataset"

# Define paths to save embeddings and labels
embeddings_path = './data/embeddings 12.npy'
labels_path = './data/labels 12.npy'

# Check if the saved files exist
if os.path.exists(embeddings_path) and os.path.exists(labels_path):
    # Load embeddings and labels if the files exist
    embeddings = np.load(embeddings_path)
    labels = np.load(labels_path)
else:
    # Create empty lists to store the embeddings and corresponding labels
    embeddings = []
    labels = []

    # Iterate over the friend folders
    for friend_folder in os.listdir(dataset_path):
        friend_path = os.path.join(dataset_path, friend_folder)
        if os.path.isdir(friend_path):
            for filename in tqdm(os.listdir(friend_path), desc=f"Processing {friend_folder}"):
                img_path = os.path.join(friend_path, filename)
                
                # Load the image and find face locations and embeddings
                image = face_recognition.load_image_file(img_path)
                face_locations = face_recognition.face_locations(image)
                
                # Use the first face found (you can modify this logic based on your requirements)
                if face_locations:
                    face_encoding = face_recognition.face_encodings(image, known_face_locations=[face_locations[0]])[0]
                    
                    # Append the embedding and label to the lists
                    embeddings.append(face_encoding)
                    labels.append(friend_folder)

    # Convert lists to numpy arrays
    embeddings = np.array(embeddings)
    labels = np.array(labels)

    # Save embeddings and labels
    np.save(embeddings_path, embeddings)
    np.save(labels_path, labels)


# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(embeddings, labels, test_size=0.2, random_state=42)

# Train a Support Vector Machine (SVM) classifier
classifier = SVC(kernel='linear', probability=True)
classifier.fit(X_train, y_train)

# Evaluate the model on the test set
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Test accuracy: {accuracy}')

# Save the trained model using pickle
with open('./Models/model13 SVM/friend_face_recognition_model.pkl', 'wb') as model_file:
    pickle.dump(classifier, model_file)

# Save the label encoder classes for later use during inference
label_encoder = LabelEncoder()
label_encoder.fit(y_train)
np.save('./Models/model13 SVM/label_encoder_classes.npy', label_encoder.classes_)
