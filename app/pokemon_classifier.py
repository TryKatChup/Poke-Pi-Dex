import os
import glob
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import typing
import numpy as np
from matplotlib import pyplot as plt
import cv2
from image_rectifier import rectify_image, rectify_image_from_file

from PIL import Image


def get_label_encoder():
    encoder = LabelEncoder()
    encoder.classes_ = np.load('./resources/classifier_model/best_classes.npy')
    return encoder


def predict_top_n_pokemon(image_filename, num_top_pokemon):
    # Predicts num_top_pokemon from image_file, using a tflite model
    TFLITE_MODEL="./resources/classifier_model/vecchio_modello_nuovo_dataset_55fotoclasse_hue.tflite"
    interpreter = tf.lite.Interpreter(TFLITE_MODEL)
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load image and convert it to tensor
    if tf.__version__ == "2.6.0":
        # Open image with keras.utils
        from tensorflow.keras.utils import load_img, img_to_array
        img = load_img(image_filename, target_size=(224, 224))  #"./evee_1.jpg"5
        img = img_to_array(img, dtype=np.float32)
    else:
        # Open image with PIL.Image
        img = Image.open(image_filename)
        img = img.resize((224, 224), Image.ANTIALIAS)
    img = np.asarray(img, dtype=np.float32)
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


# Main Test
if __name__ == "__main__":
    print("#N predictions: ")
    n = input()
    try:
        n = int(n)
        if not (1 <= n <= 10):
            raise ValueError
    except ValueError:
        print("#N must be an integer between 1 and 10!")
        exit()
    # Prediction
    result = predict_top_n_pokemon("frame.jpg", n)
    result_str = ""
    for i in range(0, n):
        result_str += str(i + 1) + "> " + str(result[0][i]) + "\t"
        if len(str(result[0][i])) < 9:
            result_str += "\t"
        else:
            result_str += " \t"
        result_str += str(result[1][i])[:6] + "\n"
    print(result_str)

    '''
    # Open image with OpenCV (NOT WORKING, maybe interpolation is broken)
    img = cv2.imread(image_filename)
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
    '''
