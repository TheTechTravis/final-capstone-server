from django.db import models
from .my_user import MyUser


class Task(models.Model):

    user = models.ForeignKey("MyUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    creation_date = models.DateField(auto_now=False, auto_now_add=False)
    is_complete = models.BooleanField()
