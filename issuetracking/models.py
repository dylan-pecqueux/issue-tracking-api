from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=255)


class Contributor(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    PERMISSION_CHOICES = [('C', 'contributeur'), ('R', 'responsable')]
    permission = models.CharField(max_length=255, choices=PERMISSION_CHOICES)
    role = models.CharField(max_length=255)

class Issue(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="author")
    assignee = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="assignee")
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=1000)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

