import os
import re
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MatDB.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from units.models import BaseUnit, ComboUnit, BaseUnitPower

names_ComboUnit = ["1/s","J/(kg K)","J/kg","K","None","W/(m K)","W/m2",
                   "kg.m2/(s2.mole)","kg/m3","kg/s","m2/s2","m2"]
alternate_names_ComboUnit = ["s-1\r\ns^-1","J/kg/K\r\nJ/Kkg\r\nJ/kgK\r\nJ/kg-K\r\nJ/K-kg",
                             "Jkg^-1\r\nJoules per kilogram\r\nJ kg^-1","Kelvin",
                             "No","W/m/K","W/m^2\r\nWatts per m^2\r\nWm^-2",
                             "kgm2/(s2mole)\r\nkg.m^2/(s^2.mole)\r\nkg.m2.s-2.mole-1",
                             "kg/m^3\r\nkg.m^-3\r\nkg m^-3\r\nkilogram per m^3","kg.s-1\r\nkg.s^-1",
                             "m2s-2\r\nm^2s^-2\r\nm^2/s^2","square meters\r\nm^2"]
for i,names_i in enumerate(names_ComboUnit):
    alternate_names_ComboUnit[i] += "\r\n" + names_i
dim_symbols = ["kg","m","s","K","mole","A","cd","J"]
replace_symbols = {"W":"J.s^-1"}

def units_string_to_power(units_string):
    values = [0 for i in range(len(dim_symbols))]
    if units_string == "None" or units_string == None:
        return values
    for i in replace_symbols.keys():
        if i in units_string:
            units_string=units_string.replace(i,replace_symbols[i])
    var = re.split("[/]", units_string)
    if len(var)>2:
        error_msg = "Error in units_to_OF: Problem with the units \"" + units_string + "\". len(["
        for i, var_i in enumerate(var):
            end = ","
            if i == len(var)-1:
                end="])>2"
            error_msg = error_msg + "\"" + var_i + "\"" + end
        sys.exit(error_msg)
    for i, var_i in enumerate(var):
        list_tmp = [k for k in re.split("[.()]", var[i]) if k]
        list_var = []
        for j, list_tmp_j in enumerate(list_tmp):
            list_var.extend([k for k in re.split(" ", list_tmp_j) if k])
        for j, list_j in enumerate(list_var):
            v = 1
            if bool(re.search(r'\d', list_j)):
                v = float(re.findall(r'-?\d+', list_j)[0]) # assume there is only one number
            if i == 1: # denominator
                v = -v
            v = int(v)
            unit = ''.join([k for k in list_j if not k.isdigit()])
            unit = unit.replace("^","")
            unit = unit.replace("-", "")
            if unit != "":
                if unit not in dim_symbols:
                    error_msg = "Error in units_to_OF: \""+ unit +"\" not found in the OpenFOAM units ("
                    for k, dim_symbols_k in enumerate(dim_symbols):
                        end = ","
                        if k == len(dim_symbols)-1:
                            end = ")"
                        error_msg = error_msg + dim_symbols_k + end
                    sys.exit(error_msg)
                values[dim_symbols.index(unit)]=v
    return values

if "delete" in sys.argv:
    BaseUnitPower.objects.all().delete()
    ComboUnit.objects.all().delete()

if "update" in sys.argv:
    for i,names_ComboUnit_i in enumerate(names_ComboUnit):
        name = names_ComboUnit_i
        alternate_names = alternate_names_ComboUnit[i]
        combo_unit, flag = ComboUnit.objects.get_or_create(name=name,symbol=name,alternate_names=alternate_names)
        dims = units_string_to_power(name)
        for j,dims_j in enumerate(dims):
            if dims_j != 0:
                base_unit = BaseUnit.objects.get(symbol=dim_symbols[j])
                base_unit_power, flag = BaseUnitPower.objects.get_or_create(combo=combo_unit, unit=base_unit, power=dims_j)

    print("Updated")
    print("ComboUnit = " + str(ComboUnit.objects.count()))
    print("BaseUnitPower = " + str(BaseUnitPower.objects.count()))

if "print" in sys.argv:

    if "BaseUnit" in sys.argv or "all" in sys.argv:
        print("==========================")
        print("BaseUnit = " + str(BaseUnit.objects.count()))
        for obj in BaseUnit.objects.all():
            print("\t"+str(obj.id))
            print("\t"+str(obj.name))
            print("\t" + str(obj.dims()))
            print("\t------")
        print("==========================")
    if "ComboUnit" in sys.argv or "all" in sys.argv:
        print("ComboUnit = " + str(ComboUnit.objects.count()))
        for obj in ComboUnit.objects.all():
            print("\t"+str(obj.id))
            print("\t"+str(obj.name))
            print("\t"+str(obj.symbol))
            print("\t"+str(repr(obj.alternate_names)))
            print("\t" + str(obj.dims()))
            print("\t------")
        print("==========================")
    if "BaseUnitPower" in sys.argv or "all" in sys.argv:
        print("BaseUnitPower = " + str(BaseUnitPower.objects.count()))
        for obj in BaseUnitPower.objects.all():
            print("\t"+str(obj.id))
            print("\t"+str(obj.combo.name))
            print("\t"+str(obj.unit.name))
            print("\t"+str(obj.power))
            print("\t------")
