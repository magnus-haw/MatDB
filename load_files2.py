#from django.shortcuts import render
import pandas as pd
import numpy as np
import re
from io import StringIO

### Loading files into database.

def parse_PATO_material_csv(fpath_or_buffer):
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

def upload_PATO_fmt(matName, Pform, ITAR=False):
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

    folder = "materials/"
    fname1 = folder + "Cork_v1.csv"
    fname2 = folder + "TACOT_v3.csv"

    # Load Cork file
    Pform1 = parse_PATO_material_csv(fname1)
    upload_PATO_fmt('Cork', Pform1)

    # Load TACOT file
    Pform2 = parse_PATO_material_csv(fname2)
    upload_PATO_fmt('TACOT', Pform2)
    
    # Load TACOT file into HEEET
    Pform2 = parse_PATO_material_csv(fname2)
    upload_PATO_fmt('HEEET', Pform2, ITAR=True)