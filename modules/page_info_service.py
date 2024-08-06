import pymupdf
from PyPDF2 import PdfReader

def get_bbox(input_pdf_path, page_num):
    doc = pymupdf.open(input_pdf_path)
    page = doc.load_page(page_num)
    drawings = page.get_drawings()
    if not drawings:
        return None

    first_rect = drawings[0]['rect']
    x0_min = first_rect.x0
    y0_min = first_rect.y0
    x1_max = first_rect.x1
    y1_max = first_rect.y1


    for drawing in drawings:
        rect = drawing['rect']
        x0_min = min(x0_min, rect.x0)
        y0_min = min(y0_min, rect.y0)
        x1_max = max(x1_max, rect.x1)
        y1_max = max(y1_max, rect.y1)

    bbox_rect = pymupdf.Rect(x0_min, y0_min, x1_max, y1_max)

    doc.close()
    return bbox_rect

def get_stroke_line_width(input_pdf_path,page_num):
    doc = pymupdf.open(input_pdf_path)

    page = doc.load_page(page_num)

    drawings = page.get_drawings()
    
    if drawings:
        stroke_line_width = drawings[0]['width']
    else:
        stroke_line_width = None  # Eğer çizim yoksa None döndür
    
    return stroke_line_width

def get_type_from_bboxlog(input_pdf_path, page_num):
    doc = pymupdf.open(input_pdf_path)

    page = doc.load_page(page_num)

    drawings = page.get_drawings()
    
    if drawings:
        first_type = drawings[0]['type']
    else:
        first_type = None  # Eğer çizim yoksa None döndür
    
    return first_type
    

def get_stroke_path(input_pdf_path, page_num):
    doc = pymupdf.open(input_pdf_path)
    page = doc.load_page(page_num)
    bboxes = page.get_bboxlog()
    en_soldaki = float('inf')
    en_sagdaki = float('-inf')
    en_yukari = float('inf')
    en_asagi = float('-inf')
    
    for bbox in bboxes:
        bbox_type, (x0, y0, x1, y1) = bbox
        if bbox_type == "stroke-path":
            en_soldaki = min(en_soldaki, x0)
            en_sagdaki = max(en_sagdaki, x1)
            en_yukari = min(en_yukari, y0)
            en_asagi = max(en_asagi, y1)

    doc.close()

    if en_soldaki == float('inf'):
        return page.rect
    else:
        return pymupdf.Rect(en_soldaki, en_yukari, en_sagdaki, en_asagi)

def get_page_width_and_height(input_pdf_path, page_num):
    reader = PdfReader(input_pdf_path)
    page = reader.pages[page_num]
    
    return page.mediabox.width, page.mediabox.height
    
        
