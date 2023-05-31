import os

import tensorflow as tf


class LabelModel(tf.Module):
    """ Fake Label Model that always returns Zero / False"""

    def __init__(self):
        super().__init__()

    @tf.function(input_signature=[tf.TensorSpec([None], tf.float32)])
    def __call__(self, x):
        return {"y": tf.constant(0.) * x}


class LabelModelV2(tf.Module):
    """ Fake Label Model that always returns 1 / True """

    def __init__(self):
        super().__init__()

    @tf.function(input_signature=[tf.TensorSpec([None], tf.float32)])
    def __call__(self, x):
        return {"y": tf.constant(1.) + 0 * x}


def export():
    """ Store a custom model """
    for i, model in enumerate([LabelModel(), LabelModelV2()]):
        version = i+1
        path = f"model{i+1}"
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, 'labelPrediction', f"{version}")
        tf.saved_model.save(model, path)


if __name__ == '__main__':
    export()
