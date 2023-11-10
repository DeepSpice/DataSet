#Based on https://stackoverflow.com/questions/46184239/extract-a-page-from-a-pdf-as-a-jpeg

from pdf2image import convert_from_path

# Create a function that transform a masive amount of pdf files into jpg files

def pdf2png(path, save_path):
    pages = convert_from_path(path, 500)
    n = path.replace('.pdf', '')
    n = n.split("/")[-1]
    for count, page in enumerate(pages):
        page.save(save_path+"/"+ n + ".png", 'PNG')
#    return print('Done')

#pdf2png("../Data/temp/pdf/Prueba.pdf", "../Data/pngs")
