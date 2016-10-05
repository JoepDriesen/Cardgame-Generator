import os, re
from xml.etree import ElementTree as et

class CardType( object ):

    def __init__( self, name, content, template_file ):
        self.name = name
        self.content = content
        self.template_file = template_file

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


def parse_type( types_directory, type_directory, fonts_directory, debug=False ):

    props_file = os.path.join( types_directory, type_directory, "props.xml" )
    template_file = os.path.join( types_directory, type_directory, "template.png" )

    try:
        card_type_xml = et.parse( props_file ).getroot()

    except et.ParseError as e:
        e.msg = '{} ({})'.format( e.msg, props_file )
        raise
    
    name_el = card_type_xml.find( 'name' )
    if name_el is None:
        raise et.ParseError( 'No <name> element was found in card type properties xml: {}'.format( props_file ) )

    content_el = card_type_xml.find( 'content' )
    if content_el is None:
        raise et.ParseError( 'No <content> element was found in card type properties xml: {}'.format( props_file ) )
    
    content = {}
    for el in content_el:

        if el.tag == 'text':

            if 'id' not in el.attrib:
                raise AttributeError( '<text> element is missing a required \'id\' attribute in card type properties xml: {}'.format( props_file ) )

            if 'font-file' not in el.attrib and 'font-family' not in el.attrib:
                raise AttributeError( '<text> element is missing a required \'font-family\' or \'font-file\' attribute in card type properties xml: {}'.format( props_file ) )

            if 'font-file' in el.attrib:
                font_file = os.path.join( fonts_directory, el.attrib.get( 'font-file' ) )

                if not os.path.isfile( font_file ):
                    raise FileNotFoundError( font_file )

            else:
                font_file = None

            if 'font-size' not in el.attrib:
                raise AttributeError( '<text> element is missing a required \'font-size\' attribute in card type properties xml: {}'.format( props_file ) )

            if not re.match( '#[a-fA-F0-9]{6}', el.attrib['color'] ):
                raise AttributeError( '\'color\' attribute of <text> element should be in hexadecimal format (e.g. #ffffff) in type properties xml: {}'.format( props_file ) )

            content[el.attrib.get( 'id' )] = {
                'type': 'text',
                'id': el.attrib.get( 'id' ),
                'font-family': el.attrib.get( 'font-family', None ),
                'font-file': font_file,
                'font-size': int( el.attrib.get( 'font-size' ) ), 
                'font-style': el.attrib.get( 'font-style', 'regular' ), 
                'font-weight': el.attrib.get( 'font-weight', '400' ), 
                'color': el.attrib.get( 'color', 'rgb(0,0,0)' ).strip(), 
                'x': int( el.attrib.get( 'x', 0 ) ),
                'y': int( el.attrib.get( 'y', 0 ) ),
                'w': int( el.attrib.get( 'w', 0 ) ),
                'h': int( el.attrib.get( 'h', 0 ) ),
                'anchor': el.attrib.get( 'anchor', 'top' ),
                'align': el.attrib.get( 'align', 'left' ),
                'multiline': el.attrib.get( 'multiline', 'false' ) in [ 'True', 'true', 1, '1', 't', 'y', 'yes' ],
            }

    if debug:
        print( "    Parsed card type: {}".format( name_el.text.strip() ) )
    
    return CardType( name=name_el.text.strip(), content=content, template_file=template_file )


def parse_types( types_directory, fonts_directory, debug=False ):
    
    if debug:
        print( 'Parsing card types...' )
    
    def is_type_dir( fname ):
        
        abs_path = os.path.join( types_directory, fname )

        if not os.path.isdir( abs_path ):

            if debug:
                print( '    Skipping {} because it is not a directory'.format( abs_path ) )

            return False

        if not os.path.isfile( os.path.join( abs_path, "props.xml" ) ):

            if debug:
                print( '    Skipping {} because it does not contain a required "props.xml" file'.format( abs_path ) )

            return False

        if not os.path.isfile( os.path.join( abs_path, "template.png" ) ):

            if debug:
                print( '    Skipping {} because it does not contain a required "template.png" file'.format( abs_path ) )

            return False

        if debug:
            print( '    Found type directory: {}'.format( fname ) )

        return True

    card_types = { 
        card_type.name.lower(): card_type for card_type in map( 
            lambda type_dir : parse_type( types_directory, type_dir, fonts_directory, debug=debug ),
            filter( is_type_dir, sorted( os.listdir( path=types_directory ) ) )
        )
    }

    print( "Parsed {} card types.".format( len( card_types ) ) )

    return card_types


def parse_card( cards_directory, card_name, language, card_types, debug=False ):
    abs_path = os.path.join( cards_directory, card_name, '{}.xml'.format( language ) )

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
