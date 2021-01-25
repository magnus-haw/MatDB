
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MatDB.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from software.models import ExportFormat, SoftwareVersion, Software
from materials.models import MaterialVersion

if "delete" in sys.argv:
    ExportFormat.objects.all().delete()

if "update" in sys.argv:
    latest_software = {}
    for softv in SoftwareVersion.objects.all():
        if softv.software.name not in latest_software.keys():
            latest_software[softv.software.name] = softv.version
        else:
            if latest_software[softv.software.name] < softv.version:
                latest_software[softv.software.name] = softv.version
    for i in latest_software.keys():
        soft = Software.objects.get(name=i)
        softv = SoftwareVersion.objects.get(version=latest_software[i], software=soft)
        for matv in MaterialVersion.objects.all():
            description = "<p>" + softv.software.name + " " + softv.version + ": " + matv.material.name + " " + matv.version + "</p>"
            exp,flag = ExportFormat.objects.get_or_create(material_version=matv, software_version=softv, description=description)
            exp.save()

if "print" in sys.argv:
    for i,obj_i in enumerate(ExportFormat.objects.all()):
        print("Export Format object " + str(i))
        print("\t"+obj_i.software_version.software.name)
        print("\t"+obj_i.software_version.version)
        print("\t"+obj_i.material_version.material.name)
        print("\t"+obj_i.material_version.version)
        print("\t"+obj_i.description)


