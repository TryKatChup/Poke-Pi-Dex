import os
import glob
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import typing


def create_dataset(
    data_folder: str,
    epochs: int,
    batch_size: int,
    res: typing.Tuple[int, int],
    seed: int,
) -> tf.data.Dataset:
    folders = sorted(glob.glob(os.path.join(data_folder, "*", "")))
    samples = []
    for folder in folders:
        cur_samples = sorted(glob.glob(os.path.join(folder, "*.jpg")))
        # /app/data/Vaporeon/
        # Obtaining only pokemon name:
        label = folder.split(os.path.sep)[-2]
        cur_samples = [(cur_sample, label) for cur_sample in cur_samples]
        samples.extend(cur_samples)
    
    # Get dataset length
    data_len = len(samples)

    # Create LabelEncoder
    label_encoder = LabelEncoder()
    # Extract images and labels
    image_paths, labels = list(zip(*samples))
    # Train LabelEncoder
    label_encoder.fit(list(set(labels)))  # convert to set to remove duplicates
    # Convert string labels to integer
    labels = label_encoder.transform(labels)

    # Convert both lists to tensors
    image_paths = tf.convert_to_tensor(image_paths, dtype=tf.string)
    labels = tf.convert_to_tensor(labels)
    
    # Create Dataset object
    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))

    
    def map_fn(path, label):
        # path/label represent values for a single example
        image = tf.image.decode_jpeg(tf.io.read_file(path))

        # some mapping to constant size - be careful with distorting aspec ratios
        image = tf.image.resize(image, res)
        # Normalize to [0, 1] range
        image /= 255.
        return image, label

    # num_parallel_calls > 1 induces intra-batch shuffling
    dataset = dataset.map(map_fn, num_parallel_calls=tf.data.AUTOTUNE)
    # Initial shuffle with seed
    dataset = dataset.shuffle(buffer_size=256, seed=seed)
    # TODO: split dataset
    # 80% of the samples to training set
    # 10% of the samples to validation set
    # 10% of the samples to test set
    # dataset = dataset.shuffle(buffer_size=100).repeat(epochs)
    val_split = test_split = 0.1
    
    test_len = int(test_split * data_len)
    val_len = int(val_split * data_len)
    
    train_len = data_len - val_len - test_len
    
    test_dataset = dataset.take(test_len)
    trainval_dataset = dataset.skip(test_len)
    val_dataset = trainval_dataset.take(val_len)
    train_dataset = trainval_dataset.skip(val_len)
    
    train_dataset = train_dataset.shuffle(buffer_size=256, reshuffle_each_iteration = True)
    
    train_dataset = train_dataset.batch(batch_size)
    val_dataset = val_dataset.batch(batch_size)
    
    train_dataset = train_dataset.repeat(epochs)
    val_dataset = val_dataset.repeat(epochs)
    
    train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
    val_dataset = val_dataset.prefetch(tf.data.AUTOTUNE)
    
    data_dict = {
        "train_dataset": train_dataset,
        "val_dataset": val_dataset,
        "test_dataset": test_dataset,
        "train_len": train_len,
        "val_len": val_len,
        "test_len": test_len,
        "label_encoder": label_encoder
    }
    
    return data_dict


def create_model(res):
    
    input_layer = tf.keras.layers.Input(shape=(res[0], res[1], 3))
    gigi = tf.keras.layers.Conv2D(16, 3, padding="same")(input_layer)
    nunzio = tf.keras.layers.BatchNormalization()(gigi)
    ciro = tf.keras.layers.ReLU()(nunzio)

    model = tf.keras.Model(inputs=input_layer, outputs=ciro, name="Pokemon-classifier")
    return model


