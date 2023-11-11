from asc2png.asc2tex import asc2tex
from asc2png.tex2pdf import tex2pdf
from asc2png.pdf2png import pdf2png
import shutil
import os

pathASC = "./Data/ascs/"
pathTEMPtex = "./Data/temp/tex/"
pathTEMPpdf = "./Data/temp/pdf/"
pathPNG = "./Data/pngs"

def create_folder(folder_path):
    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # If not, create it
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

def asc2png(name):
    toTEX = asc2tex(pathASC + name +".asc", pathTEMPtex)
    toPDF = tex2pdf(pathTEMPtex + name + ".tex", pathTEMPpdf)
    toPNG = pdf2png(pathTEMPpdf + name + ".pdf", pathPNG)

    #Delete unneeded files
    os.remove(pathTEMPtex + name + '.tex')
    os.remove(pathTEMPpdf + name + '.pdf')

def convert():
    create_folder(pathTEMPtex)
    create_folder(pathTEMPpdf)
    create_folder(pathPNG)

    #Create a dictionary with all the .asc files
    filesASC = os.listdir(pathASC)

    #Convert each .asc file to .tex format
    for k in filesASC:
        #Delete on the name the part that says ".asc"
        name = k.replace('.asc', '')
        asc2png(name)

    shutil.rmtree("./Data/temp/")
