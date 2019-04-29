from django.db import models


# Create your models here.

class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)


class Nodo(models.Model):
    name = models.TextField(blank=True)
