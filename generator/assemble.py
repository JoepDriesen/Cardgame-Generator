'''
Created on Feb 4, 2015

@author: Joep Driesen
'''
import os
from generator.files import OUTPUT_DIR, OUTPUT_CARDS_DIR
from wand.image import Image
from wand.drawing import Drawing
import textwrap

def setup():
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    if not os.path.isdir(OUTPUT_CARDS_DIR):
        os.mkdir(OUTPUT_CARDS_DIR)

def wrap_text(text, draw_obj, image_obj, max_width):
    """
    text should be an array of lines to wrap
    
    """
    lines = []
    for line in text: 
        line_len = len(line) + 1
        max_line_width = max_width + 1
        while max_line_width > max_width:
            line_len -= 1
            if line_len == 0:
                raise AttributeError('Font size is too large, unable to wrap')
            
            wrapped_lines = textwrap.wrap(line, line_len)
            max_line_width = 0
            for wrapped_line in wrapped_lines:
                metr = draw_obj.get_font_metrics(image_obj, wrapped_line)
                max_line_width = max(max_line_width, metr.text_width)
                
        lines.extend(wrapped_lines)
    return lines
    
    
def assemble_card(card, card_width, card_height, font):
    setup()
    
    output_file = os.path.join(OUTPUT_CARDS_DIR, '{}.png'.format(card.dir_name))
    
    with Image(width=card_width, height=card_height) as card_img:
        # Load the card type template
        with Image(filename=card.type.template_file) as card_template:
            
            # Calculate the size ratios for the template
            width_ratio = card_img.width / float(card_template.width)
            height_ratio = card_img.height / float(card_template.height)
            
            # Resize the template so it fits to the required dimensions
            card_template.resize(width=card_width, height=card_height)
            
            card_img.composite(card_template, top=0, left=0)
            
            # Load image graphic
            with Image(filename=card.image_file).clone() as card_graphic:
                cgb = card.type.card_graphic_box
                
                card_graphic.resize(width=round(cgb[2] * width_ratio), height=round(cgb[3] * height_ratio))
            
                # Put the card graphic on the image
                card_img.composite(card_graphic, top=int(cgb[1] * height_ratio), left=int(cgb[0] * width_ratio))
                
                with Drawing() as draw:
                    draw.font = font.file
                    
                    for cn, props in card.type.content.items():
                        content = card.get_content(cn)
                        if content is None:
                            continue
                        draw.font_size = props['fontSize']
                        if 'h' in props:
                            y = props['y'] + props['h'] - round((props['h'] - (props['fontSize'] / font.font_size_to_text_height_ratio)) / 2)
                        else:
                            y = props['y'] + round(props['fontSize'] / font.font_size_to_text_height_ratio) 
                        text = '\n'.join(wrap_text(content, draw, card_img, props['w']))
                        
                        if text == '':
                            continue
                        draw.text(x=props['x'], y=y, body=text)
                        draw(card_img)
                    
                    card_img.save(filename=output_file)
                
                