import os, math
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from generator.utils import get_image_size

def generate_printable_pdf( cards, cardback_file, card_ppi, output_directory, debug=False ):
    
    abs_path = os.path.join( output_directory, 'printable.pdf' )

    c = canvas.Canvas( filename=abs_path, pagesize=A4 )

    page_width_dots, page_height_dots = A4

    pdf_dpi = 72

    card_width_pixels, card_height_pixels = get_image_size( cards[0].image_file )
    card_width_dots = ( card_width_pixels / card_ppi ) * pdf_dpi
    card_height_dots = ( card_height_pixels / card_ppi ) * pdf_dpi

    card_margin_dots = 2

    cards_per_page_width = math.floor( page_width_dots / ( 2 * card_margin_dots + card_width_dots ) )
    cards_per_page_height = math.floor( page_height_dots / ( 2 * card_margin_dots + card_height_dots ) )

    x_offset = ( page_width_dots - ( 2 * card_margin_dots + card_width_dots ) * cards_per_page_width ) / 2
    y_offset = ( page_height_dots - ( 2 * card_margin_dots + card_height_dots ) * cards_per_page_height ) / 2
    
    x_dots = x_offset
    y_dots = y_offset + card_margin_dots

    for card in cards:

        if x_dots + 2 * card_margin_dots + card_width_dots > page_width_dots:

            x_dots = x_offset
            y_dots += card_height_dots + 2 * card_margin_dots

        if y_dots + 2 * card_margin_dots + card_height_dots > page_height_dots:

            x_dots, y_dots = x_offset, y_offset + card_margin_dots

            c.showPage()

            if cardback_file is not None:

                for i in range( cards_per_page_height ):

                    for j in range( cards_per_page_width ):

                        c.drawInlineImage( 
                            cardback_file, 
                            x_offset + card_margin_dots + j * ( 2 * card_margin_dots + card_width_dots ), 
                            y_offset + card_margin_dots + i * ( 2 * card_margin_dots + card_height_dots ), 
                            width=card_width_dots, 
                            height=card_height_dots 
                        )

                c.showPage()


            
        x_dots += card_margin_dots

        c.drawInlineImage( card.image_file, x_dots, y_dots, width=card_width_dots, height=card_height_dots )

        x_dots += card_width_dots + card_margin_dots

    c.showPage()
    c.save()
