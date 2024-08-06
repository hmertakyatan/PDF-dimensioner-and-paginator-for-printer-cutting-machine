import math
from pypdf import PdfReader, PdfWriter, PageObject
from utils import dimension_converters as converter
from modules import page_info_service as pageinfo

def paginate_labels_same_dimension(input_pdf_path, output_pdf_path, output_page_width_mm, output_page_height_mm):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    output_page_width_pts = converter.mm_to_pt(output_page_width_mm)
    output_page_height_pts = converter.mm_to_pt(output_page_height_mm)
    page_widht, page_heigth = pageinfo.get_page_width_and_height(input_pdf_path, 0)
    rows = int(output_page_height_pts // page_heigth)
    columns = int(output_page_width_pts // page_widht)
    labels_per_page = rows * columns
    num_labels = len(reader.pages)
    num_pages = math.ceil(num_labels / labels_per_page)
    label_index = 0
    i = 0
    

    for _ in range(num_pages):
        new_pdf_page = PageObject.create_blank_page(width=output_page_width_pts, height=output_page_height_pts)
        print("Blank page created.")
        
        horizontal_margin = (output_page_width_pts - (columns * page_widht)) / 2
        print(f"Horizontal margin: {converter.pt_to_mm(horizontal_margin)}") 
        vertical_margin = (output_page_height_pts - (rows * page_heigth)) / 2
        print(f"Vertical margin: {converter.pt_to_mm(vertical_margin)}")
        for row in range(rows):
            for column in range(columns):
                if label_index < num_labels:
                    label_page = reader.pages[label_index]
                    x_position = horizontal_margin + column * page_widht
                    y_position = vertical_margin + (rows - row - 1) * page_heigth
                    temp_page = PageObject.create_blank_page(width=output_page_width_pts, height=output_page_height_pts)
                    temp_page.merge_translated_page(label_page, tx=x_position  , ty=y_position)
                    new_pdf_page.merge_page(temp_page)
                  
                    label_index += 1
        writer.add_page(new_pdf_page)
        i += 1
        print(i, ".page done.")

    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)