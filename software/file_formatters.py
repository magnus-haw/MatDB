from django.conf import settings
import os
import sys
import zipfile

import re
import numpy as np
import pandas as pd


from .models import Software, SoftwareVersion
from itarmaterials.models import ITARMaterial, ITARMaterialVersion, ITARVariableProperty, ITARConstProperty, ITARMatrixProperty
from materials.models import MaterialVersion, Material, VariableProperty, ConstProperty, MatrixProperty
from units.models import ComboUnit

# Zip all the files in a directory
def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

# Check if 2 arrays have the same elements
def check_arrays(a, b):
    if len(a) != len(b):
        return False

    for i,a_i in enumerate(a):
        if (a[i] != b[i]):
            return False
    return True

# Basic formatter model class
class Formatter(object):

    # Initialize the class
    def __init__(self):
        # Get current folder
        self.cwd = os.getcwd()

    # Create a dummy file with the code name, the material name and the material version.
    def export_file(self, matv, softv):
        self.matv = matv
        self.softv= softv
        self.mat_name = matv.material.name
        self.mat_version = matv.version
        self.code_name = softv.software.name
        self.code_version = softv.version

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
        os.chdir(self.cwd)
        return full_folder_name+".zip"

    def parse_file(self):
        pass

    def upload_file(self):
        pass

