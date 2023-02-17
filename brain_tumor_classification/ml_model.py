import base64
import io
import os
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from numpy import float32

brain_tumor_classification_model = tf.keras.models.load_model(
    os.path.join("saved_ml_models", "brain_tumor_classification"))


def convert_image_to_gray(image):
    if image.mode == "RGB":
        return tf.image.rgb_to_grayscale(image)
    if image.mode == "RGBA":
        image = np.array(image, dtype=float32)
        return tf.image.decode_png(image)
    raise Exception("Unsupported Color Format")


def preprocess_image(image):
    image = Image.open(io.BytesIO(base64.decodebytes(bytes(image, "utf-8"))))
    image = convert_image_to_gray(image)
    image = tf.image.resize(image, [256, 256])
    normalize = tf.keras.layers.Rescaling(1. / 255)
    image = normalize(image)
    image = tf.expand_dims(image, axis=0)
    return image


def predict(image):
    image = preprocess_image(image)
    predication = brain_tumor_classification_model.predict(image, verbose=0)[0]
    return {"meningioma": predication[0], "glioma": predication[1], "pituitary tumor": predication[2]}


# dev only
def show_img(image):
    window_name = 'image'
    cv2.imshow(window_name, np.array(image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
