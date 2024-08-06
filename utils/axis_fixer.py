import pymupdf
def convert_y_coordinate_pymupdf_to_pypdf(rect, page_height_pts):
    temp = page_height_pts - rect.y1
    rect.y1 = page_height_pts - rect.y0
    rect.y0 = temp
    return rect
