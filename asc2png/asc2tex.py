#add remove for not .ASC files
#remove .asc from .tex files
import libraries.lt2circuitikz.lt2ti as asc2tex
import os

os.chdir('../Data')

pathASC = "ascs/"
pathTEX = "texs/"
#Create a dictionary with all the .asc files
filesASC = os.listdir(pathASC)

#Convert each .asc file to .tex format
for k in filesASC:
    a2tobj = asc2tex.lt2circuiTikz()
    a2tobj.readASCFile(pathASC + k)
    #Delete on the name the part that says ".asc"
    if '.asc' in k:
        n = k.replace('.asc', '')
    a2tobj.writeCircuiTikz(pathTEX + n + r'.tex')
