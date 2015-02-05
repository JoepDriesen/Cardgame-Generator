'''
Created on Feb 4, 2015

@author: Joep Driesen
'''
import os
from xml.etree import ElementTree


BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
CARD_TYPES_DIR = os.path.join(ASSETS_DIR, 'types')
CARDS_DIR = os.path.join(ASSETS_DIR, 'cards')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
BACKSIDE_FILE = os.path.join(ASSETS_DIR, 'backside.png')

OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
OUTPUT_CARDS_DIR = os.path.join(OUTPUT_DIR, 'cards')
OUTPUT_PRINTABLE_FILE = os.path.join(OUTPUT_DIR, 'printable_cards.pdf')


class CardType(object):
    
    def __init__(self, card_type_dir):
        rules_file = os.path.join(card_type_dir, 'props.xml')
        if not os.path.isfile(rules_file):
            raise FileNotFoundError('props.xml')
                
        self.template_file = os.path.join(card_type_dir, 'template.png')
        if not os.path.isfile(self.template_file):
            raise FileNotFoundError('template.png')
        
        card_type_xml = ElementTree.parse(rules_file).getroot()
        
        name_el = card_type_xml.find('name')
        if name_el is None:
            raise AttributeError('No <name> element was found in props.xml')
        graphic_el = card_type_xml.find('graphic')
        if graphic_el is not None:
            if 'x' not in graphic_el.attrib or 'y' not in graphic_el.attrib or 'w' not in graphic_el.attrib or 'h' not in graphic_el.attrib:
                raise AttributeError('<graphic> element missing a required attribute (x, y, w, h)')
        content_el = card_type_xml.find('content')
        if content_el is None:
            raise AttributeError('No <content> element was found in props.xml')
        for el in content_el:
            if 'x' not in el.attrib or 'x' not in el.attrib or 'x' not in el.attrib:
                raise AttributeError('Content element <{}> missing a required attribute (x, y, w)'.format(el.tag))
        
        self.name = name_el.text.strip()
        if graphic_el:
            self.card_graphic_box = (int(graphic_el.attrib['x']), int(graphic_el.attrib['y']), int(graphic_el.attrib['w']), int(graphic_el.attrib['h']))
        else:
            self.card_graphic_box = None
        
        self.content = {}
        for el in content_el:
            self.content[el.tag] = {key: self.convert(val) for key,val in el.attrib.items()}
        
    def convert(self, val):
        try:
            return int(val)
        except ValueError as e:
            if val.lower() == 'true':
                return True
            elif val.lower() == 'false':
                return False
            raise e
        
    def has_graphic(self):
        return self.card_graphic_box is not None

class Card(object):
    
    def __init__(self, card_dir, lang, card_types):
        self.dir_name = card_dir.split('/')[-1]
        self.lang = lang
        
        props_file = os.path.join(os.path.join(card_dir, lang), 'props.xml')
        if not os.path.isfile(props_file):
            raise FileNotFoundError('props.xml')
        
        self.image_file = None
        for file in os.listdir(card_dir):
            file_name_no_ext = os.path.splitext(file)[0]
            if file_name_no_ext == 'image':
                self.image_file = os.path.join(card_dir, file)
        
        
        card_xml = ElementTree.parse(props_file).getroot()
        
        name_el = card_xml.find('name')
        
        # Error checking
        if name_el is None:
            raise AttributeError('No <name> element was found in props.xml')
        type_el = card_xml.find('type')
        if type_el is None:
            raise AttributeError('No <type> element was found in props.xml')
        
        
        self.name = name_el.text.strip()
        type_name = type_el.text.strip()
        try:
            self.type = card_types[type_name.lower()]
        except KeyError:
            raise AttributeError('The type given for this card (\'{}\') was not found, available choices are \"{}\"'.format(type_name, ', '.join(sorted(card_types.keys()))))
        
        if self.type.has_graphic():
            if self.image_file is None or not os.path.isfile(self.image_file):
                raise FileNotFoundError('image.[png,jpg,gif,...]')
        
        self.other = {}
        for el in card_xml:
            if el.tag in ['name', 'type']:
                continue
            
            self.other[el.tag] = el.text
    
    @property
    def output_file(self):
        return os.path.join(OUTPUT_CARDS_DIR, '{}.png'.format(self.dir_name))
        
    def get_content(self, content_name):
        if content_name == 'name':
            content = self.name
        elif content_name == 'type':
            content = self.type.name
        else:
            content = self.other.get(content_name, None)
        
        if content is None:
            return None
            
        lines = [line.strip() for line in content.split('\n')]
        if len(lines) > 0 and lines[0] == '':
            del lines[0]
        if len(lines) > 0 and lines[-1] == '':
            del lines[-1]
        
        return lines
        
class Font(object):
    
    def __init__(self, name, file, font_size_to_text_height_ratio):
        self.name = name
        self.file = file
        self.font_size_to_text_height_ratio = float(font_size_to_text_height_ratio)
        
def parse_card_types():
    for file in os.listdir(path=CARD_TYPES_DIR):
        abs_path = os.path.join(CARD_TYPES_DIR, file)
        if os.path.isdir(abs_path):
            try:
                yield CardType(card_type_dir=abs_path)
            except FileNotFoundError as e:
                print('Found card type directory \'{}\', but a required file was missing (\'{}\')'.format(file, e.args[0]))
            
    return


def parse_cards(lang, card_types, base_dir=CARDS_DIR):
    for file in os.listdir(path=base_dir):
        abs_path = os.path.join(base_dir, file)
        if os.path.isdir(abs_path):
            try:
                yield Card(card_dir=abs_path, lang=lang, card_types=card_types)
            except (FileNotFoundError, NotADirectoryError):
                for card in parse_cards(lang, card_types, base_dir=abs_path):
                    yield card
    
    return


def get_font_file(font_name):
    """
    Searches the local assets/fonts directory for a font with the given
    name (extensions are omitted.
    If the font is not found here, it is assumed to be a system font. If
    it is not present as a system font, the default system font will be 
    used instead.
    
    """
    for file in os.listdir(path=FONTS_DIR):
        if font_name == os.path.splitext(file)[0]:
            return os.path.join(FONTS_DIR, file)
        
    return font_name

def parse_fonts():
    font_props_file = os.path.join(FONTS_DIR, 'fonts.xml')
    if not os.path.isfile(font_props_file):
        raise FileNotFoundError('\'assets/fonts/fonts.xml\' was not found. This file is required.')
    
    fonts_xml = ElementTree.parse(font_props_file)
    fonts = {}
    for font_xml in fonts_xml.findall('font'):
        if not 'name' in font_xml.attrib:
            raise AttributeError('Font without name found in \'fonts.xml\', this property is required.')
        name = font_xml.attrib['name']
        if not 'sizeToHeightRatio' in font_xml.attrib:
            fsttr = 1
        else:
            fsttr = font_xml.attrib['sizeToHeightRatio']
        
        fonts[name.lower()] = Font(name=name,
                                   file=get_font_file(name),
                                   font_size_to_text_height_ratio=fsttr)
        
    return fonts

_FONTS = parse_fonts()

def get_font(font_name):
    try:
        return _FONTS[font_name.lower()]
    except KeyError:
        raise Exception('Font \'{}\' not found, make sure it is defined in \'assets/fonts/fonts.xml\'.'.format(font_name))