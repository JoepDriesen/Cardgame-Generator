# Card Game Generator

A python program to generate a large range of card games. It uses templates, images and data files
provided by the user and generates PNG images and a ready-to-print PDF


### Requirements
* Python >3.0

### Usage

* Install the required Python packages  `pip install -r requirements.txt`
* Run the main script with the required options
```
usage: generate.py [-h] [-l LANG] [-w WIDTH] [--height HEIGHT] [-f FONT]
                   [-c CARD] [-d] [-b CARDBACK] [-rw REALWIDTH]
                   [-rh REALHEIGHT] [-si] [-sp]

Generate the drinking game cards.

optional arguments:
  -h, --help            show this help message and exit
  -l LANG, --lang LANG  The language files to use. Default: 'en'
  -w WIDTH, --width WIDTH
                        The width of the generated cards in px. Default: 500
  --height HEIGHT       The height of the generated cards in px. Default: 700
  -f FONT, --font FONT  The font to use for card generation. A corresponding
                        font file must be present in 'assets/fonts'. Default:
                        Planewalker
  -c CARD, --card CARD  If this option is provided, only the card with the
                        given name will be generated.
  -d, --debug           If this argument is provided, text fields will be
                        rendered with opaque squares behind them to easy
                        template debugging.
  -b CARDBACK, --cardback CARDBACK
                        Full path to the image to put on the back of the
                        cards. Default: '/home/joep/Documents/Projects/Drinker
                        /assets/backside.png'
  -rw REALWIDTH, --realwidth REALWIDTH
                        The real width in mm of the printable cards. Default:
                        63mm
  -rh REALHEIGHT, --realheight REALHEIGHT
                        The real height in mm of the printable cards. Default:
                        88mm
  -si, --skipimg        If this option is present, the card images will not be
                        rerendered. Beware this can lead to weird errors if
                        images are missing or incomplete.
  -sp, --skippdf        If this option is present, no printable pdf will be
                        generated
```

### Assets structure

###### Card types

There are currently 4 card types (Action, Backstab, Mandatory, Status). To add additional card types to the
game, create a new directory under the `assets/types` directory. This directory should contain the following
files:
* rules.xml - Containing information about the card type, structured like `assets/types/rules.template.xml`
* template.png - The template image for the card type

###### Cards

To add a custom card to the game, make a new directory under the `assets/cards` directory (or any subdirectory).
This directory should contain the following files:
* image.[jpg,png,gif,...] - The graphic to be used for the card
* en/props.xml - Containing information about the card. This file should be put in a directory with the name of
the language used to describe the properties and must be structured like `assets/cards/props.template.xml`

## License
This code is licensed under the [GPL license.](https://raw.githubusercontent.com/Gargamel1989/Drinker/master/LICENSE)

## Donations
As I made this in my spare time for fun and love of booze, donations are not expected but still welcomed.
If you feel like thanking me with money for some reason, you can donate at my BTC address: `1NnDRSfrk1nkHSXvY6GW1fMvsD3BYQisj1`. Thank you very much!
