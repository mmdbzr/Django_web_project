from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=False)

