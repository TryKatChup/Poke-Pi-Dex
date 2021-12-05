import os
import torch
import matplotlib.pyplot as plt
import numpy as np
# TODO Label encoer for classnames
def predict_image(image):
    with torch.no_grad()
        # Loading the saved model
        save_path = './pathtomodel'
        res = models.resnet152(pretrained=True)
        num_ftrs = model_ft.fc.in_features
        # Here the size of each output sample is set to 2.
        # Alternatively, it can be generalized to nn.Linear(num_ftrs, len(class_names)).
        model_ft.fc = nn.Linear(num_ftrs, len(class_names))
        res.load_state_dict(torch.load(save_path))
        res.eval()
        # Generate prediction
        prediction = res(image)
        # Predicted class value using argmax
        predicted_class = np.argmax(prediction)
