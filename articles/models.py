from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length = 200)
    body = RichTextUploadingField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

