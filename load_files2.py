#from django.shortcuts import render
import pandas as pd
import numpy as np
import sys
import pathlib

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
        mat,created = ITARMaterial.objects.get_or_create(name=matName)
        matv,flag = ITARMaterialVersion.objects.get_or_create(material=mat, version=Pform['version'])
    else:
        mat,created = Material.objects.get_or_create(name=matName)
        matv,flag = MaterialVersion.objects.get_or_create(material=mat, version=Pform['version'])
    
    mat.save()
    matv.save()
    
    p = Pform['vparams']['Pressure(Pa)']
    T = Pform['vparams']['Temperature(K)']
    for key in Pform['vparams'].keys():
        if key not in ['Pressure(Pa)', 'Temperature(K)']:
            label, unit = parse_quantity_header(key)
            print(label,unit)
            print(type(matv))

            if ITAR:
                mp, created_mp = ITARMaterialProperty.objects.get_or_create(name=label,unit=unit,description=label)
                mpi, created_mpi = ITARMaterialPropertyInstance.objects.get_or_create(material_version=matv, property=mp)
                vprop,fl = ITARVariableProperty.objects.get_or_create(property_instance=mpi)
            else:
                mp, created_mp = MaterialProperty.objects.get_or_create(name=label,unit=unit,description=label)
                mpi, created_mpi = MaterialPropertyInstance.objects.get_or_create(material_version=matv, property=mp)
                vprop,fl = VariableProperty.objects.get_or_create(property_instance=mpi)
            vprop.p = p
            vprop.T = T
            vprop.values = Pform['vparams'][key]
            if 'virgin' in key:
                mpi.state = 0
            elif 'char' in key:
                mpi.state = 1
            else:
                mpi.state = 2
                print(key)
    
    names, vals, notes = Pform['const_names'],Pform['const_vals'],Pform['const_notes']
    for i in range(0,len(names)):
        state =0
        if "char" in notes[i]:
            state = 1
        elif "pyrolysis" in notes[i]:
            state = 2

        # extract units
        label, myunit = parse_quantity_header(key)

        # add matrix unit
        if vals[i][0] == '(':
            if ITAR:
                mp, created_mp = ITARMaterialProperty.objects.get_or_create(name=label,unit=myunit,description=label)
                mpi, created_mpi = ITARMaterialPropertyInstance.objects.get_or_create(material_version=matv, property=mp)
                mx,flag = ITARMatrixProperty.objects.get_or_create()
            else:
                mp, created_mp = MaterialProperty.objects.get_or_create(name=label,unit=myunit,description=label)
                mpi, created_mpi = MaterialPropertyInstance.objects.get_or_create(material_version=matv, property=mp)
                mx,flag = MatrixProperty.objects.get_or_create()
            mx.value=vals[i]
            mx.save()

        # add const unit
        else:
            if ITAR:
                mp, created_mp = ITARMaterialProperty.objects.get_or_create(name=label,unit=myunit,description=label)
                mpi, created_mpi = ITARMaterialPropertyInstance.objects.get_or_create(material_version=matv, property=mp)
                const,flag = ITARConstProperty.objects.get_or_create()
            else:
                mp, created_mp = MaterialProperty.objects.get_or_create(name=label,unit=myunit,description=label)
                mpi, created_mpi = MaterialPropertyInstance.objects.get_or_create(material_version=matv, property=mp)
                const,flag = ConstProperty.objects.get_or_create()

            const.value=float(vals[i])
            const.save()

if __name__=="__main__":
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MatDB.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    from materials.models import MaterialVersion, Material, ConstProperty, MatrixProperty
    from materials.models import MaterialProperty, VariableProperty, MaterialPropertyInstance
    from itarmaterials.models import ITARMaterial, ITARMaterialVersion, ITARConstProperty, ITARMatrixProperty
    from itarmaterials.models import ITARMaterialPropertyInstance, ITARMaterialProperty, ITARVariableProperty
    from units.models import ComboUnit
    from units.utils import parse_quantity_header
    from datetime import date

    if "delete" in sys.argv:
        ConstProperty.objects.all().delete()
        MatrixProperty.objects.all().delete()
        VariableProperty.objects.all().delete()
        ITARConstProperty.objects.all().delete()
        ITARMatrixProperty.objects.all().delete()
        ITARVariableProperty.objects.all().delete()

    if "update" in sys.argv:
        folder = pathlib.Path(__file__).parent.absolute()
        fname1 = folder / "load_data_scripts" / "Cork_v1.csv"
        fname2 = folder / "load_data_scripts" / "TACOT_v3.0.0.csv"
        fname3 = folder / "load_data_scripts" / "HEEET_v4.0.1.csv"

        # Load Cork file
        Pform1 = parse_PATO_material_csv(fname1)
        upload_PATO_fmt('Cork', Pform1)

        # Load TACOT file
        Pform2 = parse_PATO_material_csv(fname2)
        upload_PATO_fmt('TACOT', Pform2)

        # Load TACOT file
        Pform3 = parse_PATO_material_csv(fname3)
        upload_PATO_fmt('HEEET', Pform3, ITAR=True)

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
