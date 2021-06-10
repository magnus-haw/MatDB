from django.db import models
from django.db.models import Max
from django.core.validators import int_list_validator

from materials.models import BaseModel, MaterialProperty, get_version_value

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
    version = models.CharField(max_length=25, validators=[int_list_validator(sep='.')])
    version_value = models.PositiveIntegerField(null=True,blank=True)
    published = models.DateField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    short_description = models.CharField(max_length=200,null=True,blank=True)
    lead_developer = models.ForeignKey('sources.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_developer')
    other_contact = models.ForeignKey('sources.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='other_contact')
    version_changes = RichTextUploadingField(blank=True,null=True)
    can_export = models.BooleanField(default=False)

    material_properties = models.ManyToManyField(MaterialProperty, related_name="software_versions")
    
    def __str__(self):
        return self.software.name + "-" + self.version

    def save(self, *args, **kwargs):
        self.version_value = get_version_value(self.version) # enforce version serialization
        super().save(*args, **kwargs)  # Call the parent save() method.

    class Meta:
        abstract = True
        unique_together = ('software', 'version',)
        ordering = ['-version_value']

class Software(AbstractSoftware):
    
    def get_latest_version(self):
        try: 
            ret = self.softwareversion_set.all().order_by('-version_value')[0]
        except:
            ret = None
        return ret

class SoftwareVersion(AbstractSoftwareVersion):

    def is_latest(self):
        vmax = SoftwareVersion.objects.filter(software=self.software).aggregate(Max('version_value'))
        if self.version_value == vmax['version_value__max']:
            return True
        else:
            return False

    def get_latest(self):
        try: 
            ret = SoftwareVersion.objects.all().order_by('-version_value')[0]
        except:
            ret = None
        return ret

# class AbstractExportFormat(BaseModel):
#     material_version = models.ForeignKey(MaterialVersion, on_delete=models.CASCADE)
#     software_version = models.ForeignKey('SoftwareVersion', on_delete=models.CASCADE)
#     description = RichTextUploadingField(blank=False,null=True)
    
#     def __str__(self):
#         name = self.software_version.software.name
#         name += "-" + self.software_version.version 
#         name += "_" + self.material_version.material.name
#         name += "-" + self.material_version.version 
#         return name

#     class Meta:
#         abstract = True
#         unique_together = ('software_version', 'material_version',)


# class ExportFormat(AbstractExportFormat):

#     class Meta:
#         verbose_name_plural = "Export format"

# class ITARExportFormat(AbstractExportFormat):
#     material_version = models.ForeignKey(ITARMaterialVersion, on_delete=models.CASCADE)
#     itarmaterial_properties = models.ManyToManyField(ITARMaterialProperty, related_name="itarmaterials")

#     class Meta:
#         verbose_name_plural = "ITAR export format"