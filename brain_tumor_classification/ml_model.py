import base64
import io
import os
import cv2
import imutils
import numpy as np
import tensorflow as tf
from PIL import Image

brain_tumor_classification_model = tf.keras.models.load_model(
    os.path.join("saved_ml_models", "brain_tumor_classification"))
mri_image_detector = tf.keras.models.load_model(
    os.path.join("saved_ml_models", "mri_image_detector"))


def crop_img(img):
    channels = img.shape[2] if len(img.shape) > 2 else 0
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) if channels > 0 else img
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    ADD_PIXELS = 0
    new_img = img[extTop[1] - ADD_PIXELS:extBot[1] + ADD_PIXELS,
              extLeft[0] - ADD_PIXELS:extRight[0] + ADD_PIXELS].copy()

    return new_img


def preprocess_image(image, crop=False):
    image = Image.open(io.BytesIO(base64.decodebytes(bytes(image, "utf-8"))))
    image = np.array(image)
    if len(image) == 3 and image.shape[2] == 4:
        image = image[:, :, :3]
    if crop:
        image = crop_img(image)
    image = image if len(image.shape) > 2 else cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image = tf.image.resize(image, [256, 256])
    image = tf.expand_dims(image, axis=0)
    return image


def predict(image):
    image = preprocess_image(image, crop=True)
    predication = brain_tumor_classification_model.predict(image, verbose=0)[0]

    return {'glioma': predication[0], 'meningioma': predication[1], 'notumor': predication[2],
            'pituitary': predication[3]}


def is_mri_image(image):
    image = preprocess_image(image)
    predication = mri_image_detector.predict(image, verbose=0)[0]
    return bool(round(predication[0]))
