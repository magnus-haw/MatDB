from django.conf import settings
import os
import sys
import zipfile
import re
import numpy as np
import pandas as pd
from datetime import date

from .models import ExportFormat, Software, SoftwareVersion, ITARExportFormat
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

# Index in the list that contains the substring
def index_containing_substring(list, substring):
    for i, s in enumerate(list):
        if substring in s:
              return i
    return -1

# Format the element with a list of formats
def format_list(list, elem):
    new_elem = elem
    for i in list:
        new_elem = i.format(new_elem)
    return new_elem

# Remove the same elements in a list
def remove_same_in_list(list):
    diff = []
    for i in list:
        if i not in diff:
            diff.append(i)
    return diff


# Basic formatter model class
class Formatter(object):

    # Initialize the class
    def __init__(self):
        # Get current folder
        self.cwd = os.getcwd()

    # Create an error file
    def error_file(self, string):
        folder_base = settings.STATIC_ROOT + "/tmp"
        file_name = folder_base + "/error.txt"
        f = open(file_name, "w")
        msg = "Error for the \""+ self.code_name + "\" export of the material \"" + self.mat_name + "\" version \"" + self.mat_version + "\"\n"
        f.write(msg+string)
        f.close()
        return file_name

    # Update the ExportFormat for a new material version
    def update_export_format(self, matv):
        softwares = Software.objects.all()
        for soft in softwares:
            softv = SoftwareVersion.objects.filter(software=soft).order_by('-version_value').first()
            if softv is not None:
                description = soft.name + " " + softv.version + ": " + matv.material.name + " " + matv.version
                if isinstance(matv, MaterialVersion):
                    exp, flag = ExportFormat.objects.get_or_create(material_version=matv, software_version=softv, description=description)
                    exp.save()
                elif isinstance(matv, ITARMaterialVersion):
                    exp, flag = ITARExportFormat.objects.get_or_create(material_version=matv, software_version=softv, description=description)
                    exp.save()

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
        software = Software.objects.get(name="PATO")
        varprops = self.matv.variableproperty_set.all().order_by('state').filter(software=software)
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
                    + "sigmaPlanck     sigmaPlanck     [1 0 -3 -1 0 0 0]       5.6697e-8;\n\n" \
                    + "/***            Anisotropic conductivity parameters: main directions and linear factors         ***/\n" \
                    + "//              kxyz = tP & kijk' & P\n" \
                    + "// 1- Express the main directions (ijk) of the diagonal conductivity matrix in the basis of the mesh (xyz) \n" \
                    + "//                                                      (i j k)                 ex. rotation a (in radians) around axis z\n" \
                    + "tP              tP              [0 0 0 0 0 0 0]         (1 0 0   // x           (cosa -sina 0\n" \
                    + "                                                         0 1 0   // y            sina  cosa 0\n" \
                    + "                                                         0 0 1); // z            0       0  1)\n" \
                    + "// 2 - Linear factors\n" \
                    + "kiCoef          kiCoef          [0 0 0 0 0 0 0]         1;       // to multiply column ki of the input files 'char' and 'virgin' by a linear factor: ki' = kiCoef*ki\n" \
                    + "kjCoef          kjCoef          [0 0 0 0 0 0 0]         1;       // idem for kj\n" \
                    + "kkCoef          kkCoef          [0 0 0 0 0 0 0]         1;       // idem for kk\n\n"

        f_const.write(header_const)
        constprops = self.matv.constproperty_set.all().filter(software=software)
        order=[1,0,2,5,3,4,6] # OpenFOAM units order [Mass Length Time Temperature Quantity	Current Luminous]
        scalar_list=["nSolidPhases","Zx[","nPyroReac["]
        for i in constprops:
            dims_tmp = i.unit.dims()
            dims=dims_tmp.copy()
            for j, order_j in enumerate(order):
                dims[order_j] = dims_tmp[j]
            units_to_OF = "["
            for j, dims_j in enumerate(dims):
                end = " "
                if j == len(dims) - 1:
                    end = "]"
                units_to_OF = units_to_OF + str(int(dims_j)) + end
            name = i.name
            name = name.split(" ")[0] # remove the units in the name
            f_const.write("// " + name + ": " + i.description + "\n")
            scalar = False
            for j in scalar_list:
                if (name.find(j) >= 0):
                    scalar = True
            if scalar:
                f_const.write(name  + " " + str(i.value) + ";\n\n")
            else:
                f_const.write(name + " " + name + " " + units_to_OF + " " + str(i.value) + ";\n\n")
        matrixprops = self.matv.matrixproperty_set.all().filter(software=software)
        for i in matrixprops:
            dims_tmp = i.unit.dims()
            dims = dims_tmp.copy()
            for j, order_j in enumerate(order):
                dims[order_j] = dims_tmp[j]
            units_to_OF = "["
            for j, dims_j in enumerate(dims):
                end = " "
                if j == len(dims) - 1:
                    end = "]"
                units_to_OF = units_to_OF + str(int(dims_j)) + end
            name = i.name
            name = name.split(" ")[0]  # remove the units in the name
            f_const.write("// " + name + ": " + i.description + "\n")
            f_const.write(name + " " + name + " " + units_to_OF + " " + str(i.value) + ";\n\n")
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
        today = date.today().strftime("%Y-%m-%d")

        if ITAR:
            mat = ITARMaterial.objects.get(name=matName)
            print(mat, "in upload")
            matv,flag = ITARMaterialVersion.objects.get_or_create(material=mat, version=Pform['version'], published=today)
            print(matv, flag, "in upload")
        else:
            mat = Material.objects.get(name=matName)
            matv,flag = MaterialVersion.objects.get_or_create(material=mat, version=Pform['version'], published=today)
        
        units = ComboUnit.objects.all()
        none_unit = ComboUnit.objects.get(name='None')
        matv.save()

        soft = Software.objects.get(name="PATO")

        p = Pform['vparams']['Pressure(Pa)']
        T = Pform['vparams']['Temperature(K)']
        for key in Pform['vparams'].keys():
            if key not in ['Pressure(Pa)', 'Temperature(K)']:
                if ITAR:
                    vprop,fl = ITARVariableProperty.objects.get_or_create(material_version=matv, name=key, software=soft)
                else:
                    vprop,fl = VariableProperty.objects.get_or_create(material_version=matv, name=key, software=soft)
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
                    mx,flag = ITARMatrixProperty.objects.get_or_create(name=names[i],material_version=matv,state=state, software=soft)
                else:
                    mx,flag = MatrixProperty.objects.get_or_create(name=names[i],material_version=matv,state=state, software=soft)
                mx.unit = myunit
                mx.value=vals[i]
                mx.description = "matrix elements"
                mx.save()

            else:
                if ITAR:
                    const,flag = ITARConstProperty.objects.get_or_create(material_version = matv, state=state, name=names[i], software=soft)
                else:
                    const,flag = ConstProperty.objects.get_or_create(material_version = matv, state=state, name=names[i], software=soft)
                const.description=notes[i]
                const.value=float(vals[i])
                const.unit = myunit
                const.save()
        return matv

