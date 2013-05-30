from Filer import *
from PIL import Image

types = [ACTION, BACKSTAB, MANDATORY, STATUS]

for card_type in types:
    folder = get_card_image_folder(card_type)
    
    for image_name in os.listdir(folder):
        card = Image.open(get_card_template_file(card_type))
        image = Image.open(get_card_image_file(image_name, card_type)).resize((414,303))
        
        card.paste(image, (43,83))
        card.save(get_card_output_file(image_name, card_type))