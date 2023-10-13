import lt2circuitikz.lt2ti as asc2tex
import os

carpeta = "../data_generator/ascs"
archivos = os.listdir(carpeta)

#archivos_tex = []
#archivos_tex = archivos_tex.append([x for x in archivos if x.endswith('.tex')])
archivos_tex = [x for x in archivos if x.endswith('.asc')]
print(archivos_tex)

for k in archivos_tex:
    a2tobj = asc2tex.lt2circuiTikz()
    ruta = "../data_generator/ascs/"+k
    a2tobj.readASCFile(ruta)
    a2tobj.writeCircuiTikz(k+r'.tex')

'''a2tobj = asc2tex.lt2circuiTikz()
a2tobj.readASCFile("..\data_generator\ascs\Prueba.asc")
a2tobj.writeCircuiTikz("pruebaa"+'.tex')'''