class FIAT_formatter(Formatter):

    # Write the FIAT material database file
    def export_file(self, matv, softv):
        self.matv = matv
        self.softv= softv
        self.mat_name = matv.material.name
        self.mat_version = matv.version
        self.code_name = softv.software.name
        self.code_version = softv.version

        # Folder name
        folder_base = settings.STATIC_ROOT + "/tmp"
        file_name = "matdatabase_" + self.code_name + "_" + self.mat_name + "_" + self.mat_version + ".txt"
        full_file_name = folder_base + "/" + file_name
        # Clean folders
        if os.path.exists(full_file_name):
            os.system("rm -f " + full_file_name)
        if not os.path.exists(folder_base):
            os.makedirs(folder_base)
        # Create the material database file
        f = open(full_file_name, "w")
        if self.matv.constproperty_set.all().filter(name="Type").count() == 0:
            return self.error_file("\"Type\" not found in ConstProperty")
        header = "FIAT Material Database File, last modified on " + str(self.matv.last_modified) + " at NASA Ames\n" \
                + "Material specification: sequence number, character name, version number, type\n" \
                + "Type: 0=subsurface, 1=reusable, 2=pyro only, 3=abl only, 4=pyro+abl\n" \
                + "1  number of materials to follow, format i4,2x,a16,2x,a5,2x,i1\n" \
                + "   {0:<3}{1:<19}{2:<6}{3:<5}".format(1,self.mat_name,self.mat_version,int(self.matv.constproperty_set.get(name="Type").value))+ self.matv.material.description + "\n\n" \
                + "{0:<19}{1:<6}{2:<5}".format(self.mat_name,self.mat_version,0)+ self.matv.material.description + "\n"
        f.write(header)
        software = Software.objects.get(name="FIAT")
        # Constant properties
        names = []
        constProps = self.matv.constproperty_set.all().filter(software=software)
        for i in constProps:
            names.append(i.name)

        text = ""
        data=[[["{:>8}"],"DH1"],[["{:>5}"],"DH2"],[["{:>5}"],"DH3"],[["{:.1f}","{:>7}"],"TDH"],[[],"\n"],
              [["{:>6}"],"GAMMA"],[["{:>5}"],"PHI"],[[],"\n"],
              [["{:.3f}","{:>7}"], "RVI_1"], [["{:.3f}","{:>8}"], "RCI_1"], [["{:.3E}","{:>11}"], "AI_1"],
              [["{:.1f}","{:>5}"], "PSII_1"], [["{:.1f}","{:>9}"], "EI_1"], [["{:.2f}","{:>10}"], "TRACI_1"],[[], "\n"],
              [["{:.3f}", "{:>7}"], "RVI_2"], [["{:.3f}", "{:>8}"], "RCI_2"], [["{:.3E}", "{:>11}"], "AI_2"],
              [["{:.1f}", "{:>5}"], "PSII_2"], [["{:.1f}", "{:>9}"], "EI_2"], [["{:.2f}", "{:>10}"], "TRACI_2"],[[], "\n"],
              [["{:.3f}", "{:>7}"], "RVI_3"], [["{:.3f}", "{:>8}"], "RCI_3"], [["{:.3E}", "{:>11}"], "AI_3"],
              [["{:.1f}", "{:>5}"], "PSII_3"], [["{:.1f}", "{:>9}"], "EI_3"], [["{:.2f}", "{:>10}"], "TRACI_3"],[[], "\n"]
              ]
        for i in data:
            if i[1] == "\n":
                text+=i[1]
            else:
                index = index_containing_substring(names,i[1])
                if index >= 0:
                    text += format_list(i[0], constProps.get(name=names[index]).value)
                else:
                    names = []
                    for i in self.matv.constproperty_set.all():
                        names.append(i.name)
                    if index_containing_substring(names,i[1]) >= 0:
                        return self.error_file("\""+i[1]+"\" found in ConstProperty but software FIAT not found.")
                    return self.error_file("\""+i[1]+"\" not found in ConstProperty")

        # Variable properties
        varprops=self.matv.variableproperty_set.all().filter(software=software)
        names=[]
        for i in varprops:
            names.append(i.name)
        var_names = ["cp","k_tt","emissivity","absorptivity","k_ip"]
        format_data = [["{:.1f}","{:>7}"],["{:.3f}","{:>7}"],["{:.3E}","{:>11}"],["{:.1f}", "{:>5}"],
                ["{:.1f}", "{:>5}"],["{:.3E}", "{:>11}"]]
        index_virgin = index_containing_substring(names, "cp_virgin")
        index_char = index_containing_substring(names, "cp_char")
        pressures = remove_same_in_list(varprops.get(name=names[index_virgin]).p)
        size_T_virgin = len(varprops.get(name=names[index_virgin]).T)
        size_T_char = len(varprops.get(name=names[index_char]).T)
        data = [ [ 0 for i in range(size_T_virgin+size_T_char)] for j in range(len(var_names)+1) ]
        if len(data) != len(format_data):
            return self.error_file("len(data) != len(format_data)")
        for j in range(0,len(data[0])):
            state = "_virgin"
            offset = 0
            if j >= size_T_virgin:
                state = "_char"
                offset = -size_T_virgin
            name = names[index_containing_substring(names, "cp"+state)]
            data[0][j] = varprops.get(name=name).T[j+offset]
            if j == size_T_virgin - 1 or j == size_T_virgin + size_T_char - 1:
                data[0][j] = - data[0][j]
            for i in range(0,len(var_names)):
                name = names[index_containing_substring(names, var_names[i]+state)]
                data[i+1][j] = varprops.get(name=name).values[j+offset]
        text += format_list(["{:<2}"],int(len(pressures)))
        for i in pressures:
            text += format_list(["{:>7}"],i)
        text += "\n"
        for j in range(0,len(data[0])):
            for i in range(0, len(data)):
                text += format_list(format_data[i], data[i][j])
            text += "\n"
        # Pyrolysis gas enthalpy
        h_g = varprops.get(name=names[index_containing_substring(names, "h_g")])
        pressures = remove_same_in_list(h_g.p)
        temperatures_list = []
        h_g_list = []
        for i in pressures:
            temperatures_list.append([])
            h_g_list.append([])
        for i, p_i in enumerate(h_g.p):
            temperatures_list[pressures.index(p_i)].append(h_g.T[i])
            h_g_list[pressures.index(p_i)].append(h_g.values[i])
        first_temperatures = remove_same_in_list(temperatures_list[0])
        option = 2
        for i in temperatures_list:
            if remove_same_in_list(i) != first_temperatures:
                option = 1
                break
        if option == 1:
            text += format_list(["{:>2}"],int(len(pressures)))
            for i in pressures:
                text += format_list(["{:>7}"],i)
            text += "\n"
            for i,temperatures_list_i in enumerate(temperatures_list):
                for j, temperatures_list_i_j in enumerate(temperatures_list_i):
                    T = temperatures_list_i_j
                    if j == len(temperatures_list_i) - 1:
                        T = -T
                    text += format_list(["{:.2f}","{:>8}"],T) + format_list(["{:.2f}","{:>10}"],h_g_list[i][j]) + "\n"
        if option == 2:
            text += format_list(["{:>2}"],-int(len(pressures)))
            for i in pressures:
                text += format_list(["{:>7}"],i)
            text += "\n"
            for j, first_temperatures_j in enumerate(first_temperatures):
                T = first_temperatures_j
                if j == len(first_temperatures) - 1:
                    T = -T
                text += format_list(["{:.2f}","{:>8}"], T)
                for i, temperatures_list_i in enumerate(temperatures_list):
                    text += format_list(["{:.2f}", "{:>10}"], h_g_list[i][j])
                text += "\n"
        f.write(text)
        f.close()
        os.chdir(self.cwd)
        return full_file_name

    def parse_file(self, fpath_or_buffer):
        """Parses FIAT material csv format

        Args:
            fpath_or_buffer (filepath): path to csv file
        """
        _df = pd.read_csv(fpath_or_buffer, encoding='unicode_escape')
        df = _df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        d = df.values

        material,version,date,form = d[0,0:4]

        # Parse variable params table
        headers = d[3].astype('str')
        split_col_index_1 = np.where(headers == 'nan')[0][0]
        nrows = np.where(d[4:,0].astype('str') == 'nan')[0][0]
        vparams={}
        for i in range(0,split_col_index_1):
            vparams[headers[i]] = d[4:4+nrows,i].astype('float')

        split_col_index_2 = split_col_index_1 + np.where(headers[split_col_index_1+1:] == 'nan')[0][0] + 1
        nrows = np.where(d[4:,split_col_index_1+1].astype('str') == 'nan')[0][0]
        vparams_h={}
        for i in range(split_col_index_1+1,split_col_index_2):
            vparams_h[headers[i]] = d[4:4+nrows,i].astype('float')

        # Parse const params table
        nrows = np.where(d[3:,split_col_index_2+1].astype('str') == 'nan')[0][0]
        const_names = d[3:3+nrows,split_col_index_2+1].astype('str')
        const_vals = d[3:3+nrows,split_col_index_2+2].astype('str')
        const_notes= d[3:3+nrows,split_col_index_2+3].astype('str')

        FIAT_fmt = {'material':material, 'version': version, 'date':date,'vparams':vparams,'vparams_h':vparams_h,
                    'const_names':const_names, "const_vals":const_vals,"const_notes":const_notes}

        return FIAT_fmt

    def upload_file(self, fpath_or_buffer, ITAR=False):
        Pform = self.parse_file(fpath_or_buffer)
        matName = Pform['material']
        today = date.today().strftime("%Y-%m-%d")

        if ITAR:
            mat = ITARMaterial.objects.get(name=matName)
            matv,flag = ITARMaterialVersion.objects.get_or_create(material=mat, version=Pform['version'], published=today)
        else:
            mat = Material.objects.get(name=matName)
            matv,flag = MaterialVersion.objects.get_or_create(material=mat, version=Pform['version'], published=today)

        units = ComboUnit.objects.all()
        none_unit = ComboUnit.objects.get(name='None')
        matv.save()

        soft = Software.objects.get(name="FIAT")
        p = Pform['vparams']['Pressure(atm)']
        T = Pform['vparams']['Temperature(R)']
        for key in Pform['vparams'].keys():
            if key not in ['Pressure(atm)', 'Temperature(R)']:
                if ITAR:
                    vprop,fl = ITARVariableProperty.objects.get_or_create(material_version=matv, name=key, software=soft)
                else:
                    vprop,fl = VariableProperty.objects.get_or_create(material_version=matv, name=key, software=soft)
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

        p = Pform['vparams_h']['Pressure(atm)']
        T = Pform['vparams_h']['Temperature(R)']
        for key in Pform['vparams_h'].keys():
            if key not in ['Pressure(atm)', 'Temperature(R)']:
                if ITAR:
                    vprop, fl = ITARVariableProperty.objects.get_or_create(material_version=matv, name=key, software=soft)
                else:
                    vprop, fl = VariableProperty.objects.get_or_create(material_version=matv, name=key, software=soft)
                vprop.p = p
                vprop.T = T
                vprop.values = Pform['vparams_h'][key]
                vprop.state = 2

                # extract units
                vprop.unit = none_unit
                ustrings = re.findall('\(.*?\)', key)
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
            ustrings = re.findall('\((?s:.*)\)',names[i])
            if len(ustrings) == 1 and ustrings[0] != '(-)':
                for unit in units:
                    l = re.split("\r\n", unit.alternate_names)
                    if ustrings[0][1:-1] in l:
                        myunit = unit
            else:
                myunit = none_unit
            if vals[i][0] == '(':
                if ITAR:
                    mx,flag = ITARMatrixProperty.objects.get_or_create(name=names[i],material_version=matv,state=state, software=soft)
                else:
                    mx,flag = MatrixProperty.objects.get_or_create(name=names[i],material_version=matv,state=state, software=soft)
                mx.unit = myunit
                mx.value=vals[i]
                mx.description = "matrix elements"
                mx.save()

            else:
                if ITAR:
                    const,flag = ITARConstProperty.objects.get_or_create(material_version = matv, state=state, name=names[i], software=soft)
                else:
                    const,flag = ConstProperty.objects.get_or_create(material_version = matv, state=state, name=names[i], software=soft)
                const.description=notes[i]
                const.value=float(vals[i])
                const.unit = myunit
                const.save()
        return matv

                
class ICARUS_formatter(Formatter):
    pass