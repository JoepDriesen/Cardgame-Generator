import os
from xml.etree import ElementTree as et

class CardType( object ):

    def __init__( self, name, content ):
        self.name = name
        self.content = content


class Card( object ):

    def __init__( self, card_type, elements ):
        self.card_type = card_type
        self.elements = elements


def parse_type( types_directory, type_properties_file, fonts_directory ):

    abs_path = os.path.join( types_directory, type_properties_file )

    try:
        card_type_xml = et.parse( abs_path ).getroot()

    except et.ParseError as e:
        raise et.ParseError( '{} ({})'.format( e.msg, abs_path ) )
    
    name_el = card_type_xml.find( 'name' )
    if name_el is None:
        raise et.ParseError( 'No <name> element was found in card type properties xml: {}'.format( abs_path ) )
    
    content_el = card_type_xml.find( 'content' )
    if content_el is None:
        raise et.ParseError( 'No <content> element was found in card type properties xml: {}'.format( abs_path ) )
    
    content = []
    for el in content_el:

        if el.tag == 'text':

            if 'for' not in el.attrib:
                raise AttributeError( '<text> element is missing a required \'for\' attribute in card properties xml: {}'.format( abs_path ) )

            if 'font' not in el.attrib:
                raise AttributeError( '<text> element is missing a required \'font\' attribute in card properties xml: {}'.format( abs_path ) )

            if not os.path.isfile( os.path.join( fonts_directory, el.attrib['font'] ) ):
                raise FileNotFoundError( os.path.join( fonts_directory, el.attrib['font'] ) )

            content.append( {
                'type': 'text',
                'for': el.attrib.get( 'for' ),
                'font': el.attrib.get( 'font' ),
                'fontSize': int( el.attrib.get( 'fontSize', 10 ) ), 
                'x': int( el.attrib.get( 'x', 0 ) ),
                'y': int( el.attrib.get( 'y', 0 ) ),
                'w': int( el.attrib.get( 'w', 0 ) ),
                'h': int( el.attrib.get( 'h', 0 ) ),
                'multiline': el.attrib.get( 'multiline', 'false' ) in [ 'True', 'true', 1, '1', 't', 'y', 'yes' ],
            } )

    return CardType( name_el.text.strip(), content )


def parse_types( types_directory, fonts_directory ):
    
    return { 
        card_type.name: card_type for card_type in map( 
            lambda prop_file : parse_type( types_directory, prop_file, fonts_directory ),
            filter( 
                lambda fname : os.path.isfile( os.path.join( types_directory, fname ) ) and os.path.splitext( fname )[1] == '.xml',
                os.listdir( path=types_directory ) 
            )
        )
    }


def parse_card( cards_directory, card_name, language, card_types ):
    abs_path = os.path.join( cards_directory, card_name, '{}.xml'.format( language ) )

    try:
        card_xml = et.parse( abs_path ).getroot()

    except et.ParseError as e:
        e.msg = '{} ({})'.format( e.msg, abs_path )
        raise
    
    type_el = card_xml.find( 'type' )
    if type_el is None:
        raise et.ParseError( 'No <type> element was found in card properties xml: {}'.format( abs_path ) )

    if type_el.text.strip() not in card_types:
        raise TypeError( 'Unknown card type: {}'.format( type_el.text.strip() ) )

    card_type = card_types[type_el.text.strip()]
    elements = {}
    for c in card_type.content:

        for_el = card_xml.find( c['for'] )
        if for_el is None:
            raise et.ParseError( 'No <{}> element was found in card properties xml: {}'.format( c['for'], abs_path ) )

        elements[c['for']] = for_el.text.strip()

    return Card( card_type=card_type, elements=elements )

def parse_cards( cards_directory, language, card_types ):

    return list(
        map(
            lambda card_dir: parse_card( cards_directory, card_dir, language, card_types ),
            filter(
                lambda fname: os.path.isdir( os.path.join( cards_directory, fname ) ),
                os.listdir( path=cards_directory )
            )
        )
    )
