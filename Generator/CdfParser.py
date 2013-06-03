import re

def parse_cdf_file(cdf_file):
    
    f = open(cdf_file, 'r')
    
    properties = {}
    prop = None
    value = ''
    for line in f:
        if not prop and line.startswith('Title'):
            prop = 'Title'
        elif not prop and line.startswith('Description'):
            prop = 'Description'
        elif not prop and line.startswith('Quote'):
            prop='Quote'
        elif prop and line.strip() == '':
            properties[prop] = value
            prop = None
            value = ''
        elif prop:
            value += line
            value = value.replace('\n', ' ')
            value = value.replace('  ', ' ')
            val_parts = re.split('([.!?] *)', value)
            value = ''.join([each.capitalize() for each in val_parts])
            value = value.replace(' i ', ' I ')
        else:
            raise Exception('Malformed cdf file (' + cdf_file + ')')
    if prop:
        properties[prop] = value
    
    if not 'Title' in properties:
        raise Exception('A Title is required! (' + cdf_file + ')')
    
    if not 'Description' in properties:
        raise Exception('A Description is required! (' + cdf_file + ')')
    
    return properties