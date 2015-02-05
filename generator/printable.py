'''
Created on Feb 5, 2015

@author: Joep Driesen
'''
from fpdf.fpdf import FPDF

class PrintableCardsPDF(FPDF):
    
    def __init__(self, cards, backsides_image, real_width, real_height):
        super(PrintableCardsPDF, self).__init__(orientation='p', format='A4')
        self.cards = cards
        self.backsides_image = backsides_image
        self.real_width = real_width
        self.real_height = real_height
        
    def render(self):
        self.add_page()
        pw = self.w
        ph = self.h
        self.cards_per_width = int(pw // self.real_width)
        self.cards_per_height = int(ph // self.real_height)
        
        total_space_width = pw % self.real_width
        total_space_height = ph % self.real_height
        
        self.margins_width = total_space_width / (self.cards_per_width + 1)
        self.margins_height = total_space_height / (self.cards_per_height + 1)
        
        cards_on_row = -1
        cards_on_col = 0
        for card in self.cards:
            cards_on_row += 1
            if cards_on_row >= self.cards_per_width:
                cards_on_col += 1
                cards_on_row = 0
                if cards_on_col >= self.cards_per_height:
                    self.add_backsides_page(ao_cards=self.cards_per_width*self.cards_per_height)
                    self.add_page()
                    cards_on_col = 0
            
            self.image(card.output_file,
                       x=(self.margins_width * (cards_on_row + 1)) + (self.real_width * cards_on_row), 
                       y=(self.margins_height * (cards_on_col + 1)) + (self.real_height * cards_on_col), 
                       w=self.real_width, h=self.real_height)
        self.add_backsides_page(ao_cards=((cards_on_col * self.cards_per_width) + cards_on_row + 1))
        
    def add_backsides_page(self, ao_cards):
        self.add_page()
        
        cards_on_row = -1
        cards_on_col = 0
        for _ in range(ao_cards):
            cards_on_row += 1
            if cards_on_row >= self.cards_per_width:
                cards_on_col += 1
                cards_on_row = 0
                if cards_on_col >= self.cards_per_height:
                    cards_on_col = 0
            
            self.image(self.backsides_image, 
                       x=(self.margins_width * (cards_on_row + 1)) + (self.real_width * cards_on_row), 
                       y=(self.margins_height * (cards_on_col + 1)) + (self.real_height * cards_on_col), 
                       w=self.real_width, h=self.real_height)