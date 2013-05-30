import re
def parse_cdf_file(cdf_file):
    
    f = open(cdf_file, 'r')
    
    describing = False
    description = None
    quoting = False
    quote = None
    for line in f:
        if line.startswith('Title'):
            title = line.split(' - ')[1].strip()
        elif line.startswith('Description'):
            describing = True
            quoting = False
        elif line.startswith('Quote'):
            quoting = True
            describing = False
        elif line == '':
            describing = False
            quoting = False
        else:
            if describing:
                if description:
                    description += line
                else:
                    description = line
            elif quoting:
                if quote:
                    quote += line
                else:
                    quote = line
        
    # Format description and quote
    description = description.replace('\n',' ')
    description = description.replace('  ', ' ')
    desc_parts = re.split('([.!?] *)', description)
    description = ''.join([each.capitalize() for each in desc_parts])
    description = description.replace(' i ', ' I ')
    if quote:
        quote = quote.replace('\n',' ')
        quote = quote.replace('  ', ' ')
        desc_parts = re.split('([.!?] *)', quote)
        quote = ''.join([each.capitalize() for each in desc_parts])
        quote = quote.replace(' i ', ' I ')
    
    if not description:
        raise Exception('A Description is required! (' + cdf_file + ')')
    
    try:
        return {'Title': title,
                'Description': description,
                'Quote': quote}
    except UnboundLocalError:
        raise Exception('A title is required! (' + cdf_file + ')')