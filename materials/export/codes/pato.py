from .base import *

# PATO export class
class pato_export_model(base_export_model):

    # Write the char, virgin and constantProperties files
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
                if len(data_p_char)>0 and not self.check_arrays(data_p_char,var.p):
                    sys.exit("Error: pressure is different between variables.")
                data_p_char = var.p
                if len(data_T_char)>0 and not self.check_arrays(data_T_char,var.T):
                    sys.exit("Error: temperature is different between variables.")
                data_T_char = var.T
                data_char.append(var.values)
            if var.state == 0: # virgin
                if len(data_p_virgin)>0 and not self.check_arrays(data_p_virgin,var.p):
                    sys.exit("Error: pressure is different between variables.")
                data_p_virgin = var.p
                if len(data_T_virgin)>0 and not self.check_arrays(data_T_virgin,var.T):
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
        constprops = self.matv.constproperty_set.all()
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
        matrixprops = self.matv.matrixproperty_set.all()
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
        os.chdir(mycwd)
        return full_folder_name+".zip"