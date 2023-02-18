from users.models import User
from .Auth import validate_token


class X_Auth_Middleware:
    excluded_paths = [
        "users/login.json",
        "users/register.json",
        "users/logout.json",
        "admin/"
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.is_excluded_path(request.path):
            headers = request.META["HTTP_AUTHORIZATION"].split(" ")
            x_auth_token = headers[1]
            email = headers[0]
            user = User.objects.get(email=email)

            if not validate_token(user, x_auth_token):
                raise Exception("Unauthorized Access")
            request.userEmail = user.email

        return self.get_response(request)

    def is_excluded_path(self, path: str):
        for excluded_path in self.excluded_paths:
            if path.find(excluded_path) >= 0:
                return True
        return False
