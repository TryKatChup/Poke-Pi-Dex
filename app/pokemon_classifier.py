import os
import glob
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import typing
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
from matplotlib import pyplot as plt


def get_label_encoder():
    encoder = LabelEncoder()
    encoder.classes_ = np.load('./classes.npy')
    return encoder

def predict_top_n_pokemon(image_file, num_top_pokemon):    
    """Predicts num_top_pokemon from image_file, using a tflite model"""
    TFLITE_MODEL="./qa_model_best100_8bit.tflite"
    interpreter = tf.lite.Interpreter(TFLITE_MODEL)
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load image and convert it to tensor
    img = load_img(image_file, target_size=(224, 224)) #"./evee_1.jpg"
    img = img_to_array(img, dtype=np.float32)
    img /= 255
    img = np.expand_dims(img, axis=0)

    input_tensor = np.array(img, dtype=np.float32)
    # Load TFLite model and allocate tensors
    interpreter.set_tensor(input_details[0]['index'], input_tensor)
    interpreter.invoke()

    # Get output
    output_data = interpreter.get_tensor(output_details[0]['index'])
    # Get label encoder
    label_encoder = get_label_encoder()
    
    # Get best num_top_pokemon
    (top_k_scores, top_k_idx) = tf.math.top_k(output_data, num_top_pokemon)
    top_k_scores = np.squeeze(top_k_scores.numpy(), axis=0)
    top_k_idx = np.squeeze(top_k_idx.numpy(), axis=0)
    top_k_labels = label_encoder.inverse_transform(top_k_idx)
    return top_k_labels, top_k_scores

