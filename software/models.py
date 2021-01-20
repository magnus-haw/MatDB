from django.db import models

from materials.models import BaseModel
from contacts.models import Person

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.
class AbstractSoftware(BaseModel):
    name = models.CharField(max_length=500,unique=True)
    short_name = models.CharField(max_length=25,unique=True,null=True,blank=True)
    link = models.URLField(blank=False, null=True)
    short_description = models.CharField(max_length=200,null=True,blank=True)
    point_of_contact = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=False, related_name='poc')
    description = RichTextUploadingField(blank=False,null=True)
    how_to_get = RichTextUploadingField(blank=False,null=True)
    how_to_use = RichTextUploadingField(blank=False,null=True)
    image = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class AbstractSoftwareVersion(BaseModel):
    version = models.CharField(max_length=500,unique=True)
    repository = models.URLField(blank=False, null=True)
    short_description = models.CharField(max_length=200,null=True,blank=True)
    lead_developer = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_developer')
    other_contact = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='other_contact')
    version_changes = RichTextUploadingField(blank=False,null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class AbstractTutorial(BaseModel):
    software_version = models.ForeignKey(SoftwareVersion, on_delete=models.CASCADE)
    name = models.CharField(max_length=500,unique=True)
    link = models.URLField(blank=False, null=True)
    short_description = models.CharField(max_length=200,null=True,blank=True)
    description = RichTextUploadingField(blank=False,null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Software(AbstractSoftware):
    pass

class SoftwareVersion(AbstractSoftwareVersion):
    pass

class Tutorial(AbstractTutorial):
    pass