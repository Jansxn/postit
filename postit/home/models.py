from django.db import models

# Create your models here.
class Uploads(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    file = models.FileField()

    def __str__(self):
        return self.title