from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class userHistory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    test_name = models.TextField()
    result = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

class subscribers(models.Model):
    email = models.EmailField()

