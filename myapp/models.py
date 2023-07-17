from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    USER_LEVELS = (
        ('Super-admin', 'Super-admin'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    )

    user_level  = models.CharField(max_length=20, choices=USER_LEVELS)


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
