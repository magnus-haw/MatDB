from django.db import models

from materials.models import BaseModel, MaterialVersion

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.
class AbstractSoftware(BaseModel):
    name = models.CharField(max_length=500,unique=True)
    short_name = models.CharField(max_length=25,unique=True,null=True,blank=True)
    repository = models.URLField(blank=True, null=True)
    short_description = models.CharField(max_length=200,null=True,blank=True)
    point_of_contact = models.ForeignKey('sources.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='poc')
    description = RichTextUploadingField(blank=True,null=True)
    image = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class AbstractSoftwareVersion(BaseModel):
    software = models.ForeignKey("Software", on_delete=models.CASCADE)
    version = models.CharField(max_length=25)
    published = models.DateField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    short_description = models.CharField(max_length=200,null=True,blank=True)
    lead_developer = models.ForeignKey('sources.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_developer')
    other_contact = models.ForeignKey('sources.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='other_contact')
    version_changes = RichTextUploadingField(blank=True,null=True)
    
    def __str__(self):
        return self.software.name + "-" + self.version

    class Meta:
        abstract = True

class AbstractExportFormat(BaseModel):
    material_version = models.ForeignKey(MaterialVersion, on_delete=models.CASCADE)
    software_version = models.ForeignKey('SoftwareVersion', on_delete=models.CASCADE)
    description = RichTextUploadingField(blank=False,null=True)

    def __str__(self):
        name = self.software_version.software.name
        name += "-" + self.software_version.version 
        name += "_" + self.material_version.material.name
        name += "-" + self.material_version.version 
        return name

    class Meta:
        abstract = True

class Software(AbstractSoftware):
    pass

class SoftwareVersion(AbstractSoftwareVersion):
    pass

class ExportFormat(AbstractExportFormat):

    class Meta:
        verbose_name_plural = "Export format"