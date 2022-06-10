from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
debug = (input("Debug Environment? [y/n]") != "n")

with open("./hicomm/secret_settings.py", "w") as f:
    f.write(f"SECRET_KEY = \"{secret_key}\"\n")
    f.write(f"DEBUG = {debug}\n")

