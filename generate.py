#!/usr/bin/env python
''' 
Created on Feb 4, 2015

@author: Joep Driesen
'''
import argparse, os
from generator.files import set_paths, parse_card_types, parse_cards, get_font
from generator.assemble import assemble_card
from generator.printable import PrintableCardsPDF

DEFAULT_LANG = 'en'
DEFAULT_WIDTH = 500  # px
DEFAULT_REAL_WIDTH = 63 # mm
DEFAULT_HEIGHT = 700 # px
DEFAULT_REAL_HEIGHT = 88 # mm
DEFAULT_FONT = 'Planewalker'
DEFAULT_FONTSIZE = 20

def generate():
    parser = argparse.ArgumentParser(description='Generate the drinking game cards.')
    parser.add_argument('-l', '--lang', action='store', default=DEFAULT_LANG, help='The language files to use. Default: \'{}\''.format(DEFAULT_LANG))
    parser.add_argument('-w', '--width', action='store', type=int, default=DEFAULT_WIDTH, help='The width of the generated cards in px. Default: {}'.format(DEFAULT_WIDTH))
    parser.add_argument('--height', action='store', type=int, default=DEFAULT_HEIGHT, help='The height of the generated cards in px. Default: {}'.format(DEFAULT_HEIGHT))
    parser.add_argument('-f', '--font', action='store', default=DEFAULT_FONT, help='The font to use for card generation. A corresponding font file must be present in \'assets/fonts\'. Default: {}'.format(DEFAULT_FONT))
    parser.add_argument('-c', '--card', action='store', default=None, help='If this option is provided, only the card with the given name will be generated.')
    parser.add_argument('-d', '--debug', action='store_true', help='If this argument is provided, text fields will be rendered with opaque squares behind them to easy template debugging.')
    parser.add_argument('-rw', '--realwidth', action='store', default=DEFAULT_REAL_WIDTH, help='The real width in mm of the printable cards. Default: {}mm'.format(DEFAULT_REAL_WIDTH))
    parser.add_argument('-rh', '--realheight', action='store', default=DEFAULT_REAL_HEIGHT, help='The real height in mm of the printable cards. Default: {}mm'.format(DEFAULT_REAL_HEIGHT))
    parser.add_argument('-si', '--skipimg', action='store_true', help='If this option is present, the card images will not be rerendered. Beware this can lead to weird errors if images are missing or incomplete.')
    parser.add_argument('-sp', '--skippdf', action='store_true', help='If this option is present, no printable pdf will be generated')
    parser.add_argument('-a', '--asset_folder', action='store', default=None, help='The location of the folder containing the assets to use for generating the card game. If omitted, the current working directory will be searched for a folder with the name `assets`')
    args = parser.parse_args()

    if args.asset_folder is None:
        assets_dir = os.path.join(os.getcwd(), 'assets')

    else:
        assets_dir = os.path.abspath(args.asset_folder)

    if not os.path.isdir(assets_dir):
        print('ERROR: Directory `{}` does not exist, exiting...'.format(assets_dir))
        exit(1)

    set_paths(assets_dir, os.getcwd())

    card_types = {card_type.name.lower(): card_type for card_type in parse_card_types()}
    
    cards_generated = {}
    cards = []
    for card in parse_cards(card_types=card_types, lang=args.lang):
        if args.card is None or card.name.lower() == args.card.lower():
            if not args.skipimg:
                assemble_card(card, card_width=args.width, card_height=args.height, font=get_font(args.font), debug=args.debug)
            cards_generated[card.type.name] = cards_generated.get(card.type.name, 0) + 1
            cards.append(card)
    
    # Display the statistics on generated cards
    print('Cards generated:\n')
    for generated_type in sorted(cards_generated.keys()):
        print('{:15s} {:>3}'.format(generated_type, cards_generated[generated_type]))
    
    if len(cards_generated) <= 0:
        print('None')
    else:
        print('-'*20)
        print('{:15s} {:>3}'.format('Total', sum(cards_generated.values())))
    
    if not args.skippdf:
        if len(cards_generated) > 0:
            from generator.files import BACKSIDE_FILE, OUTPUT_PRINTABLE_FILE

            print('\nGenerating printable pdf, this may take a while...')
            pdf = PrintableCardsPDF(cards=cards, backsides_image=BACKSIDE_FILE, real_width=args.realwidth, real_height=args.realheight)
            pdf.render()
            pdf.output(name=OUTPUT_PRINTABLE_FILE, dest='F')
        else:
            print('\nNo cards generating, skipping pdf output.')
        
    print('Done')
    
if __name__ == '__main__':
    generate()
