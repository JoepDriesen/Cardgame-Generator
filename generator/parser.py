import os, re
from xml.etree import ElementTree as et
from lxml import etree, objectify

CARD_TYPES_SCHEMA = os.path.join( os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) ), 'schemas', 'card_types.xsd' )
CARDS_SCHEMA = os.path.join( os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) ), 'schemas', 'cards.xsd' )

class CardType( object ):

    def __init__( self, name, content ):
        self.name = name
        self.content = content

        self.font_files = {}
        for c in self.content.values():
                        
            if c.get( 'font-file', None ) is not None:
                # File font
                self.font_files[os.path.basename( c['font-file'] )] = c['font-file']


class Card( object ):

    def __init__( self, name, card_type, elements ):
        self.name = name
        self.card_type = card_type
        self.elements = elements


def parse_type( type_props_file, fonts_directory, images_directory, debug=False ):

    validate_schema( type_props_file, CARD_TYPES_SCHEMA )

    try:
        card_type_xml = et.parse( type_props_file ).getroot()

    except et.ParseError as e:
        e.msg = '{} ({})'.format( e.msg, type_props_file )
        raise
   
    name_el = card_type_xml.find( 'name' )

    content = {}
    for el in card_type_xml.find( 'content' ):

        if el.tag == 'text':

            font_file = os.path.join( fonts_directory, el.attrib.get( 'font-file' ) )

            if not os.path.isfile( font_file ):
                raise FileNotFoundError( font_file )

            if 'font-size' not in el.attrib:
                raise AttributeError( '<text> element is missing a required \'font-size\' attribute in card type properties xml: {}'.format( type_props_file ) )

            if 'color' in el.attrib and not re.match( '#[a-fA-F0-9]{6}', el.attrib['color'] ):
                raise AttributeError( '\'color\' attribute of <text> element should be in hexadecimal format (e.g. #ffffff) in type properties xml: {}'.format( type_props_file ) )

            content[el.attrib.get( 'id' )] = {
                'type': 'text',
                'id': el.attrib.get( 'id' ),
                'font-file': font_file,
                'font-size': int( el.attrib.get( 'font-size' ) ), 
                'color': el.attrib.get( 'color', '#000000' ).strip(), 
                'x': int( el.attrib.get( 'x', 0 ) ),
                'y': int( el.attrib.get( 'y', 0 ) ),
                'w': int( el.attrib.get( 'w', 0 ) ),
                'h': int( el.attrib.get( 'h', 0 ) ),
                'anchor': el.attrib.get( 'anchor', 'top' ),
                'align': el.attrib.get( 'align', 'left' ),
                'multiline': el.attrib.get( 'multiline', 'false' ) in [ 'True', 'true', 1, '1', 't', 'y', 'yes' ],
            }

        elif el.tag == 'image':

            if el.attrib.get( 'type' ) == 'global':
                image_file = os.path.join( images_directory, el.attrib.get( 'filename' ) )

            else:
                image_file = os.path.join( os.path.dirname( type_props_file ), el.attrib.get( 'filename' ) )

            if not os.path.isfile( image_file ):
                raise FileNotFoundError( image_file )

            w = el.attrib.get( 'w', '100%' )
            if not w.endswith( '%' ):
                w = int( w )

            h = el.attrib.get( 'h', '100%' )
            if not h.endswith( '%' ):
                h = int( h )
                
            content[el.attrib.get( 'id' )] = {
                'type': 'image',
                'id': el.attrib.get( 'id' ),
                'filename': image_file,
                'x': int( el.attrib.get( 'x', 0 ) ),
                'y': int( el.attrib.get( 'y', 0 ) ),
                'w': w,
                'h': h,
                'anchor': el.attrib.get( 'anchor', 'top' ),
                'align': el.attrib.get( 'align', 'left' ),
            }



    if debug:
        print( "    Parsed card type: {}".format( name_el.text.strip() ) )
    
    return CardType( name=name_el.text.strip(), content=content )


def parse_types( types_directory, fonts_directory, images_directory, debug=False ):
    
    if debug:
        print( 'Parsing card types...' )
    
    def is_type_props_file( fname ):
        
        abs_path = os.path.join( types_directory, fname )

        if not os.path.isfile( abs_path ):

            if debug:
                print( '    Skipping {} because it is not a file'.format( abs_path ) )

            return False

        if not os.path.splitext( abs_path )[1] == '.xml':

            if debug:
                print( '    Skipping {} because it is not an XML file'.format( abs_path ) )

            return False

        if debug:
            print( '    Found type properties file: {}'.format( fname ) )

        return True

    card_types = { 
        card_type.name.lower(): card_type for card_type in map( 
            lambda fname: parse_type( os.path.join( types_directory, fname ), fonts_directory, images_directory, debug=debug ),
            filter( is_type_props_file, sorted( os.listdir( path=types_directory ) ) )
        )
    }

    print( "Parsed {} card types.".format( len( card_types ) ) )

    return card_types


def parse_card( cards_directory, card_name, language, card_types, debug=False ):
    abs_path = os.path.join( cards_directory, card_name, '{}.xml'.format( language ) )

    validate_schema( abs_path, CARDS_SCHEMA )

    try:
        card_xml = et.parse( abs_path ).getroot()

    except et.ParseError as e:
        e.msg = '{} ({})'.format( e.msg, abs_path )
        raise
    
    type_el = card_xml.find( 'type' )
    if type_el is None:
        raise et.ParseError( 'No <type> element was found in card properties xml: {}'.format( abs_path ) )

    if type_el.text.strip().lower() not in card_types:
        raise TypeError( 'Unknown card type: {}'.format( type_el.text.strip() ) )

    card_type = card_types[type_el.text.strip()]
    elements = {}
    for c in card_type.content.values():

        for_el = card_xml.find( c['id'] )
        if for_el is None:

            if c.get( 'required', False ):
                raise et.ParseError( 'No <{}> element was found in card properties xml: {}'.format( c['id'], abs_path ) )

        else:
            elements[c['id']] = for_el.text.strip()

    return Card( name=card_name, card_type=card_type, elements=elements )

def parse_cards( cards_directory, language, card_types, debug=False ):

    if debug:
        print( "Parsing cards..." )
    
    def is_card_dir( fname ):

        abs_path = os.path.join( cards_directory, fname )

        if not os.path.isdir( abs_path ):

            if debug:
                print( '    Skipping {} because it is not a directory'.format( abs_path ) )

            return False

        if not os.path.isfile( os.path.join( abs_path, '{}.xml'.format( language ) ) ):

            print( '    Warning! Skipping {} because it is does not contain a necessary language file: {}.xml'.format( abs_path, language ) )

            return False

        if debug:
            print( '    Found card directory: {}'.format( fname ) )

        return True

    cards = list(
        map(
            lambda card_dir: parse_card( cards_directory, card_dir, language, card_types, debug=debug ),
            filter( is_card_dir, sorted( os.listdir( path=cards_directory ) ) )
        )
    )

    print( "Parsed {} cards".format( len( cards ) ) )

    return cards


def validate_schema( xml_file, schema_file ):

    with open( xml_file, 'r' ) as f:

        schema = etree.XMLSchema( file=schema_file )
        parser = objectify.makeparser( schema=schema )
        objectify.fromstring( f.read(), parser )

    return
