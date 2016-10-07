import argparse, os
from generator.parser import parse_types, parse_cards
from generator.composer import compose_card
from generator.pdf import generate_printable_pdf


def generate():
    parser = argparse.ArgumentParser(
            description='Generate game cards.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter )

    parser.add_argument( '-t', '--types-folder', action='store', default='./assets/types/', help='The location of the folder containing the xml property files of the available game card types.' )
    parser.add_argument( '-f', '--fonts-folder', action='store', default='./assets/fonts/', help='The location of the folder containing the font files used by the card types.' )
    parser.add_argument( '-c', '--cards-folder', action='store', default='./assets/cards/', help='The location of the folder containing the xml property files of the game cards to be generated.' )
    parser.add_argument( '-i', '--images-folder', action='store', default='./assets/images/', help='The location of the folder containing the global images used by the game cards to be generated.' )
    parser.add_argument( '-b', '--cardback_file', action='store', default=None, help='If provided, this image will be used as a cardback for the generated cards.' )
    parser.add_argument( '-o', '--output-folder', action='store', default='./output/', help='The location of the folder in which to store generated cards.' )
    parser.add_argument( '-l', '--language', action='store', default='en', help='The language to use when generating cards.' )
    parser.add_argument( '-s', '--single-card', action='store', default=None, help='If provided, only the card with this folder name will be generated. Implies --skip-pdf.' )
    parser.add_argument( '-p', '--skip-pdf', action='store_const', const=True, default=False, help='If provided, no printable pdf containing all the cards will be generated.' )

    parser.add_argument( '-w', '--card-width', action='store', default=180, help='The width of the cards in pixels.' )
    parser.add_argument( '-e', '--card-height', action='store', default=252, help='The height of the cards in pixels.' )
    parser.add_argument( '-r', '--card-resolution', action='store', default=72, help='The ppi (pixels-per-inch) resolution of images and thus of the generated card images.' )

    parser.add_argument( '-d', '--debug', action='store_true', help='Show debug output' )

    args = parser.parse_args()

    types_folder = os.path.abspath( args.types_folder )
    fonts_folder = os.path.abspath( args.fonts_folder )
    cards_folder = os.path.abspath( args.cards_folder )
    images_folder = os.path.abspath( args.images_folder )
    cardback_file = None if args.cardback_file is None else os.path.abspath( args.cardback_file )

    output_folder = os.path.abspath( args.output_folder )
    
    if os.path.exists( output_folder ) and not os.path.isdir( output_folder ):
        
        print( "Error: Could not write to {} because it exists and is not a directory.".format( output_folder ) )

        exit()

    card_types = parse_types( types_folder, fonts_folder, images_folder, debug=args.debug )
    cards = parse_cards( cards_folder, args.language, card_types, debug=args.debug )

    if not os.path.exists( output_folder ):
        os.mkdir( output_folder )

    print( 'Composing cards...' )

    for card in cards:

        if args.single_card is None or args.single_card == card.name:
            compose_card( 
                card=card,
                card_width=int( args.card_width ),
                card_height=int( args.card_height ),
                output_directory=output_folder,
                debug=args.debug
            )

    if args.single_card is None and not args.skip_pdf:
        generate_printable_pdf( cards=cards, cardback_file=cardback_file, card_ppi=int( args.card_resolution ), output_directory=output_folder, debug=args.debug )


if __name__ == '__main__':
    generate()
