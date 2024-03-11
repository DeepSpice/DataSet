from pdf2image import convert_from_path

def pdf2png(path, save_path):
    pages = convert_from_path(path, 500)
    n = path.replace('.pdf', '')
    n = n.split("/")[-1]
    for count, page in enumerate(pages):
        page.save(save_path+"/"+ n + ".png", 'PNG')
