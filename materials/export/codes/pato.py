from django.conf import settings
import os
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

class pato_export_model():
    def __init__(self, matv, code_name):
        self.matv = matv
        self.mat_name = matv.material.name
        self.mat_version = matv.version
        self.code_name = code_name

    def create_file(self):
        mycwd = os.getcwd()
        folder_base = settings.STATIC_ROOT + "/tmp"
        folder_name = self.code_name + "_" + self.mat_name + "_" + self.mat_version
        full_folder_name = folder_base + "/" + folder_name
        if os.path.exists(full_folder_name):
            os.system("rm -rf " + full_folder_name)
        os.makedirs(full_folder_name)
        os.chdir(folder_base)
        os.system("rm -f " + folder_name+".zip")
        file_name = full_folder_name+"/file"
        f = open(file_name, "w")
        f.write(self.code_name + "_" + self.mat_name + "_" + self.mat_version)
        f.close()
        zip_file = zipfile.ZipFile(folder_name+".zip", 'w', zipfile.ZIP_DEFLATED)
        zipdir(folder_name, zip_file)
        zip_file.close()
        os.system("rm -rf " + full_folder_name)
        os.chdir(mycwd)
        return full_folder_name+".zip"