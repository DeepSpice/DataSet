import subprocess
import os
import shutil

# Change the current working directory to the parent directory
#os.chdir('../Data/texs')

# Create a dictionary with all the .tex files
#filesTEX = os.listdir('./')

#Convert each .asc file to .tex format
#for k in filesTEX:
#    if k!='latex_ext.tex':
#        code = 'pdflatex ' + k
#        # Convert the .tex file to a .pdf file
#        subprocess.run(code, shell=True)
#        name = k.replace('.tex', '')
#        # Move the .pdf file to the "pdfs" folder
#        shutil.move(name + '.pdf', '../pdfs/')
#        #Delete unneeded files
#        os.remove(name + '.log')
#        os.remove(name + '.aux')

#Change to the original folder
#os.chdir('../../asc2png')

def tex2pdf(path, out_path):
    # Change the current working
    os.chdir('./Data/temp/tex')

    file = path.split("/")[-1]
    code = 'pdflatex ' + file
    #run on the cmd
    subprocess.run(code, shell=True)

    #Change to the original folder
    os.chdir('../../../asc2png')

    name = path.replace('.tex', '')
    # Move the .pdf file to the "pdfs" folder
    shutil.move(name + '.pdf', out_path)
    #Delete unneeded files
    os.remove(name + '.log')
    os.remove(name + '.aux')
