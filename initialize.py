from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()

DEBUG = (input("NOT Production Environment? [y/n]") == "y")