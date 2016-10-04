import argparse, os
from generator.parser import parse_types, parse_cards
from generator.composer import compose_card


def generate():
    parser = argparse.ArgumentParser(
            description='Generate game cards.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter )

    parser.add_argument( '-t', '--types-folder', action='store', default='./assets/types/', help='The location of the folder containing the xml property files of the available game card types.' )
    parser.add_argument( '-f', '--fonts-folder', action='store', default='./assets/fonts/', help='The location of the folder containing the font files used in the game cards.' )
    parser.add_argument( '-c', '--cards-folder', action='store', default='./assets/cards/', help='The location of the folder containing the xml property files of the game cards to be generated.' )
    parser.add_argument( '-o', '--output-folder', action='store', default='./output/', help='The location of the folder in which to store generated cards.' )
    parser.add_argument( '-l', '--language', action='store', default='en', help='The language to use when generating cards.' )

    parser.add_argument( '-d', '--debug', action='store_true', help='Show debug output' )

    args = parser.parse_args()

    types_folder = os.path.abspath( args.types_folder )
    fonts_folder = os.path.abspath( args.fonts_folder )
    cards_folder = os.path.abspath( args.cards_folder )

    output_folder = os.path.abspath( args.output_folder )
    
    if os.path.exists( output_folder ) and not os.path.isdir( output_folder ):
        
        print( "Error: Could not write to {} because it exists and is not a directory.".format( output_folder ) )

        exit()

    card_types = parse_types( types_folder, fonts_folder, debug=args.debug )
    cards = parse_cards( cards_folder, args.language, card_types, debug=args.debug )

    if not os.path.exists( output_folder ):
        os.mkdir( output_folder )

    for card in cards:
        compose_card( card=card, output_directory=output_folder, debug=args.debug )

if __name__ == '__main__':
    generate()
