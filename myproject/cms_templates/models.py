from django.db import models

# Create your models here.

class Resource(models.Model):
    name = models.CharField(max_length=128)
    cont = models.TextField()
    def __str__(self):
	    return self.name
