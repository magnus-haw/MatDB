
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MatDB.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.shortcuts import get_object_or_404
from materials.export.codes import export_models
from django.conf import settings
from materials.models import DownloadModel
from materials.models import MaterialVersion

if "delete" in sys.argv:
    DownloadModel.objects.all().delete()

if "update" in sys.argv:
    for matv in MaterialVersion.objects.all():
        for name in export_models:
            code_name = name
            down,flag = DownloadModel.objects.get_or_create(material_version=matv, code_name=code_name)
            down.save()

print("New DownloadModel = ", end="")
print(DownloadModel.objects.all())
