from rest_framework import serializers
from .models import Predictions


class PredicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predictions
        fields = ["user", "image", "createdAt", "glioma", "meningioma", "no_tumor", "pituitary"]
