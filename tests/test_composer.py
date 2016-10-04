import unittests

class TestComposeCard( unittest.TestCase ):

    def setUp( self ):

        self.card_types = { 'testtype1': CardType( 'testtype1', {
            'type': 'text',
            'for': 'for1',
            'font': 'testfont1',
        } ) }
        self.cards = [ Card( name='testcard1', card_type='testtype1', elements={
            'for1': 'test text'
        } ) ]
