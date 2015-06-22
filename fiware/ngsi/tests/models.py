from django.db import models


class TestModel(models.Model):
    c = models.CharField(max_length=10)
    i = models.IntegerField()
