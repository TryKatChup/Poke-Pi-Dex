import os
import glob
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import typing


def create_dataset(
    data_folder: str,
    epochs: int,
    batch_size: int, # how many samples are processed in parallel (2^n)
    res: typing.Tuple[int, int],
    seed: int,
) -> tf.data.Dataset:
    # Import folder with images
    folders = sorted(glob.glob(os.path.join(data_folder, "*", "")))
    samples = []
    for folder in folders:
        cur_samples = sorted(glob.glob(os.path.join(folder, "*.jpg")))
        # /app/data/Vaporeon/
        # Obtaining only pokemon name
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

    # Load images from disk
    def map_fn(path, label):
        # path/label represent values for a single example
        image = tf.image.decode_image(tf.io.read_file(path), expand_animations=False, channels=3)

        # some mapping to constant size - be careful with distorting aspec ratios
        image = tf.image.resize(image, res)
        
        # Normalize to [0, 1] range
        image /= 255.
        return image, label

    # num_parallel_calls > 1 induces intra-batch shuffling
    dataset = dataset.map(map_fn, num_parallel_calls=tf.data.AUTOTUNE)
    # Initial shuffle of the whole dataset with seed
    dataset = dataset.shuffle(buffer_size=data_len, reshuffle_each_iteration=False, seed=seed)
    val_split = test_split = 0.1
    
    test_len = int(test_split * data_len)
    val_len = int(val_split * data_len)
    
    train_len = data_len - val_len - test_len
    
    test_dataset = dataset.take(test_len)
    trainval_dataset = dataset.skip(test_len)
    val_dataset = trainval_dataset.take(val_len)
    train_dataset = trainval_dataset.skip(val_len)

    train_dataset = train_dataset.cache()
    val_dataset = val_dataset.cache()

    # =====================================================================================
    # Data Augmentation techniques
    # =====================================================================================
    #
    # Useful to expand the size of a training set by creating modified data from the existing one.
    # - Prevent overfitting;
    # - Expand dataset in case it is too small;
    # - It can improve the performance of the model by augmenting the data we already have.
    #
    # We apply various changes to the initial data:
    # - Random rotation of image;
    # - Random flip from left to right and viceversa;
    # - Change randomly brightness, with a minimum decrease of 20% and a maximum one of 19.9%

    def random_rotate(image, label):
        # Generate a random number, between 0 and 3 (number of 90 degrees rotation)
        k = tf.random.uniform(shape=(), minval=0, maxval=4, dtype=tf.int32)
        # tf.cond wants always a function :D
        image = tf.image.rot90(image, k)
        return image, label
    
    # Apply functions on train dataset
    train_dataset = train_dataset.map(
        lambda image, label: (tf.image.random_flip_left_right(image), label),
        num_parallel_calls=tf.data.AUTOTUNE
    #).map(
    #    lambda image, label: (tf.image.random_brightness(image, 0.2), label),
    #    num_parallel_calls=tf.data.AUTOTUNE
    ).map(
        random_rotate,
        num_parallel_calls=tf.data.AUTOTUNE
    )
    
    train_dataset = train_dataset.shuffle(buffer_size=256, reshuffle_each_iteration=True)
    
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


def create_model(
    n_conv: int = 3,
    use_bn: bool = False,
    res: typing.Tuple[int, int] = (256, 256)
):
    
    # 1. Input
    # 2. Feature extraction con n_conv livelli e numero crescente di filtri (32 -> 64 -> 128...):
    #     1. Conv2D
    #     2. BatchNorm (se specificato)
    #     3. ReLU
    # 3. Flatten
    # 4. Classifier con 3 livelli fully connected:
    #     1. Dense con 1024 neuroni
    #     2. BatchNorm (se specificato)
    #     3. ReLU
    #     4. Dense con 1024 neuroni
    #     5. BatchNorm (se specificato)
    #     6. ReLU
    #     7. Dense con 150 neuroni (come il numero di classi)
    #     8. Softmax
    
    input_layer = tf.keras.layers.Input(shape=(res[0], res[1], 3))
    x = input_layer
    
    for i in range(n_conv):
        n_filters = 2 ** (i + 6)
        
        # Conv2D + BatchNorm + ReLU
        x = tf.keras.layers.Conv2D(n_filters, 3, padding="same")(x)
        if use_bn:
            x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.ReLU()(x)

        x = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(x)
    
    flat = tf.keras.layers.Flatten()(x)
    
    # 1st Dense(1024) + BatchNorm + ReLU
    fc1 = tf.keras.layers.Dense(1024)(flat)
    if use_bn:
        fc1 = tf.keras.layers.BatchNormalization()(fc1)
    fc1 = tf.keras.layers.ReLU()(fc1)
    # 2nd Dense(1024) + BatchNorm + ReLU
    fc2 = tf.keras.layers.Dense(1024)(fc1)
    if use_bn:
        fc2 = tf.keras.layers.BatchNormalization()(fc2)
    fc2 = tf.keras.layers.ReLU()(fc2)
    # 3rd Dense(150) + softmax
    fc3 = tf.keras.layers.Dense(150)(fc2)
    fc3 = tf.keras.layers.Softmax()(fc3)

    model = tf.keras.Model(inputs=input_layer, outputs=fc3, name="Pokemon-classifier")
    
    return model
