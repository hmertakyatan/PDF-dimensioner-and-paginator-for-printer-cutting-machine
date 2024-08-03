import fitz
from PyPDF2 import PdfReader

def get_outer_bbox(input_pdf_path, page_num):
    doc = fitz.open(input_pdf_path)
    page = doc.load_page(page_num)
    drawings = page.get_drawings()

    # Başlangıç değerleri belirle
    en_soldaki = float('inf')
    en_sagdaki = float('-inf')
    en_yukari = float('inf')
    en_asagi = float('-inf')

    for path in drawings:
        if 'rect' in path:
            rect = fitz.Rect(path['rect'])
            en_soldaki = min(en_soldaki, rect.x0)
            en_sagdaki = max(en_sagdaki, rect.x1)
            en_yukari = min(en_yukari, rect.y0)
            en_asagi = max(en_asagi, rect.y1)

    outer_bbox = fitz.Rect(en_soldaki, en_yukari, en_sagdaki, en_asagi)
    doc.close()
    return outer_bbox

def get_bboxlog_fill_path(input_pdf_path, page_num):
    # PDF dosyasını aç
    doc = fitz.open(input_pdf_path)
    # Belirli sayfayı yükle
    page = doc.load_page(page_num)
    
    # Sayfadaki çizim ve dolgu yollarını al
    bboxes = page.get_bboxlog()
    
    # Başlangıç değerleri belirle
    en_soldaki = float('inf')
    en_sagdaki = float('-inf')
    en_yukari = float('inf')
    en_asagi = float('-inf')
    
    # Bbox'ları döngüyle işle ve fill-path olanları seç
    for bbox in bboxes:
        bbox_type, (x0, y0, x1, y1) = bbox
        if bbox_type == "stroke-path":
            en_soldaki = min(en_soldaki, x0)
            en_sagdaki = max(en_sagdaki, x1)
            en_yukari = min(en_yukari, y0)
            en_asagi = max(en_asagi, y1)

    # PDF dosyasını kapat
    doc.close()

    # Bulunan sınırları içeren bir dikdörtgen oluştur
    if en_soldaki == float('inf'):
        # Eğer hiçbir fill-path bulunmadıysa, tüm sayfanın bbox'unu döndür
        return page.rect
    else:
        return fitz.Rect(en_soldaki, en_yukari, en_sagdaki, en_asagi)

def get_bboxlog_stroke_path(input_pdf_path, page_num):
    # PDF dosyasını aç
    doc = fitz.open(input_pdf_path)
    # Belirli sayfayı yükle
    page = doc.load_page(page_num)
    
    # Sayfadaki çizim ve dolgu yollarını al
    bboxes = page.get_bboxlog()
    
    # Başlangıç değerleri belirle
    en_soldaki = float('inf')
    en_sagdaki = float('-inf')
    en_yukari = float('inf')
    en_asagi = float('-inf')
    
    # Bbox'ları döngüyle işle ve fill-path olanları seç
    for bbox in bboxes:
        bbox_type, (x0, y0, x1, y1) = bbox
        if bbox_type == "stroke-path":
            en_soldaki = min(en_soldaki, x0)
            en_sagdaki = max(en_sagdaki, x1)
            en_yukari = min(en_yukari, y0)
            en_asagi = max(en_asagi, y1)

    # PDF dosyasını kapat
    doc.close()

    # Bulunan sınırları içeren bir dikdörtgen oluştur
    if en_soldaki == float('inf'):
        # Eğer hiçbir fill-path bulunmadıysa, tüm sayfanın bbox'unu döndür
        return page.rect
    else:
        return fitz.Rect(en_soldaki, en_yukari, en_sagdaki, en_asagi)

def get_page_width_and_height(input_pdf_path, page_num):
    reader = PdfReader(input_pdf_path)
    page = reader.pages[page_num]
    
    return page.mediabox.width, page.mediabox.height
    
        
