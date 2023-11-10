from asc2tex import asc2tex
from tex2pdf import tex2pdf
from pdf2png import pdf2png
import time
import shutil
import os

pathASC = "../Data/ascs/"
pathTEMPtex = "../Data/temp/tex/"
pathTEMPpdf = "../Data/temp/pdf/"
pathPNG = "../Data/pngs"

def create_folder(folder_path):
    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # If not, create it
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

create_folder(pathASC)
create_folder(pathTEMPtex)
create_folder(pathTEMPpdf)
create_folder(pathPNG)

def asc2png(name):
    toTEX = asc2tex(pathASC + name +".asc", pathTEMPtex)
    toPDF = tex2pdf(pathTEMPtex + name + ".tex", pathTEMPpdf)
    toPNG = pdf2png(pathTEMPpdf + name + ".pdf", pathPNG)

    #Delete unneeded files
    os.remove(pathTEMPtex + name + '.tex')
    os.remove(pathTEMPpdf + name + '.pdf')


start_time = time.time()

#Create a dictionary with all the .asc files
filesASC = os.listdir(pathASC)

#Convert each .asc file to .tex format
for k in filesASC:
#    #Delete on the name the part that says ".asc"
    name = k.replace('.asc', '')
    asc2png(name)

# os.remove(pathTEMPtex + "latex_ext.tex")

shutil.rmtree("../Data/temp/")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tiempo transcurrido: {elapsed_time} segundos")