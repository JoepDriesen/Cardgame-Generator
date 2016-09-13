import argparse
from generator.parser import parse_types


def generate():
    parser = argparse.ArgumentParser(
            description='Generate game cards.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter )

    parser.add_argument( '-c', '--cards-folder', action='store', default='./assets/cards/', help='The location of the folder containing the xml property files of the game cards to be generated.' )
    parser.add_argument( '-t', '--types-folder', action='store', default='./assets/types/', help='The location of the folder containing the xml property files of the available game card types.' )
    parser.add_argument( '-f', '--fonts-folder', action='store', default='./assets/fonts/', help='The location of the folder containing the font files used in the game cards.' )

    args = parser.parse_args()

    parse_types( args.types_folder, args.fonts_folder )

if __name__ == '__main__':
    generate()
