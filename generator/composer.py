import os, xml.etree.ElementTree as et
from PIL import Image, ImageDraw, ImageFont

def compose_card( card, output_directory, font_imports_file=None, debug=False ):

    abs_path = os.path.join( output_directory, '{}.png'.format( card.name ) )
    t = card.card_type
    template_size = get_image_size( t.template_file )

    im = Image.open( t.template_file )
    draw = ImageDraw.Draw( im )

    for el_name, c in t.content.items():

        if el_name not in card.elements:
            continue

        if c['font-file'] is not None:
            font = ImageFont.truetype( c['font-file'], c['font-size'] )
            
        elif c['font-family'] is not None:
            font = ImageFont.load_path( c['font-family'] )
        
        else:

            if debug:
                print( '    Warning: Using default font for \'{}\' in card: {}'.format( el_name, card.name ) )

            font = ImageFont.load_default()

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
            
    im.save( abs_path )

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


"""
    svg = et.Element( "svg", attrib={
        'version': '1.2',
        'baseProfile': 'tiny',
        'xmlns': "http://www.w3.org/2000/svg",
        'xmlns:ev': "http://www.w3.org/2001/xml-events",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'width': str( template_size[0] ),
        'height': str( template_size[1] )
    } )

    defs = et.SubElement( svg, 'defs' )
   
    if font_imports_file:
    
        # Add font imports
        style = et.SubElement( defs, 'style', attrib={ 'type': 'text/css' } )
        with open( font_imports_file, 'r' ) as f:
            style.text = f.read()

    # Add template image
    et.SubElement( svg, 'image', attrib={
        'x': '0',
        'y': '0',
        'width': str( template_size[0] ),
        'height': str( template_size[1] ),
        'xlink:href': t.template_file
    } )

    # Add text elements
    for c, a in t.content.items():

        if c in card.elements:
            
            text = card.elements[c]

            if not a['multiline']:

                t = et.SubElement( svg, 'text', attrib={
                    'x': str( a['x'] ),
                    'y': str( a['y'] ),
                    'font-family': a['font-family'],
                    'font-size': str( a['font-size'] ),
                    'font-style': str( a['font-style'] ),
                    'font-weight': str( a['font-weight'] ),
                    'fill': a['color']
                } )
                t.text = text

            else:

                t = et.SubElement( svg, 'textArea', attrib={
                    'x': str( a['x'] ),
                    'y': str( a['y'] ),
                    'width': str( a['w'] ),
                    'height': str( a['h'] ),
                    'font-family': a['font-family'],
                    'font-size': str( a['font-size'] ),
                    'font-style': str( a['font-style'] ),
                    'font-weight': str( a['font-weight'] ),
                    'fill': a['color'],
                } )
                t.text = text


    tree = et.ElementTree( svg )
    tree.write( abs_path, encoding='utf-8', xml_declaration=True )


    dwg = svgwrite.Drawing( os.path.join( output_directory, '{}.svg'.format( card.name ) ), size=template_size, profile='tiny' )

    dwg.add( dwg.image( t.template_file, insert=( 0, 0 ), size=template_size ) )

    for el_name in card.elements:

        attr = t.content[ el_name ]
        
        if attr.get( 'multiline', False ):
            dwg.add( dwg.textArea(
                text=card.elements[ el_name ],
                insert=( attr[ 'x' ], attr[ 'y' ] ),
                size=( attr[ 'w' ], attr.get( 'h', 10000 ) ),
                fill=attr[ 'fontColor' ],
                font_family=attr[ 'font' ],
                font_size=attr[ 'fontSize' ]
            ) )

        else:
            dwg.add( dwg.text(
                text=card.elements[ el_name ],
                insert=( attr[ 'x' ], attr[ 'y' ] ),
                fill=attr[ 'fontColor' ],
                font_family=attr[ 'font' ],
                font_size=attr[ 'fontSize' ]
            ) )
            
    dwg.save()
"""

import struct
import imghdr

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height
