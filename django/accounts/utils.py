from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode


def urlencode_pk(pk: int) -> str:
    return urlsafe_base64_encode(force_bytes(pk))


def urldecode_pk(pk: str) -> int:
    return int(force_text(urlsafe_base64_decode(pk)))


def secure_dump(value: str) -> str:
    return signing.dumps(value)


def secure_loads(value: str) -> str:
    return signing.loads(value, max_age=settings.SECRET_TIMEOUT_SECONDS)


def make_user_token(user) -> str:
    return default_token_generator.make_token(user)


def compare_user_token(user, token: str) -> bool:
    return default_token_generator.check_token(user, token)
