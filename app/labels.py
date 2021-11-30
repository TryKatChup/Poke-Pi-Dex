import json


def load_labels(filename):
    file_labels = open(filename, "r", encoding="utf-8")
    return json.load(file_labels)