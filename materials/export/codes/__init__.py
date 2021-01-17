from os.path import dirname, basename, isfile, join
import glob
from django.shortcuts import render,get_object_or_404
# from ...models import Material, MaterialVersion, VariableProperties

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not (f.endswith('__init__.py') or f.endswith('base.py'))]
export_models= __all__

# class AbstractExportModel():
#     def __init__(self, matv):
#         self.matv = matv
#
#     def read(self):
#         pass

# from .pato import *
# from . import fiat