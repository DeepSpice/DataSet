import asc2png.libraries.lt2circuitikz.lt2ti as circuitikz
import os

def asc2tex(path, out_path):
    print("----------------------------------------------------------")
    print(path)
    print(out_path)
    print("----------------------------------------------------------")
    a2tobj = circuitikz.lt2circuiTikz()
    a2tobj.readASCFile(path)
    #Delete on the name the part that says ".asc"
    n = path.replace('.asc', '')
    n = n.split("/")[-1]

    a2tobj.writeCircuiTikz(out_path + "/" + n + r'.tex')

if __name__ == "__main__":
    asc2tex("./data", "./data2")