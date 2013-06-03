from Filer import *
from CdfParser import parse_cdf_file
from PIL import Image, ImageFont, ImageDraw

def get_title_fontsize(title):
    if len(title) > 20:
        return 20
    return 30

def get_description_fontsize(description, quote=None):
    return 20

# TODO
#    - Draw the card's description
#    - Make sure the description is drawn within the boundaries -> play with font size
#    - Implement the discard drink amount and draw it on the card if it is present
#    - Draw the card's quote if it is present

types = [ACTION, BACKSTAB, MANDATORY, STATUS]

locale = 'en'

# Loop over all card types
for card_type in types:
    # Get the folder paths containing the assets for this card type 
    image_folder = get_card_image_folder(card_type)
    properties_folder = get_card_properties_folder(card_type, locale)
    
    # Get all properties so we can check later if there are any properties
    # that were not processed into cards
    propertiess = os.listdir(properties_folder)
    
    # Loop over all card images and their properties in this directory
    for image_file in os.listdir(image_folder):
        
        # Get the properties file corresponding to this image
        properties_file = image_file.replace('.png', '.cdf')
        
        # Check if the properties file exists and warn the user if it doesn't
        if properties_file in propertiess:
            propertiess.remove(properties_file)
        else:
            print('There was no corresponding properties file for the image ' + \
                  get_card_image_file(image_file, card_type) + \
                  '.\nNo card was generated for this image.')
            continue
        
        # Parse the properties of this card
        properties = parse_cdf_file(get_card_properties_file(properties_file, card_type, locale))
        
        # Open the images for this card
        card = Image.open(get_card_template_file(card_type))
        image = Image.open(get_card_image_file(image_file, card_type)).resize((414,303))
        
        # Paste the cards image into the template
        card.paste(image, (43,83))
        
        # Calculate the font size for the card's title
        fs = get_title_fontsize(properties['Title'])
        font = ImageFont.truetype('C:\Windows\Fonts\BOD_PSTC.ttf', fs)
        
        # Draw the card's title on the template
        draw = ImageDraw.Draw(card)
        draw.text((45, 40), properties['Title'], (0, 0, 0), font=font)
        
        # Calculate the font size for the card's description
        if 'quote' in properties:
            fs = get_description_fontsize(properties['Description'], properties['quote'])
        else:
            fs = get_description_fontsize(properties['Description'])
        font = ImageFont.truetype('C:\Windows\Fonts\BOD_PSTC.ttf', fs)
        
        # Draw the card's description on the template
        draw = ImageDraw.Draw(card)
        draw.text((45, 40), properties['Description'], (0, 0, 0), font=font)
        
        card.save(get_card_output_file(image_file, card_type))
    
    for properties in propertiess:
        print('There was no corresponding image for the properties file ' + \
              get_card_properties_file(properties, card_type) + \
              '.\nNo card was generated for this properties.')