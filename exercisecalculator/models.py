from django.db import models

class Vocations(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Skills(models.Model):
    name = models.CharField(max_length=50)
    vocations = models.ForeignKey(Vocations, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name