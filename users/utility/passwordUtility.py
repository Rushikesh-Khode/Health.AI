import re


def validate_password(password: str):
    if len(password) < 8 or not re.findall("\d", password) or not re.findall("[A-Z]", password) or not re.findall(
            "[a-z]", password) or not re.findall('[()[\]{}|\\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
        return False
    return True
