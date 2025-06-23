from django.core.management.utils import get_random_secret_key
import secrets

print(secrets.token_urlsafe(64))
# print(get_random_secret_key())