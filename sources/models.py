from django.db import models
from materials.models import BaseModel, Material
from itarmaterials.models import ITARMaterial

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

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

REFERENCE_TYPES = (
    (0,'Journal article'),
    (1,'Unpublished report'),
    (2,'Book'),
    (3,'Test data'),
    (4,'Sim data'),
    (5,'Poster'),
    (6,'Presentation'),
    (7,'Other'),
)

class Reference(BaseModel):
    title = models.CharField(max_length = 500)
    doc_num = models.CharField(max_length = 100, null=True, blank=True)
    reftype = models.PositiveIntegerField(choices=REFERENCE_TYPES, default=0)
    published = models.DateField(null=True, blank=True)
    authors = models.CharField(max_length = 50)
    materials = models.ManyToManyField(Material, blank=True)
    itarmaterials = models.ManyToManyField(ITARMaterial, blank=True)
    softwares = models.ManyToManyField('software.Software', blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    
    file = models.FileField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

class Tutorial(BaseModel):
    name = models.CharField(max_length=500,unique=True)
    link = models.URLField(blank=True, null=True)
    short_description = models.CharField(max_length=200,null=True,blank=True)
    description = RichTextUploadingField(blank=False,null=True)
    materials = models.ManyToManyField(Material, blank=True)
    itarmaterials = models.ManyToManyField(ITARMaterial, blank=True)
    softwares = models.ManyToManyField('software.Software', blank=True)
    file = models.FileField(null=True, blank=True)
    
    def __str__(self):
        return self.name