from Filer import *
from CdfParser import parse_cdf_file
from PIL import Image, ImageFont, ImageDraw

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
    description_folder = get_card_description_folder(card_type, locale)
    
    # Get all descriptions so we can check later if there are any descriptions
    # that were not processed into cards
    descriptions = os.listdir(description_folder)
    
    # Loop over all card images and their descriptions in this directory
    for image_file in os.listdir(image_folder):
        
        # Get the description file corresponding to this image
        description_file = image_file.replace('.png', '.cdf')
        
        # Check if the description file exists and warn the user if it doesn't
        if description_file in descriptions:
            descriptions.remove(description_file)
        else:
            print('There was no corresponding description file for the image ' + \
                  get_card_image_file(image_file, card_type) + \
                  '.\nNo card was generated for this image.')
            continue
        
        # Parse the description of this card
        description = parse_cdf_file(get_card_description_file(description_file, card_type, locale))
        
        # Open the images for this card
        card = Image.open(get_card_template_file(card_type))
        image = Image.open(get_card_image_file(image_file, card_type)).resize((414,303))
        
        # Paste the cards image into the template
        card.paste(image, (43,83))
        
        # Pick the font for the card's title
        # TODO: Check if the title length requires a smaller font
        font = ImageFont.truetype('C:\Windows\Fonts\BOD_PSTC.ttf', 30)
        
        # Draw the card's title on the template
        draw = ImageDraw.Draw(card)
        draw.text((45, 40), description['Title'], (0, 0, 0), font=font)
        
        card.save(get_card_output_file(image_file, card_type))
    
    for description in descriptions:
        print('There was no corresponding image for the description file ' + \
              get_card_description_file(description, card_type) + \
              '.\nNo card was generated for this description.')