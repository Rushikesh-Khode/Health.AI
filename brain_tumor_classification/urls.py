from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import get_brain_tumor_classification_prediction, get_predictions_history

urlpatterns = [
    path("predict/", get_brain_tumor_classification_prediction, name="brain_tumor_classification"),
    path("predict/history/<int:images>/", get_predictions_history, name="predictions_history"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
