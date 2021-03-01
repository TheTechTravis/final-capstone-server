from django.db import models
from django.contrib.auth.models import User


# Blueprint for creating a single application user
class MyUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
