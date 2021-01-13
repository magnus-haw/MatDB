from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    affiliation = models.CharField(max_length=100, null=True, blank=True)
    office = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name