from asc2tex import asc2tex
from tex2pdf import tex2pdf
from pdf2png import pdf2png
import time
import os

pathASC = "../Data/ascs/"
pathTEMPtex = "../Data/temp/tex/"
pathTEMPpdf = "../Data/temp/pdf/"
pathPNG = "../Data/pngs"

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

os.remove(pathTEMPtex + "latex_ext.tex")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tiempo transcurrido: {elapsed_time} segundos")
