from PyPDF2 import PdfReader, PdfWriter, Transformation, PageObject
from PyPDF2.generic import RectangleObject
from modules import page_info_service as pageinfo
from utils import dimension_converters as converter

def scale_page_content(input_pdf_path, new_width_mm, new_height_mm, quantity):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    new_width_pts = converter.mm_to_pt(new_width_mm)
    new_height_pts = converter.mm_to_pt(new_height_mm)
    
    scaled_pages = []

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        #Get bounding box coordinates of given page.
        outer_bbox = pageinfo.get_outer_bbox(input_pdf_path, page_num)
        bboxlog = pageinfo.get_bboxlog_stroke_path(input_pdf_path, page_num)
        print(f"BBOXLOG x0 : {bboxlog.x0}, y0: {bboxlog.y0}, x1: {bboxlog.x1}, y1: {bboxlog.y1}")
        print(f"x0 : {outer_bbox.x0}, y0: {outer_bbox.y0}, x1: {outer_bbox.x1}, y1: {outer_bbox.y1}")
        print(f" Input Page Width (mm): {converter.pt_to_mm(page.mediabox.width)}, Input Page Height (mm): {converter.pt_to_mm(page.mediabox.height)}")
        print(f"Input Page Bounding Box Width (mm): {converter.pt_to_mm(outer_bbox.width)}, Input Bounding Box Height (mm): {converter.pt_to_mm(outer_bbox.height)}")
        #New page crated for positioning.
        new_page = PageObject().create_blank_page(width=outer_bbox.width*5, height=outer_bbox.height*5)
        new_page.merge_page(page)
        #Using stroke path rect for positioning, because its include with borders
        translate_x = -1 * bboxlog.x0
        translate_y = -1 * bboxlog.y0
        op = Transformation().translate(tx=translate_x, ty=translate_y)
        new_page.add_transformation(op)
        
        bbox_width = min(page.mediabox.width, outer_bbox.width)
        bbox_height = min(page.mediabox.height, outer_bbox.height)
            
        scale_width_factor = new_width_pts / bbox_width
        scale_height_factor = new_height_pts / bbox_height
        new_page.scale(scale_width_factor, scale_height_factor)
        new_page.mediabox = RectangleObject((0,0, new_width_pts, new_height_pts))


        scaled_pages.append(new_page)

    # Ölçeklenmiş sayfaları quantity kadar yazıcıya ekleyin
    for _ in range(quantity):
        for scaled_page in scaled_pages:
            writer.add_page(scaled_page)

    return writer

def save_scaled_pdf(writer, output_pdf_path):
    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)
    return output_pdf_path