import argparse, os, random
from generator.parser import parse_types, parse_cards
from generator.utils import get_image_size
from PIL import Image


def generate():
    parser = argparse.ArgumentParser(
            description='Generate game cards.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter )

    parser.add_argument( '-t', '--types-folder', action='store', default='./assets/types/', help='The location of the folder containing the xml property files of the available game card types.' )
    parser.add_argument( '-f', '--fonts-folder', action='store', default='./assets/fonts/', help='The location of the folder containing the font files used by the card types.' )
    parser.add_argument( '-c', '--cards-folder', action='store', default='./assets/cards/', help='The location of the folder containing the xml property files of the game cards to be generated.' )
    parser.add_argument( '-o', '--output-folder', action='store', default='./output/', help='The location of the folder in which to store generated cards.' )
    parser.add_argument( '-l', '--language', action='store', default='en', help='The language to use when generating cards.' )

    parser.add_argument( '-r', '--rows', action='store', default=3, help='The amount of card rows in the preview image. Minimum 1.' )
    parser.add_argument( '-m', '--columns', action='store', default=10, help='The amount of columns in the preview image. Minimum 1.' )

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

    for card in cards:
        card.image_file = os.path.join( output_folder, '{}.png'.format( card.name ) )

    if not os.path.exists( output_folder ):
        os.mkdir( output_folder )

    print( 'Creating preview image...' )

    image_width, image_height = get_image_size( cards[0].image_file )

    columns = max( 1, int( args.columns ) )
    rows = max( 1, int( args.rows ) )

    output_file = os.path.join( output_folder, 'preview.png' )
    im = Image.new( 'RGB', ( image_width * columns, image_height * rows ) )

    i, j = 0, 0
    random.shuffle( cards )
    for card in cards:

        if i >= columns:
            i = 0
            j += 1

        if j >= rows:
            break

        # Add card image file
        card_im = Image.open( card.image_file )
        im.paste( card_im, ( i * image_width, j * image_height ) )

        if args.debug:
            print( '    Pasted image {}'.format( j * columns + i + 1 ) )

        i += 1

    im.save( output_file )


if __name__ == '__main__':
    generate()
