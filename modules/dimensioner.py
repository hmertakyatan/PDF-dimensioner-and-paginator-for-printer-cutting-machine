from PyPDF2 import PdfReader, PdfWriter, Transformation, PageObject
from PyPDF2.generic import RectangleObject
from modules import page_info_service as pageinfo
from utils import dimension_converters as converter
from utils import axis_fixer

def scale_page_content(input_pdf_path, new_width_mm, new_height_mm, quantity):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    new_width_pts = converter.mm_to_pt(new_width_mm)
    new_height_pts = converter.mm_to_pt(new_height_mm)
    
    scaled_pages = []

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        #Get page values values
        bbox_rect_info = pageinfo.get_bbox(input_pdf_path, page_num)
        
        #WARNING!!: pypdf and pymupdf coordinate systems are different. Therefore we make adjustments on the y-axis
        bbox = axis_fixer.convert_y_coordinate_pymupdf_to_pypdf(rect = bbox_rect_info, page_height_pts= page.mediabox.height)
        print(f"Bounding Box Coordinates: x0 : {bbox.x0}, y0: {bbox.y0}, x1: {bbox.x1}, y1: {bbox.y1}")
        print(f" Bounding Box Width (mm): {converter.pt_to_mm(bbox.width)}, Input Bounding Box Height (mm): {converter.pt_to_mm(bbox.height)}")
        print(f" Input Page Width (mm): {converter.pt_to_mm(page.mediabox.width)}, Input Page Height (mm): {converter.pt_to_mm(page.mediabox.height)}")
        #Page types :
        # f -> no border width only label with backgroundcolor.
        # s -> no border and no label just drawings
        # fs -> border and label

        page_type = pageinfo.get_type_from_bboxlog(input_pdf_path,page_num)
        print("Page Type: " + page_type)
        new_page = PageObject().create_blank_page(width=page.mediabox.width, height=page.mediabox.height)
        new_page.merge_page(page)
        #Using stroke path rect for positioning, because its include with borders
        translate_x = -1 * bbox.x0
        translate_y = -1 * bbox.y0
        op = Transformation().translate(tx=translate_x, ty=translate_y)
        new_page.add_transformation(op)
        bbox_width = bbox.width
        bbox_height = bbox.height
        
        if(bbox.width > page.mediabox.width):
            bbox_width = page.mediabox.width
        if(bbox.height > page.mediabox.height):
            bbox_height = page.mediabox.height

        scale_width_factor = new_width_pts / bbox_width
        scale_height_factor = new_height_pts / bbox_height
        new_page.scale(scale_width_factor, scale_height_factor)
        new_page.mediabox = RectangleObject((0,0,new_width_pts,new_height_pts))
        scaled_pages.append(new_page)

    for _ in range(quantity):
        for scaled_page in scaled_pages:
            writer.add_page(scaled_page)

    return writer

def save_scaled_pdf(writer, output_pdf_path):
    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)
    return output_pdf_path