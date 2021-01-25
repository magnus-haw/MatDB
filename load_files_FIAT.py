#from django.shortcuts import render
import pandas as pd
import numpy as np
import re
import sys
from io import StringIO

### Loading files into database.

def parse_FIAT_material_csv(fpath_or_buffer):
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


def upload_FIAT_fmt(matName, Pform, ITAR=False):
    if ITAR:
        mat = ITARMaterial.objects.get(name=matName)
        matv,flag = ITARMaterialVersion.objects.get_or_create(material=mat, version=Pform['version'])
    else:
        mat = Material.objects.get(name=matName)
        matv,flag = MaterialVersion.objects.get_or_create(material=mat, version=Pform['version'])

    units = ComboUnit.objects.all()
    none_unit = ComboUnit.objects.get(name='None')
    matv.save()

    p = Pform['vparams']['Pressure(atm)']
    T = Pform['vparams']['Temperature(R)']
    for key in Pform['vparams'].keys():
        if key not in ['Pressure(atm)', 'Temperature(R)']:
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

    p = Pform['vparams_h']['Pressure(atm)']
    T = Pform['vparams_h']['Temperature(R)']
    for key in Pform['vparams_h'].keys():
        if key not in ['Pressure(atm)', 'Temperature(R)']:
            if ITAR:
                vprop, fl = ITARVariableProperty.objects.get_or_create(material_version=matv, name=key)
            else:
                vprop, fl = VariableProperty.objects.get_or_create(material_version=matv, name=key)
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

if __name__=="__main__":
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MatDB.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    from materials.models import MaterialVersion, Material, ConstProperty, MatrixProperty, VariableProperty
    from itarmaterials.models import ITARMaterial, ITARMaterialVersion, ITARConstProperty, ITARMatrixProperty, ITARVariableProperty
    from units.models import ComboUnit
    from datetime import date

    folder = "materials/FIAT_database/"
    fname1 = folder + "TACOT_v3.0.2.csv"

    # Load TACOT file
    Pform1 = parse_FIAT_material_csv(fname1)

    if "delete" in sys.argv:
        mat = Material.objects.get(name='TACOT')
        matv = MaterialVersion.objects.get(material=mat, version=Pform1['version'])
        matv.variableproperty_set.all().delete()
        matv.matrixproperty_set.all().delete()
        matv.constproperty_set.all().delete()

    if "update" in sys.argv:
        upload_FIAT_fmt('TACOT', Pform1)

    if "print" in sys.argv:
        print("ConstProperty.objects.count()=",end="")
        print(ConstProperty.objects.count())
        print("MatrixProperty.objects.count()=",end="")
        print(MatrixProperty.objects.count())
        print("VariableProperty.objects.count()=",end="")
        print(VariableProperty.objects.count())
        print("ITARConstProperty.objects.count()=", end="")
        print(ITARConstProperty.objects.count())
        print("ITARMatrixProperty.objects.count()=", end="")
        print(ITARMatrixProperty.objects.count())
        print("ITARVariableProperty.objects.count()=", end="")
        print(ITARVariableProperty.objects.count())
