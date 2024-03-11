import subprocess
import os
import shutil

def tex2pdf(path, out_path):
    # Change the current working
    os.chdir('./Data/temp/tex')

    file = path.split("/")[-1]
    code = 'pdflatex ' + file

    # Ejecutar el comando en un proceso Popen para redirigir la salida
    process = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Esperar a que termine el proceso y obtener la salida
    output, _ = process.communicate()
    # Imprimir la salida del proceso
    #print(output)

    #Change to the original folder
    os.chdir('../../..')

    name = path.replace('.tex', '')
    # Move the .pdf file to the "pdf" folder
    shutil.move(name + '.pdf', out_path)
    #Delete unneeded files
    os.remove(name + '.log')
    os.remove(name + '.aux')
