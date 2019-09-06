import re

def return_plain(marker, sep=''):
    vals_pattern = re.compile(r"\^[A-Z][\w\-\']*\^")
    values = re.split(vals_pattern, marker)
    new_value = [x for x in values if x]
    return sep.join(new_value)