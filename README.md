# Card Game Generator

A python program to generate card games. It uses xml templates, images and font files
provided by the user and generates composite PNG images and a ready-to-print PDF containing
all the generated card images.


### Requirements
* Python >3.0

### Usage

* Install the required Python packages  `pip install -r requirements.txt`
* Run the main script with the required options
```
usage: generate.py [-h] [-t TYPES_FOLDER] [-f FONTS_FOLDER] [-c CARDS_FOLDER]
                   [-b CARDBACK_FILE] [-o OUTPUT_FOLDER] [-l LANGUAGE]
                   [-s SINGLE_CARD] [-p] [-r CARD_RESOLUTION] [-d]

Generate game cards.

optional arguments:
  -h, --help            show this help message and exit
  -t TYPES_FOLDER, --types-folder TYPES_FOLDER
                        The location of the folder containing the xml property
                        files of the available game card types. (default:
                        ./assets/types/)
  -f FONTS_FOLDER, --fonts-folder FONTS_FOLDER
                        The location of the folder containing the font files
                        used by the card types. (default: ./assets/fonts/)
  -c CARDS_FOLDER, --cards-folder CARDS_FOLDER
                        The location of the folder containing the xml property
                        files of the game cards to be generated. (default:
                        ./assets/cards/)
  -b CARDBACK_FILE, --cardback_file CARDBACK_FILE
                        If provided, this image will be used as a cardback for
                        the generated cards. (default: None)
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        The location of the folder in which to store generated
                        cards. (default: ./output/)
  -l LANGUAGE, --language LANGUAGE
                        The language to use when generating cards. (default:
                        en)
  -s SINGLE_CARD, --single-card SINGLE_CARD
                        If provided, only the card with this folder name will
                        be generated. Implies --skip-pdf. (default: None)
  -p, --skip-pdf        If provided, no printable pdf containing all the cards
                        will be generated. (default: False)
  -r CARD_RESOLUTION, --card_resolution CARD_RESOLUTION
                        The ppi (pixels-per-inch) resolution of the template
                        images and thus of the generated card images.
                        (default: 72)
  -d, --debug           Show debug output (default: False)
```

### Assets structure

###### Card types

Every generated card must belong to a certain type. Card types define where 
the different card elements (such as text, images, icons) should appear on
the card.

For every card type, the following is required:
* A directory containing:
* A 'props.xml' file, conforming to the template found at 'templates/props.xml'
* A 'template.png' image file. This image will be used as the base of all cards of this type.
All templates used should have equal dimension, or a faulty PDF could be generated.

###### Cards

For each card in your game, the following is required:
* A directory containing:
* A 'language.xml' file, where 'language' is the language used in the file (e.g. en.xml).
This file contains the display values for the fields defined in the card type properties file.

###### Fonts

Any fonts used should be provided in ttf format.

## License
This code is licensed under the [GPL license.](https://raw.githubusercontent.com/Gargamel1989/Drinker/master/LICENSE)


### TODO
* Add an 'images_folder' where images can be put that can be inserted into any card. Put card template.png files here.
* Add local_image field, where the image should be in the folder with the card language files
* Create schema files and possibly schema validation
