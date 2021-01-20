
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

for i in range(1,3):
    if "delete" in sys.argv:
        for obj in DownloadModel.objects.all():
            obj.delete()
    if "update" in sys.argv:
        matv = get_object_or_404(MaterialVersion, pk=i)
        for name in export_models:
            code_name = name
            file_name = name + "_" + matv.material.name + "_" + matv.version
            down,flag = DownloadModel.objects.get_or_create(material=matv, code_name=code_name, file_name=file_name)
            down.save()

print("New DownloadModel = ", end="")
print(DownloadModel.objects.all())
