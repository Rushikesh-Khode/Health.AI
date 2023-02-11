import random

from rest_framework.decorators import api_view
from users.seralizers import UserSerializer
from argon2 import PasswordHasher
from rest_framework.response import Response
from .models import User
from datetime import datetime

from users.utility.passwordUtility import validate_password

password_generator = PasswordHasher()


@api_view(["POST"])
def register_user(request, format=None):
    serializer = UserSerializer(data=request.data)
    password2 = None

    if ("password2" in serializer.initial_data) and serializer.initial_data["password2"]:
        password2 = serializer.initial_data["password2"]
    else:
        Response({"error": {"password2": "password 2 not found"}}, status=400)

    if serializer.is_valid():
        if validate_password(password=serializer.validated_data["password"]):
            if serializer.validated_data["password"] == password2:
                serializer.validated_data["password"] = password_generator.hash(serializer.validated_data["password"])
                serializer.save()

                # TODO: redirect to login page
                return Response({"email": serializer.validated_data["email"]})
            else:

                return Response({"error": {"password": "password does not match"}}, status=400)
        else:

            return Response({"error": {
                "password": "password should be greater than 8 characters and should contain 1 capital, 1 small, "
                            "1 digit & 1 special character"}},
                status=400)

    return Response({"error": serializer.errors}, status=400)


@api_view(["POST"])
def login_user(request, format=None):
    user = User.objects.get(email=request.data["email"])

    if user and password_generator.verify(user.password, request.data["password"]):
        x_auth_token = password_generator.hash(
            user.email + str(user.birthday) + str(user.gender) + str(random.randint(100000, 1000000000)))
        user.x_auth_token = x_auth_token
        user.x_auth_created_at = datetime.now()

        user.save()
        # TODO : redirect to dashboard
        return Response({"email": request.data["email"], "x-auth-token": x_auth_token})

    return Response({"error": {"user": "email or password invalid"}})
