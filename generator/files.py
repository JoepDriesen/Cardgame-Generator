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

OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
OUTPUT_CARDS_DIR = os.path.join(OUTPUT_DIR, 'cards')


class CardType(object):
    
    name = None
    rules = None
    
    template_file = None
    card_title_box = None
    card_graphic_box = None
    card_rules_box = None
    
    def __init__(self, card_type_dir):
        rules_file = os.path.join(card_type_dir, 'rules.xml')
        if not os.path.isfile(rules_file):
            raise FileNotFoundError('rules.xml')
                
        self.template_file = os.path.join(card_type_dir, 'template.png')
        if not os.path.isfile(self.template_file):
            raise FileNotFoundError('template.png')
        
        card_type_xml = ElementTree.parse(rules_file).getroot()
        
        name_el = card_type_xml.find('name')
        if name_el is None:
            raise AttributeError('No <name> element was found in rules.xml')
        self.name = name_el.text.strip()
        
        rules_el = card_type_xml.find('rules')
        if rules_el is None:
            raise AttributeError('No <rules> element was found in rules.xml')
        self.rules = rules_el.text
        
        tb = card_type_xml.find('titleBox')
        if tb is None:
            raise AttributeError('No <titleBox> element was found in rules.xml')
        self.card_title_box = (int(tb.attrib['left']), int(tb.attrib['top']), int(tb.attrib['width']), int(tb.attrib['height']))
        gb = card_type_xml.find('graphicBox')
        if gb is None:
            raise AttributeError('No <graphicBox> element was found in rules.xml')
        self.card_graphic_box = (int(gb.attrib['left']), int(gb.attrib['top']), int(gb.attrib['width']), int(gb.attrib['height']))
        rb = card_type_xml.find('rulesBox')
        if rb is None:
            raise AttributeError('No <rulesBox> element was found in rules.xml')
        self.card_rules_box = (int(rb.attrib['left']), int(rb.attrib['top']), int(rb.attrib['width']), int(rb.attrib['height']))


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
                
        if self.image_file is None or not os.path.isfile(self.image_file):
            raise FileNotFoundError('image.[png,jpg,gif,...]')
        
        
        card_xml = ElementTree.parse(props_file).getroot()
        
        name_el = card_xml.find('name')
        if name_el is None:
            raise AttributeError('No <name> element was found in rules.xml')
        self.name = name_el.text.strip()
        
        type_el = card_xml.find('type')
        if type_el is None:
            raise AttributeError('No <type> element was found in rules.xml')
        type_name = type_el.text.strip()
        try:
            self.type = card_types[type_name.lower()]
        except KeyError:
            raise AttributeError('The type given for this card (\'{}\') was not found, available choices are \"{}\"'.format(type_name, ', '.join(sorted(card_types.keys()))))
        
        rules_el = card_xml.find('rules')
        if rules_el is None:
            raise AttributeError('No <rules> element was found in rules.xml')
        self._rules = rules_el.text
    
    @property
    def rules(self):
        return '\n'.join(self.rule_lines)
    
    @property
    def rule_lines(self):
        rule_lines = [line.strip() for line in self._rules.split('\n')]
        if len(rule_lines) > 0 and rule_lines[0] == '':
            del rule_lines[0]
        if len(rule_lines) > 0 and rule_lines[-1] == '':
            del rule_lines[-1]
        return rule_lines
        
class Font(object):
    
    def __init__(self, name, file, 
                 title_font_size, title_text_height,
                 rules_font_size, rules_text_height):
        self.name = name
        self.file = file
        
        self.title_font_size = title_font_size
        self.title_text_height = title_text_height
        
        self.rules_font_size = rules_font_size
        self.rules_text_height = rules_text_height
        
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
        
        title_el = font_xml.find('title')
        if title_el is None:
            raise AttributeError('Font \'{}\' does not have a title element, this element is required'.format(name))
        if 'size' not in title_el.attrib or 'height' not in title_el.attrib:
            raise AttributeError('Font \'{}\': title element does not have all required attributes (size, height)'.format(name))
        
        rules_el = font_xml.find('rules')
        if rules_el is None:
            raise AttributeError('Font \'{}\' does not have a rules element, this element is required'.format(name))
        if 'size' not in rules_el.attrib or 'height' not in rules_el.attrib:
            raise AttributeError('Font \'{}\': rules element does not have all required attributes (size, height)'.format(name))
        
        fonts[name.lower()] = Font(name=name,
                                   file=get_font_file(name),
                                   title_font_size=int(title_el.attrib['size']),
                                   title_text_height=int(title_el.attrib['height']),
                                   rules_font_size=int(rules_el.attrib['size']),
                                   rules_text_height=int(rules_el.attrib['height']))
        
    return fonts

_FONTS = parse_fonts()

def get_font(font_name):
    try:
        return _FONTS[font_name.lower()]
    except KeyError:
        raise Exception('Font \'{}\' not found, make sure it is defined in \'assets/fonts/fonts.xml\'.'.format(font_name))