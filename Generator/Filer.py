import os

card_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../Cards')
output_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../Output')

# Card Types
ACTION = 'Action'
BACKSTAB = 'Backstab'
MANDATORY = 'Mandatory'
STATUS = 'Status'

def get_card_image_folder(card_type):
    return os.path.realpath(card_dir + '/Images/' + card_type)
    
def get_card_image_file(card_name, card_type):
    return os.path.realpath(card_dir + '/Images/' + card_type + '/' + card_name)

def get_card_description_file(card_name, card_type, locale='en'):
    return os.path.realpath(card_dir + '/Descriptions/' + card_type + '/' + locale + '/' + card_name)

def get_card_template_file(card_type):
    return os.path.realpath(card_dir + '/Templates/' + card_type + '.png')

def get_card_output_file(card_name, card_type):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    type_dir = os.path.realpath(output_dir + '/' + card_type)
    if not os.path.exists(type_dir):
        os.mkdir(type_dir)
    return os.path.realpath(type_dir + '/' + card_name)