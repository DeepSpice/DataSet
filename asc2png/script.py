import lt2circuitikz.lt2ti as asc2tex;
file = r'Prueba.asc';
a2tobj = asc2tex.lt2circuiTikz();
a2tobj.readASCFile(file);
a2tobj.writeCircuiTikz(file+r'.tex');
