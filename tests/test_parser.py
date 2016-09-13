import os, unittest
from generator.parser import parse_type, parse_types, parse_card, parse_cards, \
        CardType
from xml.etree import ElementTree as et


TEST_FILES = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), 'test_files' )


class TestParseType( unittest.TestCase ):

    def test_file_does_not_exist( self ):

        self.assertRaises( FileNotFoundError, lambda: parse_type( os.path.join( TEST_FILES, 'fubar' ), 'test.xml', os.path.join( TEST_FILES, 'fonts' ) ) )
        self.assertRaises( FileNotFoundError, lambda: parse_type( TEST_FILES, 'fubar.xml', os.path.join( TEST_FILES, 'fonts' ) ) )

    def test_missing_elements( self ):

        types_dir = os.path.join( TEST_FILES, 'types' )
        fonts_dir = os.path.join( TEST_FILES, 'fonts' )

        self.assertRaises( et.ParseError, lambda: parse_type( types_dir, 'no_name.xml', fonts_dir ) )
        self.assertRaises( et.ParseError, lambda: parse_type( types_dir, 'no_content.xml', fonts_dir ) )

    def test_missing_attributes( self ):

        types_dir = os.path.join( TEST_FILES, 'types' )
        fonts_dir = os.path.join( TEST_FILES, 'fonts' )

        self.assertRaises( AttributeError, lambda: parse_type( types_dir, 'bad_attributes.xml', fonts_dir ) )

    def test_default_attributes( self ):

        types_dir = os.path.join( TEST_FILES, 'types' )
        fonts_dir = os.path.join( TEST_FILES, 'fonts' )

        card_type = parse_type( types_dir, 'defaults.xml', fonts_dir )

        self.assertEqual( card_type.name, 'test' )
        self.assertEqual( len( card_type.content ), 1 )

        t = card_type.content[0]

        self.assertEqual( t['for'], 'rules' )
        self.assertEqual( t['font'], 'test.ttf' )
        self.assertEqual( t['fontSize'], 10 )
        self.assertEqual( t['x'], 0 )
        self.assertEqual( t['y'], 0 )
        self.assertEqual( t['w'], 0 )
        self.assertEqual( t['h'], 0 )
        self.assertEqual( t['multiline'], False )

    def test_custom_attributes( self ):

        types_dir = os.path.join( TEST_FILES, 'types' )
        fonts_dir = os.path.join( TEST_FILES, 'fonts' )

        card_type = parse_type( types_dir, 'custom_attributes.xml', fonts_dir )

        self.assertEqual( card_type.name, 'test' )
        self.assertEqual( len( card_type.content ), 1 )

        t = card_type.content[0]

        self.assertEqual( t['for'], 'rules' )
        self.assertEqual( t['font'], 'test.ttf' )
        self.assertEqual( t['fontSize'], 20 )
        self.assertEqual( t['x'], 10 )
        self.assertEqual( t['y'], 20 )
        self.assertEqual( t['w'], 30 )
        self.assertEqual( t['h'], 40 )
        self.assertEqual( t['multiline'], True )

    def test_missing_font( self ):

        types_dir = os.path.join( TEST_FILES, 'types' )
        fonts_dir = os.path.join( TEST_FILES, 'fonts' )

        self.assertRaises( FileNotFoundError, lambda: parse_type( types_dir, 'missing_font.xml', fonts_dir ) )


class TestParseTypes( unittest.TestCase ):

    def test_multiple_types( self ):

        fonts_dir = os.path.join( TEST_FILES, 'fonts' )

        card_types = parse_types( os.path.join( TEST_FILES, 'multiple_types' ), fonts_dir )
        
        self.assertEqual( len( card_types ), 2 )


class TestParseCard( unittest.TestCase ):

    def setUp( self ):
        self.card_types = { 'test': CardType( 'test', [ { 'for': 'test1' } ] ) }

    def test_missing_files( self ):

        cards_dir = os.path.join( TEST_FILES, 'cards' )

        self.assertRaises( FileNotFoundError, lambda: parse_card( cards_dir, 'doesnotexist', 'testlan', self.card_types ) )
        self.assertRaises( FileNotFoundError, lambda: parse_card( cards_dir, 'test', 'doesnotexist', self.card_types ) )

    def test_missing_elements( self ):

        self.assertRaises( et.ParseError, lambda: parse_card( TEST_FILES, 'cards', 'missing_el', self.card_types ) )
    
    def test_missing_type( self ):

        self.assertRaises( TypeError, lambda: parse_card( TEST_FILES, 'cards', 'missing_type', self.card_types ) )

    def test_missing_type_elements( self ):

        self.assertRaises( et.ParseError, lambda: parse_card( TEST_FILES, 'cards', 'missing_type_el', self.card_types ) )

    def test_correct( self ):

        card = parse_card( TEST_FILES, 'cards', 'correct', self.card_types )

        self.assertEqual( card.card_type, self.card_types['test'] )
        self.assertEqual( card.elements['test1'], 'Test' )
        

class TestParseTypes( unittest.TestCase ):

    def test_multiple_types( self ):

        card_types = { 'test': CardType( 'test', [ { 'for': 'test1' } ] ) }
        cards = parse_cards( os.path.join( TEST_FILES, 'multiple_cards' ), 'testlan', card_types )

        self.assertEqual( len( cards ), 2 )



if __name__ == '__main__':
    unittest.main()
