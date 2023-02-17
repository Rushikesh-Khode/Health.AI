from rest_framework.decorators import api_view
from rest_framework.response import Response
from .ml_model import predict


@api_view(["POST"])
def get_brain_tumor_classification_prediction(request, format=None):
    image = request.data["image"].replace("data:image/jpeg;base64,", "")

    if not image:
        raise Exception("No image found")

    prediction = predict(image)

    return Response(prediction)
