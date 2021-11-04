import os
import glob
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import typing
import numpy as np


def get_label_encoder():
    encoder = LabelEncoder()
    encoder.classes_ = np.load('./classes.npy')
    return encoder


def top_prediction(model, img, label_encoder, k=1):
    scores = model.predict(img)
    (top_k_scores, top_k_idx) = tf.math.top_k(scores, k)
    top_k_idx = np.squeeze(top_k_idx.numpy(), axis=0)
    top_k_labels = label_encoder.inverse_transform(top_k_idx)
    return top_k_labels

