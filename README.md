# Drinking Game

A freely distributed, open-source drinking game loosely based on the 4chan drinking game. 


### Requirements
* Python >3.0

### How to use

1. Install the python packages in the `requirements.txt` file
2. Run the `generate.py` with the required options

```
usage: generate.py [-h] [-l LANG] [-w WIDTH] [--height HEIGHT] [-f FONT]

Generate the drinking game cards.

optional arguments:
  -h, --help            show this help message and exit
  -l LANG, --lang LANG  The language files to use. Default: 'en'
  -w WIDTH, --width WIDTH
                        The width of the generated cards in px. Default: 500
  --height HEIGHT       The height of the generated cards in px. Default: 697
  -f FONT, --font FONT  The font to use for card generation. A corresponding
                        font file must be present in 'assets/fonts'. Default:
                        Planewalker
```


### History

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