class PATO_formatter(Formatter):
    # Write the char, virgin and constantProperties files
    def export_file(self, matv, softv):
        self.matv = matv
        self.softv= softv
        self.mat_name = matv.material.name
        self.mat_version = matv.version
        self.code_name = softv.software.name
        self.code_version = softv.version
        

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
        # Create virgin and char files
        char_file_name = full_folder_name+"/char"
        f_char = open(char_file_name, "w")
        virgin_file_name = full_folder_name+"/virgin"
        f_virgin = open(virgin_file_name, "w")
        names = ["// p(Pa)","T(K)","cp(J/kg/K)","h(J/kg)","ki(W/m/K)","kj(W/m/K)","kk(W/m/K)","emissivity","absorptivity"]
        header_char = "// " + self.mat_name + "_" + self.mat_version + "\n"  \
               + "// Tabulated char-material properties as a function of pressure and temperature.\n\n"
        line = ""
        padding = 14
        for i in names:
            line = line + "{:<{padding}}".format(i,padding=padding)
        header_char = header_char + line + "\n"
        f_char.write(header_char)
        header_virgin = header_char.replace("char","virgin")
        f_virgin.write(header_virgin)
        varprops = self.matv.variableproperty_set.all().order_by('state')
        data_char = []
        data_p_char = []
        data_T_char = []
        data_virgin = []
        data_p_virgin = []
        data_T_virgin = []
        for var in varprops:
            if var.state == 1: # char
                if len(data_p_char)>0 and not check_arrays(data_p_char,var.p):
                    sys.exit("Error: pressure is different between variables.")
                data_p_char = var.p
                if len(data_T_char)>0 and not check_arrays(data_T_char,var.T):
                    sys.exit("Error: temperature is different between variables.")
                data_T_char = var.T
                data_char.append(var.values)
            if var.state == 0: # virgin
                if len(data_p_virgin)>0 and not check_arrays(data_p_virgin,var.p):
                    sys.exit("Error: pressure is different between variables.")
                data_p_virgin = var.p
                if len(data_T_virgin)>0 and not check_arrays(data_T_virgin,var.T):
                    sys.exit("Error: temperature is different between variables.")
                data_T_virgin = var.T
                data_virgin.append(var.values)
        for i,pI in enumerate(data_p_char):
            f_char.write("{:<{padding}}".format("{0:.3e}".format(data_p_char[i]),padding=padding))
            f_char.write("{:<{padding}}".format("{0:.3e}".format(data_T_char[i]),padding=padding))
            for j, vI in enumerate(data_char):
                f_char.write("{:<{padding}}".format("{0:.3e}".format(data_char[j][i]),padding=padding))
            f_char.write("\n")
        for i,pI in enumerate(data_p_virgin):
            f_virgin.write("{:<{padding}}".format("{0:.3e}".format(data_p_virgin[i]),padding=padding))
            f_virgin.write("{:<{padding}}".format("{0:.3e}".format(data_T_virgin[i]),padding=padding))
            for j, vI in enumerate(data_virgin):
                f_virgin.write("{:<{padding}}".format("{0:.3e}".format(data_virgin[j][i]),padding=padding))
            f_virgin.write("\n")
        f_char.close()
        f_virgin.close()
        # Create the constant properties file
        const_file_name = full_folder_name+"/constantProperties"
        f_const = open(const_file_name, "w")
        header_const = "// Constant property directory. Update as needed.\n" \
                    + "FoamFile\n{\n\tversion     2.0;\n\tformat      ascii;\n\tclass       dictionary;\n\tobject      constantProperties;\n}" \
                    + "// * * * * * *  Units * * * * * [kg m s K mol A cd] * * * * * * * * * * * * * //\n" \
                    + "// e.g. W: kg m^2 s^{-3}        [1 2 -3 0 0 0 0]\n\n" \
                    + "/****           Universal constants                                             ****/\n" \
                    + "R               R               [1 2 -2 -1 -1 0 0]      8.314471469;\n" \
                    + "sigmaPlanck     sigmaPlanck     [1 0 -3 -1 0 0 0]       5.6697e-8;\n\n"
        f_const.write(header_const)
        constprops = self.matv.constproperty_set.all()
        for i in constprops:
            dims = i.unit.dims()
            units_to_OF = "["
            for j, dims_j in enumerate(dims):
                end = " "
                if j == len(dims) - 1:
                    end = "]"
                units_to_OF = units_to_OF + str(int(dims_j)) + end
            name = i.name
            name = name.split(" ")[0] # remove the units in the name
            f_const.write("// " + name + "\n")
            f_const.write(name + " " + name  + " " + units_to_OF + " " + str(i.value) + "\n\n")
        f_const.close()
        zip_file = zipfile.ZipFile(folder_name+".zip", 'w', zipfile.ZIP_DEFLATED)
        zipdir(folder_name, zip_file)
        zip_file.close()
        os.system("rm -rf " + full_folder_name)
        os.chdir(self.cwd)
        return full_folder_name+".zip"

    def parse_file(self, fpath_or_buffer):
        """Parses PATO material csv format

        Args:
            fpath_or_buffer (filepath): path to csv file
        """
        _df = pd.read_csv(fpath_or_buffer, encoding='unicode_escape')
        df = _df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        d = df.values

        material,version,date,form = d[0,0:4]

        # Parse variable params table
        headers = d[3].astype('str')
        split_col_index = np.where(headers == 'nan')[0][0]
        nrows = np.where(d[4:,0].astype('str') == 'nan')[0][0]
        vparams={}
        for i in range(0,split_col_index):
            vparams[headers[i]] = d[4:4+nrows,i].astype('float')
        
        # Parse const params table
        nrows = np.where(d[3:,split_col_index+1].astype('str') == 'nan')[0][0]
        const_names = d[3:3+nrows,split_col_index+1].astype('str')
        const_vals = d[3:3+nrows,split_col_index+2].astype('str')
        const_notes= d[3:3+nrows,split_col_index+3].astype('str')

        PATO_fmt = {'material':material, 'version': version, 'date':date,'vparams':vparams,
                    'const_names':const_names, "const_vals":const_vals,"const_notes":const_notes}

        return PATO_fmt

    def upload_file(self, fpath_or_buffer, ITAR=False):
        Pform = self.parse_file(fpath_or_buffer)
        matName = Pform['material']
        
        if ITAR:
            mat = ITARMaterial.objects.get(name=matName)
            matv,flag = ITARMaterialVersion.objects.get_or_create(material=mat, version=Pform['version'])
        else:
            mat = Material.objects.get(name=matName)
            matv,flag = MaterialVersion.objects.get_or_create(material=mat, version=Pform['version'])
        
        units = ComboUnit.objects.all()
        none_unit = ComboUnit.objects.get(name='None')
        matv.save()

        p = Pform['vparams']['Pressure(Pa)']
        T = Pform['vparams']['Temperature(K)']
        for key in Pform['vparams'].keys():
            if key not in ['Pressure(Pa)', 'Temperature(K)']:
                if ITAR:
                    vprop,fl = ITARVariableProperty.objects.get_or_create(material_version=matv, name=key)
                else:
                    vprop,fl = VariableProperty.objects.get_or_create(material_version=matv, name=key)
                vprop.p = p
                vprop.T = T
                vprop.values = Pform['vparams'][key]
                if 'virgin' in key:
                    vprop.state = 0
                elif 'char' in key:
                    vprop.state = 1
                else:
                    vprop.state = 2
                    print(key)

                # extract units
                vprop.unit = none_unit
                ustrings = re.findall('\(.*?\)',key)
                if len(ustrings) == 1 and ustrings[0] != '(-)':
                    for unit in units:
                        if ustrings[0][1:-1] in unit.alternate_names:
                            vprop.unit = unit
                
                vprop.save()
        
        names, vals, notes = Pform['const_names'],Pform['const_vals'],Pform['const_notes']
        for i in range(0,len(names)):
            state =0
            if "char" in notes[i]:
                state = 1
            elif "pyrolysis" in notes[i]:
                state = 2

            # extract units
            ustrings = re.findall('\(.*?\)',names[i])
            if len(ustrings) == 1 and ustrings[0] != '(-)':
                for unit in units:
                    if ustrings[0][1:-1] in unit.alternate_names:
                        myunit = unit
            else:
                myunit = none_unit

            if vals[i][0] == '(':
                if ITAR:
                    mx,flag = ITARMatrixProperty.objects.get_or_create(name=names[i],material_version=matv,state=state)
                else:
                    mx,flag = MatrixProperty.objects.get_or_create(name=names[i],material_version=matv,state=state)
                mx.unit = myunit
                mx.value=vals[i]
                mx.description = "matrix elements"
                mx.save()

            else:
                if ITAR:
                    const,flag = ITARConstProperty.objects.get_or_create(material_version = matv, state=state, name=names[i])
                else:
                    const,flag = ConstProperty.objects.get_or_create(material_version = matv, state=state, name=names[i])
                const.description=notes[i]
                const.value=float(vals[i])
                const.unit = myunit
                const.save()

class FIAT_formatter(Formatter):
    pass

class ICARUS_formatter(Formatter):
    pass