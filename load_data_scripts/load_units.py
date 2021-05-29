import os
import re
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MatDB.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from units.models import BaseUnit, ComboUnit, BaseUnitPower

inputs_BaseUnit=[
	{"name":"Ampere","symbol":"A","coeff":1.0,"temp_offset":0.0,"dims":[0, 0, 0, 1, 0, 0, 0]},
	{"name":"British thermal unit","symbol":"BTU","coeff":1055.0,"temp_offset":0.0,"dims":[2, 1, -2, 0, 0, 0, 0]},
	{"name":"Candela","symbol":"cd","coeff":1.0,"temp_offset":0.0,"dims":[0, 0, 0, 0, 0, 0, 1]},
	{"name":"Celcius","symbol":"degC","coeff":1.0,"temp_offset":273.15,"dims":[0, 0, 0, 0, 1, 0, 0]},
	{"name":"Fahrenheit","symbol":"degF","coeff":0.55555555555,"temp_offset":255.37,"dims":[0, 0, 0, 0, 1, 0, 0]},
	{"name":"Foot","symbol":"ft","coeff":0.3048,"temp_offset":0.0,"dims":[1, 0, 0, 0, 0, 0, 0]},
	{"name":"Inch","symbol":"in","coeff":0.0254,"temp_offset":0.0,"dims":[1, 0, 0, 0, 0, 0, 0]},
	{"name":"Joule","symbol":"J","coeff":1.0,"temp_offset":0.0,"dims":[2, 1, -2, 0, 0, 0, 0]},
	{"name":"Kelvin","symbol":"K","coeff":1.0,"temp_offset":0.0,"dims":[0, 0, 0, 0, 1, 0, 0]},
	{"name":"Kilogram","symbol":"kg","coeff":1.0,"temp_offset":0.0,"dims":[0, 1, 0, 0, 0, 0, 0]},
	{"name":"Meter","symbol":"m","coeff":1.0,"temp_offset":0.0,"dims":[1, 0, 0, 0, 0, 0, 0]},
	{"name":"Mole","symbol":"mole","coeff":1.0,"temp_offset":0.0,"dims":[0, 0, 0, 0, 0, 1, 0]},
	{"name":"Newton","symbol":"N","coeff":1.0,"temp_offset":0.0,"dims":[1, 1, -2, 0, 0, 0, 0]},
	{"name":"None","symbol":"-","coeff":1.0,"temp_offset":0.0,"dims":[0, 0, 0, 0, 0, 0, 0]},
	{"name":"Pascal","symbol":"Pa","coeff":1.0,"temp_offset":0.0,"dims":[-1, 1, -2, 0, 0, 0, 0]},
	{"name":"Pound-force","symbol":"lbf","coeff":4.448222,"temp_offset":0.0,"dims":[1, 1, -2, 0, 0, 0, 0]},
	{"name":"Pound-mass","symbol":"lb","coeff":0.45359237,"temp_offset":0.0,"dims":[0, 1, 0, 0, 0, 0, 0]},
	{"name":"Second","symbol":"s","coeff":1.0,"temp_offset":0.0,"dims":[0, 0, 1, 0, 0, 0, 0]},
    {"name":"Rankine","symbol":"R","coeff":0.555556,"temp_offset":0.0,"dims":[0, 0, 0, 0, 1, 0, 0]}
]

def dims_to_BaseUnit(dims):
    units_model = ["length_dim", "mass_dim", "time_dim",
                    "current_dim", "temp_dim", "mole_dim", "luminous_dim"]
    dict = {}
    for i, dims_i in enumerate(dims):
        dict[units_model[i]]=dims_i
    return dict

for i in inputs_BaseUnit:
    i.update(dims_to_BaseUnit(i["dims"]))
    del i["dims"]

names_ComboUnit = ["1/s","J/(kg K)","J/kg","K","None","W/(m K)","W/m2",
                   "kg.m2/(s2.mole)","kg/m3","kg/s","m2/s2","m2",
                   "BTU/(lb.R)","BTU/(ft s R)","BTU/lb","lb/ft3"]
alternate_names_ComboUnit = ["s-1\r\ns^-1","J/kg/K\r\nJ/Kkg\r\nJ/kgK\r\nJ/kg-K\r\nJ/K-kg",
                             "Jkg^-1\r\nJoules per kilogram\r\nJ kg^-1","Kelvin",
                             "No","W/m/K","W/m^2\r\nWatts per m^2\r\nWm^-2",
                             "kgm2/(s2mole)\r\nkg.m^2/(s^2.mole)\r\nkg.m2.s-2.mole-1",
                             "kg/m^3\r\nkg.m^-3\r\nkg m^-3\r\nkilogram per m^3","kg.s-1\r\nkg.s^-1",
                             "m2s-2\r\nm^2s^-2\r\nm^2/s^2","square meters\r\nm^2",
                             "BTU/(lb R)\r\nBTU/lb/R\r\nBTU lb-1 R-1\r\nBTU lb^-1 R^-1\r\nBTU.lb^-1.R^-1",
                             "BTU/(ft.s.R)\r\nBTU ft-1 s-1 R-1\r\nBTU ft^-1 s^-1 R^-1",
                             "BTU lb-1\r\nBTU lb^-1\r\nBTU.lb^-1",
                             "lb.ft-3\r\nlb fr-3\r\nlb.ft^-3\r\nlb ft^-3"]

for i,names_i in enumerate(names_ComboUnit):
    alternate_names_ComboUnit[i] += "\r\n" + names_i
dim_symbols=[]
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
    print ("Delete all the BaseUnit, BaseUnitPower, and ComboUnit.")
    BaseUnit.objects.all().delete()
    BaseUnitPower.objects.all().delete()
    ComboUnit.objects.all().delete()

if "update" in sys.argv:
    # Create/update the BaseUnit
    for i in inputs_BaseUnit:
        base_unit,flag = BaseUnit.objects.get_or_create(**i)
        base_unit.save()

    # Create/update the dim symbols
    for obj in BaseUnit.objects.all():
        dim_symbols.append(obj.symbol)

    # Create/update the BaseUnitPower and ComboUnit
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
    print("BaseUnit = " + str(BaseUnit.objects.count()))

if "print" in sys.argv:
    if "BaseUnit" in sys.argv or "all" in sys.argv:
        print("==========================")
        print("BaseUnit = " + str(BaseUnit.objects.count()))
        for obj in BaseUnit.objects.all():
            print("\t"+str(obj.id))
            print("\t"+str(obj.name))
            print("\t"+str(obj.symbol))
            print("\t"+str(obj.coeff))
            print("\t"+str(obj.temp_offset))
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
