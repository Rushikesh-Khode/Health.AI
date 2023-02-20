from argon2 import PasswordHasher
from rest_framework.decorators import api_view
from rest_framework.response import Response
from auth_service import Auth
from users.seralizers import UserSerializer
from users.utility.passwordUtility import validate_password
from .models import User

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
    try:
        user = User.objects.get(email=request.data["email"])
    except:
        return Response({"error": {"users": "users not found"}})

    if user and request.data["password"] and password_generator.verify(user.password, request.data["password"]):
        x_auth_token = Auth.generate_token(user)

        return Response({"email": request.data["email"], "x-auth-token": x_auth_token})

    return Response({"error": {"users": "email or password invalid"}})


@api_view(["GET"])
def logout_user(request, format=None):
    email = request.META["HTTP_AUTHORIZATION"].split(" ")[0]
    user = User.objects.get(email=email)

    Auth.invalidate_token(user)

    return Response({"email": email})
