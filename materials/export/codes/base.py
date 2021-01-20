from django.conf import settings
import os
import zipfile

# Zip all the files in a directory
def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

# Basic export model class
class base_export_model():

    # Initialize the class
    def __init__(self, matv, code_name):
        self.matv = matv
        self.mat_name = matv.material.name
        self.mat_version = matv.version
        self.code_name = code_name

    # Check if 2 arrays have the same elements
    def check_arrays(self, a, b):
        if len(a) != len(b):
            return False
        bool = True
        for i,a_i in enumerate(a):
            if (a[i] != b[i]):
                bool = False
        return bool

    # Create a dummy file with the code name, the material name and the material version.
    def create_file(self):
        # Get current folder
        mycwd = os.getcwd()
        # Folder name
        folder_base = settings.STATIC_ROOT + "/tmp"
        folder_name = self.code_name + "_" + self.mat_name + "_" + self.mat_version
        full_folder_name = folder_base + "/" + folder_name
        # Clean folders
        if os.path.exists(full_folder_name):
            os.system("rm -rf " + full_folder_name)
        os.makedirs(full_folder_name)
        os.chdir(folder_base)
        os.system("rm -f " + folder_name+".zip")
        # Create a dummy file
        file_name = folder_name+"/file"
        f = open(file_name, "w")
        f.write(folder_name)
        f.close()
        zip_file = zipfile.ZipFile(folder_name+".zip", 'w', zipfile.ZIP_DEFLATED)
        zipdir(folder_name, zip_file)
        zip_file.close()
        os.system("rm -rf " + full_folder_name)
        os.chdir(mycwd)
        return full_folder_name+".zip"