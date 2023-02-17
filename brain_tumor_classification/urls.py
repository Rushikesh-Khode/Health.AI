from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import get_brain_tumor_classification_prediction

urlpatterns = [
    path("predict/", get_brain_tumor_classification_prediction, name="brain_tumor_classification")
]

urlpatterns = format_suffix_patterns(urlpatterns)
