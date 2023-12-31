import os
import face_recognition
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle
from tqdm import tqdm

# Set path to the directory containing your dataset
dataset_path = "./cleanedDataset"
model = "model9"
# Create empty lists to store the embeddings and corresponding labels
embeddings = []
labels = []

# Iterate over the friend folders
for friend_folder in sorted(os.listdir(dataset_path)):
    friend_path = os.path.join(dataset_path, friend_folder)
    if os.path.isdir(friend_path):
        for filename in tqdm(os.listdir(friend_path), desc=f"Processing {friend_folder}"):
            img_path = os.path.join(friend_path, filename)
            
            # Load the image and find face locations and embeddings
            image = face_recognition.load_image_file(img_path)
            
            # Use the dlib face encoding model
            try:
                face_encoding = face_recognition.face_encodings(image, model="large")[0]
            except:
                print("Image Error")
                continue
            # Append the embedding and label to the lists
            embeddings.append(face_encoding)
            labels.append(friend_folder)

# Convert lists to numpy arrays
X_train = np.array(embeddings)
y_train = np.array(labels)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Train a Support Vector Machine (SVM) classifier
classifier = SVC(kernel='linear', probability=True)
classifier.fit(X_train, y_train)

# Evaluate the model on the test set
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Test accuracy: {accuracy}')

os.mkdir(f"./Models/{model}")
# Save the trained model using pickle
with open(f'./Models/{model}/friend_face_recognition_model.pkl', 'wb') as model_file:
    pickle.dump(classifier, model_file)

# Save the label encoder classes for later use during inference
label_encoder = LabelEncoder()
label_encoder.fit(y_train)
np.save(f'./Models/{model}/label_encoder_classes.npy', label_encoder.classes_)
