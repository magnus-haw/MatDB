### Utilities functions for units

import re
from .models import ComboUnit

def get_label_and_unit(str_input, brackets='()'):
    if brackets == '()':
        symbol_regex= '(?<=\().+?(?=\))'
    elif brackets == '[]':
        symbol_regex= '(?<=\[).+?(?=\])'
    ustrings = re.findall(symbol_regex,str_input)
    label = str_input.split(brackets[0])[0].strip()
    
    if len(ustrings) == 1:
        unitsymbol =  ustrings[0]
    else:
        unitsymbol =  '-'

    return label, unitsymbol

def parse_quantity_header(str_input, brackets='()'):
    # extract units
    none_unit, created = ComboUnit.objects.get_or_create(name='None', symbol='-')
    
    label,symbol = get_label_and_unit(str_input, brackets=brackets)
    query = ComboUnit.objects.filter(symbol= symbol) | ComboUnit.objects.filter(alternateunitsymbol__symbol = symbol)
    if query.count() == 1:
        return label, query[0]

    return label, none_unit