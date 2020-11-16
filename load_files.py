#from django.shortcuts import render
import pandas as pd
import numpy as np
from io import StringIO

### Loading files into database.

def parse_PATO_material_csv(fpath_or_buffer):
    """Parses PATO material csv format

    Args:
        fpath_or_buffer (filepath): path to csv file
    """
    df = pd.read_csv(fpath_or_buffer, encoding='unicode_escape')
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

if __name__=="__main__":
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MatDB.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    from materials.models import MaterialVersion, Material, ConstProperty, VariableProperties, MatrixProperty
    from datetime import date
    dt = date.fromisoformat('2020-01-01')

    folder = "materials/"
    fname1 = folder + "Cork_v1.csv"
    fname2 = folder + "TACOT_v3.csv"

    # Pform = parse_PATO_material_csv(fname1)
    # mat = Material.objects.get(name="Cork")
    # matv,flag = MaterialVersion.objects.get_or_create(material=mat, version=Pform['version'],rating=1,notes='',date=dt)
    # matv.save()

    # vprops,fl = VariableProperties.objects.get_or_create(material=matv,state=0)
    # vprops.p = Pform['vparams']['Pressure(Pa)']
    # vprops.T = Pform['vparams']['Temperature(K)']
    # vprops.cp = Pform['vparams']['cp_virgin(J/kg/K)']
    # vprops.h = Pform['vparams']['h_virgin(J/kg)']
    # vprops.ki = Pform['vparams']['ki_virgin(W/m/K)']
    # vprops.kj = Pform['vparams']['kj_virgin(W/m/K)']
    # vprops.kk = Pform['vparams']['kk_virgin(W/m/K)']
    # vprops.emissivity = Pform['vparams']['emissivity_virgin(-)']
    # vprops.absorptivity = Pform['vparams']['absorptivity_virgin(-)']
    # vprops.save()

    # vprops,fg = VariableProperties.objects.get_or_create(material=matv,state=1)
    # vprops.p = Pform['vparams']['Pressure(Pa)']
    # vprops.T = Pform['vparams']['Temperature(K)']
    # vprops.cp = Pform['vparams']['cp_char(J/kg/K)']
    # vprops.h = Pform['vparams']['h_char(J/kg)']
    # vprops.ki = Pform['vparams']['ki_char(W/m/K)']
    # vprops.kj = Pform['vparams']['kj_char(W/m/K)']
    # vprops.kk = Pform['vparams']['kk_char(W/m/K)']
    # vprops.emissivity = Pform['vparams']['emissivity_char(-)']
    # vprops.absorptivity = Pform['vparams']['absorptivity_char(-)']
    # vprops.save()
    
    # names, vals, notes = Pform['const_names'],Pform['const_vals'],Pform['const_notes']
    # for i in range(0,len(names)):
    #     state =0
    #     if "char" in notes[i]:
    #         state = 1
    #     elif "pyrolysis" in notes[i]:
    #         state = 2

    #     if vals[i][0] == '(':
    #         mx,flag = MatrixProperty.objects.get_or_create(name=names[i],value=vals[i],material=matv,state=state,description="")
    #         mx.save()

    #     else:
    #         const,flag = ConstProperty.objects.get_or_create(material = matv, state=state, name=names[i], 
    #                                                     value=float(vals[i]),description=notes[i])
    #         const.save()
    
    ### Load TACOT
    Pform = parse_PATO_material_csv(fname2)
    mat = Material.objects.get(name="TACOT")
    
    matv,flag = MaterialVersion.objects.get_or_create(material=mat, version=Pform['version'],rating=1,notes='',date=dt)
    matv.save()

    vprops,fl = VariableProperties.objects.get_or_create(material=matv,state=0)
    vprops.p = Pform['vparams']['Pressure(Pa)']
    vprops.T = Pform['vparams']['Temperature(K)']
    vprops.cp = Pform['vparams']['cp_virgin(J/kg/K)']
    vprops.h = Pform['vparams']['h_virgin(J/kg)']
    vprops.ki = Pform['vparams']['ki_virgin(W/m/K)']
    vprops.kj = Pform['vparams']['kj_virgin(W/m/K)']
    vprops.kk = Pform['vparams']['kk_virgin(W/m/K)']
    vprops.emissivity = Pform['vparams']['emissivity_virgin(-)']
    vprops.absorptivity = Pform['vparams']['absorptivity_virgin(-)']
    vprops.save()

    vprops,fg = VariableProperties.objects.get_or_create(material=matv,state=1)
    vprops.p = Pform['vparams']['Pressure(Pa)']
    vprops.T = Pform['vparams']['Temperature(K)']
    vprops.cp = Pform['vparams']['cp_char(J/kg/K)']
    vprops.h = Pform['vparams']['h_char(J/kg)']
    vprops.ki = Pform['vparams']['ki_char(W/m/K)']
    vprops.kj = Pform['vparams']['kj_char(W/m/K)']
    vprops.kk = Pform['vparams']['kk_char(W/m/K)']
    vprops.emissivity = Pform['vparams']['emissivity_char(-)']
    vprops.absorptivity = Pform['vparams']['absorptivity_char(-)']
    vprops.save()
    
    names, vals, notes = Pform['const_names'],Pform['const_vals'],Pform['const_notes']
    for i in range(0,len(names)):
        state =0
        if "char" in notes[i]:
            state = 1
        elif "pyrolysis" in notes[i]:
            state = 2

        if vals[i][0] == '(':
            mx,flag = MatrixProperty.objects.get_or_create(name=names[i],value=vals[i],material=matv,state=state,description="")
            mx.save()

        else:
            const,flag = ConstProperty.objects.get_or_create(material = matv, state=state, name=names[i], 
                                                        value=float(vals[i]),description=notes[i])
            const.save()

