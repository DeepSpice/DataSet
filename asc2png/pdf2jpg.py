#Based on https://stackoverflow.com/questions/46184239/extract-a-page-from-a-pdf-as-a-jpeg

from pdf2image import convert_from_path

pages = convert_from_path('pdf_file', 500)
for count, page in enumerate(pages):
    page.save(f'out{count}.jpg', 'JPEG')
