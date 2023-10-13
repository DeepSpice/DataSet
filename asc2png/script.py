#add remove for not .ASC files
#remove .asc from .tex files
import libraries.lt2circuitikz.lt2ti as asc2tex
import os

pathASC = "../data_generator/ascs"
pathTEX = "../data_generator/texs"
filesASC = os.listdir(pathASC)

#filesASC = [x for x in files if x.endswith('.asc')]

for k in filesASC:
    a2tobj = asc2tex.lt2circuiTikz()
    a2tobj.readASCFile(pathASC + "/" + k)
    a2tobj.writeCircuiTikz(pathTEX + "/" + k + r'.tex')
