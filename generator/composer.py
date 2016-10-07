import os, xml.etree.ElementTree as et
from PIL import Image, ImageDraw, ImageFont
from generator.utils import get_image_size

def compose_card( card, card_width, card_height, output_directory, debug=False ):

    card.image_file = os.path.join( output_directory, '{}.png'.format( card.name ) )
    t = card.card_type

    im = Image.new( mode='RGBA', size=( card_width, card_height ) )
    draw = ImageDraw.Draw( im )

    for el_name, c in t.content.items():

        if c['type'] == 'image':

            w = c['w']
            if type( w ) == str:
                w = int( card_width * ( int( w.replace( '%', '' ) ) / 100.0 ) )

            h = c['h']
            if type( h ) == str:
                h = int( card_height * ( int( h.replace( '%', '' ) ) / 100.0 ) )

            i_w, i_h = get_image_size( c['filename'] )
            
            paste_im = Image.open( c['filename'] )
            if ( i_w != w or i_h != h ):
                paste_im = paste_im.resize( ( w, h ) )

            im.paste( paste_im, ( c['x'], c['y'] , c['x'] + w, c['y'] + h ) )

        elif c['type'] == 'text':
        
            if el_name not in card.elements:
                continue

            font = ImageFont.truetype( c['font-file'], c['font-size'] )
            
            text = card.elements[el_name]
    
            text = text.replace( '*', '•' )
    
            if not c['multiline']:
    
                if c['w']:
                    while font.getsize( text )[0] > c['w']:
                        text = remove_last_word( text )[0]
             
                if c['w'] and c['align'] == 'center':
                    x = c['x'] + ( c['w'] - font.getsize( line )[0] ) / 2
    
                elif c['w'] and c['align'] == 'right':
                    x = c['x'] + c['w'] - font.getsize( line )[0]
    
                else:
                    x = c['x']
    
                draw.text( ( x, c['y'] ), text, font=font, fill=c['color'] )
    
            else:
             
                text_lines = text.splitlines()
                y = c['y']
                line_height = font.getsize( 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' )[1]
                bot = c['anchor'] == 'bottom'
    
                if bot:
                    text_lines = reversed( text_lines )
    
                def inc_y( cur_y ):
                    return cur_y - line_height if bot else cur_y + line_height
    
                for text_line in text_lines:
    
                    text_line = text_line.strip()
    
                    if not c['w']:
    
                        draw.text( ( c['x'], y ), text_line, font=font, fill=c['color'] )
                        y = inc_y( y )
    
     
                    else:
     
                        h_text = 0
                        text_left = text_line
                        lines = []
     
                        while True:
                         
                            if c['h'] and h_text + line_height  > c['h']:
                                break
     
                            text_next = ''
     
                            w_line, h_line = font.getsize( text_left )
     
                            while w_line > c['w']:
                             
                                text_left, last_word = remove_last_word( text_left )
     
                                if text_left == '':
                                    text_left = last_word
                                    break
                             
                                else:
                                    text_next = last_word + ' ' + text_next
     
                                    w_line = font.getsize( text_left )[0]
     
                            lines.append( text_left )
                         
                            if text_next == '':
                                break
                            text_left = text_next
     
                        if bot:
                            lines = reversed( lines )
     
                        for line in lines:
                            if c['align'] == 'center':
                                x = c['x'] + ( c['w'] - font.getsize( line )[0] ) / 2
                         
                            elif c['align'] == 'right':
                                x = c['x'] + c['w'] - font.getsize( line )[0]
    
                            else:
                                x = c['x']
    
                            draw.text( ( x, y ), line, font=font, fill=c['color'] )
                            y = inc_y( y )
             
    im.save( card.image_file )

    if debug:
        print('    Finished composing card: {}'.format( card.name ) )

def remove_last_word( text ):
    
    text = text.strip()
    word = ''
    rest = text

    for letter in reversed( text ):
        rest = rest[:-1]
        if letter == ' ':
            return rest, word
        word = letter + word
    
    return rest, word
