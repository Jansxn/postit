from django.db import models

# Create your models here.

class Member(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    passwd = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.fname} {self.lname}"