from __future__ import unicode_literals

from django.db import models


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='ortophotos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class TiledDocument(models.Model):
    description = models.CharField(max_length=255, blank=True)
    tiles_folder = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    size_x = models.IntegerField(default=22615)
    size_y = models.IntegerField(default=17283)

    def __str__(self):
        return self.description
