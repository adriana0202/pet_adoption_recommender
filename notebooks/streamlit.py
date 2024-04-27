import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import re
import pickle
import streamlit as st
import os, keras
import cv2
import tensorflow as tf
from tensorflow.keras.applications import VGG16, VGG19, ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input as vgg16_preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from keras import models, layers
import numpy as np
import warnings
import io
from PIL import Image

# Suppress all warnings
warnings.filterwarnings("ignore")

# folder_path = input()

# loading extracted vectors from 1,000 images pool
with open('prediction_models/model_feature_vectors.pickle', 'rb') as handle:
    model_feature_vectors = pickle.load(handle)

#load model

model = VGG16(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

#define vector extraction function for uploaded file

# def extract_feature_vector(image_path):
#     image = load_img(image_path, target_size=(224, 224))
#     image = img_to_array(image)
#     image = vgg16_preprocess_input(image)
#     image = np.expand_dims(image, axis=0)
#     feature_vector = model.predict(image)
#     return feature_vector.flatten()

# Main Streamlit app 
def main():
    st.title("Image Recommender")


# Sidebar for file upload
st.sidebar.title("Upload Image")
uploaded_file = st.file_uploader("Choose a file", type=['png','jpg','jpeg'])


# Load the pickle file
with open('/Users/adrianabrazon/Documents/IronHack/final_project/prediction_models/model_feature_vectors.pickle', 'rb') as handle:
    model_feature_vectors = pickle.load(handle)

given_model = VGG16(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet',
)


# Extract the feature vectors for VGG16
vgg16_feature_vectors = model_feature_vectors['VGG16']

def extract_feature_vector(image_path, model):
    # Load the image
    image = load_img(image_path, target_size=(224, 224))
    # Convert image to array
    image_array = img_to_array(image)
    # Preprocess the image
    image_array = vgg16_preprocess_input(image_array)
    # Expand dimensions to create a batch of size 1
    image_array = np.expand_dims(image_array, axis=0)
    # Extract feature vector using the model
    feature_vector = model.predict(image_array)
    # Flatten the feature vector
    feature_vector = feature_vector.flatten()
    return feature_vector

# Load the feature vector of a given image
given_image_path = uploaded_file
given_feature_vector = extract_feature_vector(given_image_path, given_model)

# Ensure the given feature vector has the same dimensionality as stored feature vectors
# given_feature_vector = given_feature_vector[:vgg16_feature_vectors.shape[1]]
vgg16_feature_vector_length = len(next(iter(vgg16_feature_vectors.values())))
given_feature_vector = given_feature_vector[:vgg16_feature_vector_length]

# Calculate similarities with VGG16 feature vectors
similarities = {}
for filename, feature_vector in vgg16_feature_vectors.items():
    similarity_score = cosine_similarity([given_feature_vector], [feature_vector])[0][0]
    similarities[filename] = similarity_score

# Sort the similarities and get the top 5 similar images
top_5_similar_images = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:5]

# Print or use the top 5 similar images as needed
print(top_5_similar_images)

# similar_images[model_name] = top_5_similar_images
        # Display recommended similar images
st.subheader("Recommended Similar Images:")

for i, (filename, similarity_score) in enumerate(top_5_similar_images):
    image_path = os.path.join('/Users/adrianabrazon/Documents/IronHack/final_project/images', filename)
    st.image((image_path), caption=f"#{i+1}: {filename}", use_column_width=True)        
        # for i, similar_image in enumerate(top_5_similar_images):
        #     st.image(os.path.join("image_folder_path", similar_image), caption=f"#{i+1}: {similar_image}", use_column_width=True)

# for i, similar_image in enumerate(similar_images):
    
if __name__ == "__main__":
        main()

# uploaded_files = st.file_uploader("Choose an image", accept_multiple_files=True)
# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     st.write("filename:", uploaded_file.name)
#     st.write(bytes_data)

# def file_selector(folder_path='given_images/'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.selectbox('Select a file', filenames)
#     return os.path.join(folder_path, selected_filename)
# filename = file_selector()
# st.write('You selected `%s`' % filename)
# st.image(filename)

# def file_selector(uploaded_file):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.selectbox('Select a file', filenames)
#     return os.path.join(folder_path, selected_filename)

# uploaded_file = file_selector()
# st.write('You selected `%s`' % filename)
# st.image(filename)

# # Main Streamlit app 
# def main():
#     st.title("Image Recommender")

#     # Sidebar for file upload
#     st.sidebar.title("Upload Image")
#     uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png"])

#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         st.sidebar.image(image, caption='Uploaded Image.', use_column_width=True)

#         # Load images and calculate similarity matrix
#         images, filenames = load_images("image_folder_path")
#         similarity_matrix = calculate_similarity(images)

#         # Display recommended similar images
#         st.subheader("Recommended Similar Images:")
#         image_index = 0  # You can change this to the index of the uploaded image
#         similar_images = recommend_similar_images(image_index, similarity_matrix, filenames)
#         for i, similar_image in enumerate(similar_images):
#             st.image(os.path.join("image_folder_path", similar_image), caption=f"#{i+1}: {similar_image}", use_column_width=True)

# if __name__ == "__main__":
#     main()