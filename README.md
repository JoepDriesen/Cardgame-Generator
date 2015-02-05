# Drinking Game

A freely distributed, open-source drinking game loosely based on the 4chan drinking game.

Rules are included with the game.

###### Copyright Issues
I am a programmer, not an artist. As a result the artwork used for the card graphics are simple images found
via Google. If your work is used in this game and you would like to have it removed, please contact me and I will fix
this as fast as possible. No copyright infringement is intended.


### Requirements
* Python >3.0

### How to use
The game is distibuted as a collection of art assets and a Python script to assemble the assets into
printable cards.
The cards should be printed and cut (and preferably plastified, as they will get a lot of liquor on them), after
which the game is ready to play.

1. Install the Python packages in the `requirements.txt` file (`pip install -r requirements.txt`)
2. Run the `generate.py` with the required options
3. Output will be found in the directory `output/` in the form of individual card images and a printable pdf document

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

### About

In early 2010, some people on 4chan came up with a drinking game[*](http://knowyourmeme.com/memes/4chan-drinking-game-cards). While
it seemed like a lot of fun, it looked very crappy, was generally only funny to people who were actually on 
4chan and a lot of the cards were just shit. For most people, this made it kind of hard to play with normal
friends, which is obviously the reason for having a drinking game. 

The basics of the game still appeared quite fun, so I set out to make a modified version of the game, more
accessible to the general drinking game public.

Over the years I and a lot of my friends have been playing this game and adjusting it where necessary. In my
opinion it is now one of the best drinking games I have ever played (/personalbias) and would like to share it
with the world.

I have tried to make it as easy as possible to adjust the game to your own needs or add your own cards to it.

Have fun!

## Contributing
Contributions are very welcome! You can contribute in the following ways:
* Fix spelling errors
* Translate cards into different languages
* Propose new cards
* Contribute card graphics (a standard art style for every card instead of stupid google pictures would be awesome)
* Report card balance issues
* Suggest a proper name


##### Assets structure

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

###### New cards
* take 2 votes: wheter the discard pile should be shuffled back into the deck, wether this card should be shuffled back into the deck. Democracy wins.