import os, unittest
from generator import parser
from xml.etree import ElementTree as et
from lxml.etree import XMLSyntaxError


TEST_FILES = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), 'test_files' )
SCHEMAS_DIR = os.path.join( os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) ), 'schemas' )


class TestValidator( unittest.TestCase ):

    def setUp( self ):

        self.types_schema_file = os.path.join( SCHEMAS_DIR, 'card_types.xsd' )
        self.cards_schema_file = os.path.join( SCHEMAS_DIR, 'cards.xsd' )

    def test_valid_schema( self ):
        
        valid_card_type_file = os.path.join( TEST_FILES, 'schemas', 'card_type.xml' )
        parser.validate_schema( valid_card_type_file, self.types_schema_file )
        
        valid_card_file = os.path.join( TEST_FILES, 'schemas', 'card.xml' )
        parser.validate_schema( valid_card_file, self.cards_schema_file )

    def test_invalid_schema( self ):

        for fname in os.listdir( os.path.join( TEST_FILES, 'schemas', 'invalid' ) ):

            abs_path = os.path.join( TEST_FILES, 'schemas', 'invalid', fname )

            if fname.startswith( 'card_type' ):
                self.assertRaises( XMLSyntaxError, lambda: parser.validate_schema( abs_path, self.types_schema_file ) )

            elif fname.startswith( 'card' ):
                self.assertRaises( XMLSyntaxError, lambda: parser.validate_schema( abs_path, self.cards_schema_file ) )


class TestParseType( unittest.TestCase ):

    def setUp( self ):

        self.types_dir = os.path.join( TEST_FILES, 'types' )
        self.fonts_dir = os.path.join( TEST_FILES, 'fonts' )
        self.images_dir = os.path.join( TEST_FILES, 'images' )

    def test_file_does_not_exist( self ):

        self.assertRaises( 
            FileNotFoundError, 
            lambda: parser.parse_type( 
                os.path.join( TEST_FILES, 'fubar', 'test.xml' ), 
                os.path.join( TEST_FILES, 'fonts' ),
                None
            )
        )
    
        self.assertRaises( 
            FileNotFoundError, 
            lambda: parser.parse_type( 
                os.path.join( TEST_FILES, 'fubar.xml' ), 
                os.path.join( TEST_FILES, 'fonts' ),
                None
            )
        )

    def test_default_attributes( self ):

        card_type = parser.parse_type( os.path.join( self.types_dir, 'defaults.xml' ), self.fonts_dir, None )

        self.assertEqual( card_type.name, 'test' )
        self.assertEqual( len( card_type.content ), 1 )

        t = card_type.content['test']

        self.assertEqual( t['id'], 'test' )
        self.assertEqual( t['font-file'], os.path.join( self.fonts_dir, 'test.ttf' ) )
        self.assertEqual( t['font-size'], 3 )
        self.assertEqual( t['color'], '#000000' )
        self.assertEqual( t['x'], 0 )
        self.assertEqual( t['y'], 0 )
        self.assertEqual( t['w'], 0 )
        self.assertEqual( t['h'], 0 )
        self.assertEqual( t['anchor'], 'top' )
        self.assertEqual( t['align'], 'left' )
        self.assertEqual( t['multiline'], False )

    def test_custom_attributes( self ):

        card_type = parser.parse_type( os.path.join( self.types_dir, 'custom_attributes.xml' ), self.fonts_dir, None )

        self.assertEqual( card_type.name, 'test' )
        self.assertEqual( len( card_type.content ), 1 )

        t = card_type.content['test']

        self.assertEqual( t['id'], 'test' )
        self.assertEqual( t['font-file'], os.path.join( self.fonts_dir, 'test.ttf' ) )
        self.assertEqual( t['font-size'], 20 )
        self.assertEqual( t['color'], '#ffffff' )
        self.assertEqual( t['x'], 10 )
        self.assertEqual( t['y'], 20 )
        self.assertEqual( t['w'], 30 )
        self.assertEqual( t['h'], 40 )
        self.assertEqual( t['anchor'], 'bottom' )
        self.assertEqual( t['align'], 'right' )
        self.assertEqual( t['multiline'], True )

    def test_missing_font( self ):

        self.assertRaises( 
            FileNotFoundError, 
            lambda: parser.parse_type( 
                os.path.join( self.types_dir, 'missing_font.xml' ), 
                self.fonts_dir,
                None
            )
        )

    def test_global_image( self ):

        self.assertRaises(
            FileNotFoundError,
            lambda: parser.parse_type( 
                os.path.join( self.types_dir, 'missing_image.xml' ), 
                self.fonts_dir, 
                self.images_dir 
            )
        )
            
        parser.parse_type( 
            os.path.join( self.types_dir, 'image.xml' ), 
            self.fonts_dir, 
            self.images_dir 
        )

    def test_content_order_intact( self ):

        t = parser.parse_type( os.path.join( self.types_dir, 'ordering.xml' ), self.fonts_dir, self.images_dir )
        
        self.assertEqual( len( t.content ), 4 )

        c = list( t.content.items() )
        self.assertEqual( c[0][1]['type'], 'image' )
        self.assertEqual( c[1][1]['type'], 'text' )
        self.assertEqual( c[2][1]['type'], 'image' )
        self.assertEqual( c[3][1]['type'], 'text' )


class TestParseTypes( unittest.TestCase ):

    def test_multiple_types( self ):

        fonts_dir = os.path.join( TEST_FILES, 'fonts' )

        card_types = parser.parse_types( 
                types_directory=os.path.join( TEST_FILES, 'multiple_types' ), 
                fonts_directory=fonts_dir,
                images_directory=None,
        )
        
        self.assertEqual( len( card_types ), 2 )


class TestParseCard( unittest.TestCase ):

    def setUp( self ):
        self.card_types = { 'test': parser.CardType( 'test', { 'test1': { 'id': 'test1' } } ) }

    def test_missing_files( self ):

        cards_dir = os.path.join( TEST_FILES, 'cards' )

        self.assertRaises( 
            FileNotFoundError, 
            lambda: parser.parse_card( cards_dir, 'doesnotexist', 'testlan', self.card_types ) 
        )
        self.assertRaises( 
            FileNotFoundError, 
            lambda: parser.parse_card( cards_dir, 'test', 'doesnotexist', self.card_types ) 
        )

    def test_missing_type( self ):

        self.assertRaises( et.ParseError, lambda: parser.parse_card( TEST_FILES, 'cards', 'missing_type', self.card_types ) )
    
    def test_correct( self ):

        card = parser.parse_card( TEST_FILES, 'cards', 'correct', self.card_types )

        self.assertEqual( card.card_type, self.card_types['test'] )
        self.assertEqual( card.elements['test1'], 'Test' )
        

class TestParseCards( unittest.TestCase ):

    def setUp( self ):
        self.card_types = { 'test': parser.CardType( 'test', { 'test1': { 'id': 'test1' } } ) }

    def test_multiple_types( self ):

        cards = parser.parse_cards( os.path.join( TEST_FILES, 'multiple_cards' ), 'testlan', self.card_types )

        self.assertEqual( len( cards ), 2 )


if __name__ == '__main__':
    unittest.main()
