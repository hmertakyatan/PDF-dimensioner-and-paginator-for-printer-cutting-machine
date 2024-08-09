from PyPDF2 import PdfReader, PdfWriter, Transformation, PageObject
from PyPDF2.generic import RectangleObject
from modules import page_info_service as pageinfo
from utils import dimension_converters as converter
from utils import axis_fixer
import pymupdf

def scale_page_content(input_pdf_path, new_width_mm, new_height_mm, quantity):
    new_width_pts = converter.mm_to_pt(new_width_mm)
    new_height_pts = converter.mm_to_pt(new_height_mm)
    input_doc = pymupdf.open(input_pdf_path)
    output_doc = pymupdf.open()
    
    for _ in range(quantity):
        for page_num in range(input_doc.page_count):
            bbox_rect = pageinfo.get_bbox(input_doc.load_page(page_num)) 
            output_page =pymupdf.utils.new_page(doc=output_doc,width=new_width_pts, height=new_height_pts)
            pymupdf.utils.show_pdf_page(
                rect=output_page.rect,
                page=output_page,
                src=input_doc,
                pno=page_num,
                keep_proportion=False,
                clip=bbox_rect
            )
    
    return output_doc


        

        
        
        
        
        
        

       
