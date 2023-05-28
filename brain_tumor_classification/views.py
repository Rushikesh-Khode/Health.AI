from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User
from .ml_model import predict, is_mri_image
from .seralizer import PredicationSerializer
from .models import Predictions

one_mb_str_len = 1048576


@api_view(["POST"])
def get_brain_tumor_classification_prediction(request, format=None):
    image = request.data["image"].replace("data:image/jpeg;base64,", "")
    force_push = bool(request.data["forcePush"])
    email = request.META["HTTP_AUTHORIZATION"].split(" ")[0]
    user = User.objects.get(email=email)

    if not image:
        return Response({"error": "Image Size More Than 1mb"}, 404)

    if len(image) > one_mb_str_len:
        return Response({"error": "Image Size More Than 1mb"}, 404)

    is_valid_image = is_mri_image(image)

    if not force_push and not is_valid_image:
        return Response({"email": email, "prediction": "Not Valid Mri Image"},
                        status=406)

    prediction = predict(image)
    data = {
        "user": user.pk,
        "image": image,
        "glioma": prediction["glioma"],
        "meningioma": prediction["meningioma"],
        "no_tumor": prediction["notumor"],
        "pituitary": prediction["pituitary"],
    }
    serializer = PredicationSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({"email": email, "prediction": prediction},
                        status=200)

    return Response({"error": serializer.errors}, status=400)


@api_view(["GET"])
def get_predictions_history(request, images=0, format=None):
    email = request.META["HTTP_AUTHORIZATION"].split(" ")[0]
    user = User.objects.get(email=email)
    prediction_history = Predictions.objects.filter(user=user.pk).order_by("createdAt")
    history_data = []

    if images not in (1, 0):
        return Response({"error": "bad url format at /images/"}, 400)

    for prediction in prediction_history:
        if images:
            history_data.append(
                {
                    "user": prediction.user.email,
                    "image": prediction.image,
                    "glioma": prediction.glioma,
                    "meningioma": prediction.meningioma,
                    "no_tumor": prediction.no_tumor,
                    "pituitary": prediction.pituitary,
                }
            )
        else:
            history_data.append(
                {
                    "user": prediction.user.email,
                    "glioma": prediction.glioma,
                    "meningioma": prediction.meningioma,
                    "no_tumor": prediction.no_tumor,
                    "pituitary": prediction.pituitary,
                }
            )

    return Response({"history": history_data}, 200)
