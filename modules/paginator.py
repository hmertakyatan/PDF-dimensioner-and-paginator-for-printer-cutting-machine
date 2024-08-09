import math
from utils import dimension_converters as converter
from modules import page_info_service as pageinfo
import pymupdf
MINIMUM_MARGIN = converter.mm_to_pt(1.5) #MM
def paginate_labels_same_dimension(input_pdf_path, output_page_width_mm, output_page_height_mm):
    
    output_page_width_pts = converter.mm_to_pt(output_page_width_mm)
    output_page_height_pts = converter.mm_to_pt(output_page_height_mm)
    input_page_rects = pageinfo.get_page_rect(input_pdf_path, 0)

    input_doc = pymupdf.open(input_pdf_path)
    output_doc = pymupdf.open()

    rows = int(output_page_height_pts // input_page_rects.height)
    columns = int(output_page_width_pts // input_page_rects.width)

    if((output_page_height_pts - (input_page_rects.height * rows)) < MINIMUM_MARGIN):
        rows -=1     
    if((output_page_width_pts-(input_page_rects.width * columns)) < MINIMUM_MARGIN):
        columns -=1
   
    labels_quantity = input_doc.page_count
    labels_per_page = rows * columns
    page_quantity = math.ceil(labels_quantity / labels_per_page)
    label_index = 0
    for _ in range(page_quantity):
        output_page = pymupdf.utils.new_page(doc=output_doc, width=output_page_width_pts, height=output_page_height_pts)
        horizontal_margin = (output_page_width_pts - (input_page_rects.width * columns)) / 2
        vertical_margin = (output_page_height_pts - (input_page_rects.height * rows)) / 2

        for row in range(rows):
            for column in range(columns):
                if(label_index < input_doc.page_count):
                    x0 = horizontal_margin + column * input_page_rects.width
                    y0 = vertical_margin + row * input_page_rects.height
                    input_page_coordinate = pymupdf.Rect(x0, y0, x0 + input_page_rects.width, y0 + input_page_rects.height)
                    pymupdf.utils.show_pdf_page(
                        rect=input_page_coordinate,
                        page= output_page,
                        src=input_doc,
                        pno= label_index,
                    )
                    label_index +=1
    return output_doc  
            



    

    