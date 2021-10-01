# import tensorflow as tf
import glob
import os

def create_dataset(datafolder):
    folders = sorted(glob.glob(os.path.join(datafolder,"*")))
    samples = []
    for folder in folders:
        cur_samples = sorted(glob.glob(os.path.join(folder,"*.jpg")))
        # /home/katchup/Scrivania/PokemonData/Vaporeon
        # Obtaining only pokemon name:
        label = folder.split("/")[-1]
        cur_samples = [(cur_sample, label) for cur_sample in cur_samples]
        samples.extend(cur_samples)

    image_paths, labels = list(zip(*samples))
    image_paths = tf.convert_to_tensor(image_paths, dtype=tf.string)
    labels = tf.convert_to_tensor(labels)

    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))

    if mode == 'train':
        dataset = dataset.shuffle(buffer_size=100).repeat(epoch_size)

    def map_fn(path, label):
        # path/label represent values for a single example
        image = tf.image.decode_jpeg(tf.read_file(path))

        # some mapping to constant size - be careful with distorting aspec ratios
        image = tf.image.resize_images(out_shape)
        # color normalization - just an example
        image = tf.to_float(image) * (2. / 255) - 1
        return image, label

    # num_parallel_calls > 1 induces intra-batch shuffling
    dataset = dataset.map(map_fn, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.batch(batch_size)

    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    return dataset


#TODO Label as int instead of string