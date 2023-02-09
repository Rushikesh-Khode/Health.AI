from rest_framework.decorators import api_view
from django.http import JsonResponse
from users.models import User
from users.seralizers import UserSerializer
from argon2 import PasswordHasher


# Create your views here.

@api_view(['GET'])
def get_all(request):
    users = User.objects.get(pk=1)
    users.password = PasswordHasher().hash(password=users.password)
    users.save()
    return JsonResponse(UserSerializer(users).data)
