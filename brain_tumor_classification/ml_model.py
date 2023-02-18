import base64
import io
import os
import tensorflow as tf
from PIL import Image

brain_tumor_classification_model = tf.keras.models.load_model(
    os.path.join("saved_ml_models", "brain_tumor_classification"))


def preprocess_image(image):
    image = Image.open(io.BytesIO(base64.decodebytes(bytes(image, "utf-8"))))
    image = tf.image.resize(image, [256, 256])
    image = tf.expand_dims(image, axis=0)
    return image


def predict(image):
    image = preprocess_image(image)
    predication = brain_tumor_classification_model.predict(image, verbose=0)[0]
    return {'glioma': predication[0], 'meningioma': predication[1], 'notumor': predication[2],
            'pituitary': predication[3]}
