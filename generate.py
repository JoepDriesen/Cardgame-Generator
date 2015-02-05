#!/usr/bin/env python
''' 
Created on Feb 4, 2015

@author: Joep Driesen
'''
import argparse
from generator.files import parse_card_types, parse_cards, get_font
from generator.assemble import assemble_card

DEFAULT_LANG = 'en'
DEFAULT_WIDTH = 500  # px
DEFAULT_HEIGHT = 697 # px
DEFAULT_FONT = 'Planewalker'
DEFAULT_FONTSIZE = 20

def generate():
    parser = argparse.ArgumentParser(description='Generate the drinking game cards.')
    parser.add_argument('-l', '--lang', action='store', default=DEFAULT_LANG, help='The language files to use. Default: \'{}\''.format(DEFAULT_LANG))
    parser.add_argument('-w', '--width', action='store', type=int, default=DEFAULT_WIDTH, help='The width of the generated cards in px. Default: {}'.format(DEFAULT_WIDTH))
    parser.add_argument('--height', action='store', type=int, default=DEFAULT_HEIGHT, help='The height of the generated cards in px. Default: {}'.format(DEFAULT_HEIGHT))
    parser.add_argument('-f', '--font', action='store', default=DEFAULT_FONT, help='The font to use for card generation. A corresponding font file must be present in \'assets/fonts\'. Default: {}'.format(DEFAULT_FONT))
    parser.add_argument('-c', '--card', action='store', default=None, help='If this option is provided, only the card with the given name will be generated.')
    args = parser.parse_args()
    
    card_types = {card_type.name.lower(): card_type for card_type in parse_card_types()}
    
    cards_generated = {}
    for card in parse_cards(card_types=card_types, lang=args.lang):
        if args.card is None or card.name.lower() == args.card.lower():
            assemble_card(card, card_width=args.width, card_height=args.height, font=get_font(args.font))
            cards_generated[card.type.name] = cards_generated.get(card.type.name, 0) + 1
    
    # Display the statistics on generated cards
    print('Cards generated:\n')
    for generated_type in sorted(cards_generated.keys()):
        print('{:15s} {:>3}'.format(generated_type, cards_generated[generated_type]))
    
    if len(cards_generated) <= 0:
        print('None')
    else:
        print('-'*20)
        print('{:15s} {:>3}'.format('Total', sum(cards_generated.values())))
if __name__ == '__main__':
    generate()