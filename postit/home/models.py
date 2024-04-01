from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Uploads(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    file = models.FileField()
    submission_page = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title