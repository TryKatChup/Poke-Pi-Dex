import tflite_runtime.interpreter as tflite
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
from PIL import Image
import numpy as np
from PIL import Image
# convert scientific notation to decimal
np.set_printoptions(suppress=True,
   formatter={'float_kind':'{:f}'.format})

def get_label_encoder():
    encoder = LabelEncoder()
    encoder.classes_ = np.load('./resources/classifier_model/best_classes.npy')
    return encoder


def predict_top_n_pokemon(image_filename, num_top_pokemon):
    # Predicts num_top_pokemon from image_file, using a tflite model
    TFLITE_MODEL="./vecchio_modello_nuovo_dataset_55fotoclasse_hue.tflite"
    interpreter = tflite.Interpreter(TFLITE_MODEL)
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load image
    img = Image.open("./images/pikachu_peluche.jpg")
    img = img.resize((224, 224), Image.ANTIALIAS)
    img = np.asarray(img, dtype=np.float32)
    img /= 255
    img = np.expand_dims(img, axis=0)
    # remove comment only if experimening  with some strange models (pytorch to tflite case)
    #img = tf.transpose(img, [0, 3, 1, 2])
    print(img.shape)

    input_tensor = np.array(img, dtype=np.float32)
    # Load the TFLite model and allocate tensors.
    interpreter.set_tensor(input_details[0]['index'], input_tensor)
    interpreter.invoke()

    # Get output
    output_data = interpreter.get_tensor(output_details[0]['index'])
    # Get label encoder
    label_encoder = get_label_encoder()
    
    # Get best num_top_pokemon
    # tflite_runtime.interpreter as tflite method
    results = np.squeeze(output_data, axis=0)
    top_k_idx = np.argsort(results)[-5:][::-1]
    top_k_values = results[top_k_idx]
    top_k_labels = label_encoder.inverse_transform(top_k_idx) 
    return top_k_labels, top_k_values
    
 
