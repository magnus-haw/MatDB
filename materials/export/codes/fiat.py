from .base import *
import sys

def index_containing_substring(list, substring):
    for i, s in enumerate(list):
        if substring in s:
              return i
    return -1

def format_list(list, elem):
    new_elem = elem
    for i in list:
        new_elem = i.format(new_elem)
    return new_elem

def remove_same_in_list(list):
    diff = []
    for i in list:
        if i not in diff:
            diff.append(i)
    return diff



class fiat_export_model(base_export_model):

    def error_file(self, string):
        folder_base = settings.STATIC_ROOT + "/tmp"
        file_name = folder_base + "/error.txt"
        f = open(file_name, "w")
        msg = "Error for the \""+ self.code_name + "\" export of the material \"" + self.mat_name + "\" version \"" + self.mat_version + "\"\n"
        f.write(msg+string)
        f.close()
        return file_name

    def create_file(self):
        # Get current folder
        mycwd = os.getcwd()
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
        # Constant properties
        names = []
        for i in self.matv.constproperty_set.all():
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
                    text += format_list(i[0],self.matv.constproperty_set.get(name=names[index]).value)
                else:
                    text += str(i[0].format("{" + i[1] + "}"))
        # Variable properties
        varprops=self.matv.variableproperty_set
        names=[]
        for i in varprops.all():
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
        os.chdir(mycwd)
        return full_file_name



