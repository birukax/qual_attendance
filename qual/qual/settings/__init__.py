import os

environment = os.environ.get("DJANGO_ENV", "local")

if environment == "prod":
    from .prod import *
elif environment == "local":
    from .local import *
else:
    from .local import *
