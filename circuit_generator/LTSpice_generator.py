import re
import numpy as np

class schematicAscGenerator:
    def __init__(self):
        self.wires = {}
        self.g = {}
        self.r = {}
        self.c = {}
        self.l = {}
        self.d = {}
        self.v = {}
        self.comp = {}
        self.coords = []

        # File header
        self.asc = "Version 4\nSHEET 1 880 680\n"
    
    def reset(self):
        self.wires = {}
        self.g = {}
        self.r = {}
        self.c = {}
        self.l = {}
        self.d = {}
        self.v = {}
        self.comp = {}
        self.coords = []
        
    def coordsSetter(self, x, y, comp="wire", deg = 0):
        newX = x if x%16 == 0 else round(x/16)*16
        newY = y if y%16 == 0 else round(y/16)*16
        newY = -1*newY

        if comp == "res" or comp == "ind":
            newX = newX-16*np.sign(np.cos(np.deg2rad(deg+1)))
            newY = newY-16*np.sign(np.sin(np.deg2rad(deg+1)))
        if comp == "diode":
            newX = newX-16*round(np.cos(np.deg2rad(deg)))
        if comp == "cap":
            newX = newX-16*round(np.cos(np.deg2rad(deg)))
            newY = newY-16*round(np.sin(np.deg2rad(deg)))
        if comp == "volt":
            newX = newX+16*round(np.sin(np.deg2rad(deg)))
            newY = newY-16*round(np.cos(np.deg2rad(deg)))
        if comp == "curr":
            newX = newX
            newY = newY

        return int(newX), int(newY)
    
    def wire(self, x0, y0, x1, y1):
        #'''
        # x0 = initial position in x
        # y0 = initial position in y
        # x1 = final position in x
        # y1 = final position in y
        # '''
        x0, y0 = self.coordsSetter(x0, y0)
        x1, y1 = self.coordsSetter(x1, y1)

        if (x0 == x1) or (y0 == y1): ### Cable recto
            name = f'W{len(self.wires)}'
            self.wires[name] = f'WIRE {x0} {y0} {x1} {y1}'
        else:
            name = f'W{len(self.wires)}'
            self.wires[name] = f'WIRE {x0} {y0} {x1} {y0}\nWIRE {x1} {y0} {x1} {y1}'
    
    def ground(self, x, y):
        # x = initial position in x
        # y = initial position in y
        x, y = self.coordsSetter(x, y)
        name = f'G{len(self.g)}'
        self.g[name] = f'FLAG {x} {y} 0'
            
    def res(self, x, y, deg, val):
        # x = initial position in x
        # y = initial position in y
        # deg = rotation (0, 90, 270)
        # val = resistance value
        x, y = self.coordsSetter(x, y, "res", deg)
        # Name of resistance is equal to the number of components 
        name = f'R{len(self.r)}'
        # Coords and rotation
        header = f'SYMBOL res {x} {y} R{deg}'
        # Box sizes
        window = ""
        # Resistance name
        nameTag = f'SYMATTR InstName {name}'
        # Resistance value
        valueTag = f'SYMATTR Value {val}'
        # Object with info of resistance
        self.r[name] = {
            "header":header,
            "nameTag":nameTag,
            "valueTag":valueTag
        }

        self.coords.append({
            "start_x": x, 
            "start_y": y, 
            "end_x": x+round(np.sin(np.deg2rad(deg)))*16*5, 
            "end_y": y-round(np.cos(np.deg2rad(deg)))*16*5, 
        })

        # Change window size depends of rotation
        if deg == 90 or deg==270:
            window  = "WINDOW 0 0 56 VBottom 2\nWINDOW 3 32 56 VTop 2" if deg == 90 else "WINDOW 0 32 56 VBottom 2\nWINDOW 3 0 56 VTop 2"
            self.r[name]["window"] = window
            
    def cap(self, x, y, deg, val):
        # x = initial position in x
        # y = initial position in y
        # deg = rotation (0, 90, 270)
        # val = capacitor value
        x, y = self.coordsSetter(x, y, "cap", deg)
        # Name of capacitor is equal to the number of components 
        name = f'C{len(self.c)}'
        # Coords and rotation
        header = f'SYMBOL cap {x} {y} R{deg}'
        # Box sizes
        window = ""
        # Resistance name
        nameTag = f'SYMATTR InstName {name}'
        # Resistance value
        valueTag = f'SYMATTR Value {val}'
        # Object with info of capacitor
        self.c[name] = {
            "header":header,
            "nameTag":nameTag,
            "valueTag":valueTag
        }
        # Change window size depends of rotation
        if deg != 0:
            if deg == 90:
                window  = "WINDOW 0 0 32 VBottom 2\nWINDOW 3 32 32 VTop 2"
            elif deg == 180:
                window  = "WINDOW 0 25 56 VLeft 2\nWINDOW 3 24 8 VLeft 2"
            elif deg == 270:
                window  = "WINDOW 0 32 32 VTop 2\nWINDOW 3 0 32 VBottom 2"
            self.c[name]["window"] = window
        
        self.coords.append({
            "start_x": x, 
            "start_y": y, 
            "end_x": x+round(np.sin(np.deg2rad(deg)))*16*5, 
            "end_y": y-round(np.cos(np.deg2rad(deg)))*16*5, 
        })
            
    def ind(self, x, y, deg, val):
        # x = initial position in x
        # y = initial position in y
        # deg = rotation (0, 90, 270)
        # val = capacitor value
        x, y = self.coordsSetter(x, y, "ind", deg)
        # Name of capacitor is equal to the number of components 
        name = f'L{len(self.l)}'
        # Coords and rotation
        header = f'SYMBOL ind {x} {y} R{deg}'
        # Box sizes
        window = ""
        # Resistance name
        nameTag = f'SYMATTR InstName {name}'
        # Resistance value
        valueTag = f'SYMATTR Value {val}'
        # Object with info of capacitor
        self.l[name] = {
            "header":header,
            "nameTag":nameTag,
            "valueTag":valueTag
        }
        # Change window size depends of rotation
        if deg != 0:
            if deg == 90:
                window  = "WINDOW 0 5 56 VBottom 2\nWINDOW 3 32 56 VTop 2"
            elif deg == 180:
                window  = "WINDOW 0 36 80 VLeft 2\nWINDOW 3 36 40 VLeft 2"
            elif deg == 270:
                window  = "WINDOW 0 32 56 VTop 2\nWINDOW 3 5 56 VBottom 2"
            self.l[name]["window"] = window
        self.coords.append({
            "start_x": x, 
            "start_y": y, 
            "end_x": x+round(np.sin(np.deg2rad(deg)))*16*5, 
            "end_y": y-round(np.cos(np.deg2rad(deg)))*16*5, 
        })
                       
    def diode(self, x, y, deg):
        # x = initial position in x
        # y = initial position in y
        # deg = rotation (0, 90, 270)
        # val = capacitor value
        x, y = self.coordsSetter(x, y, "diode", deg)
        # Name of capacitor is equal to the number of components 
        name = f'D{len(self.d)}'
        # Coords and rotation
        header = f'SYMBOL diode {x} {y} R{deg}'
        # Box sizes
        window = ""
        # Resistance name
        nameTag = f'SYMATTR InstName {name}'
        # Object with info of capacitor
        self.d[name] = {
            "header":header,
            "nameTag":nameTag,
        }
        # Change window size depends of rotation
        if deg != 0:
            if deg == 90:
                window  = "WINDOW 0 0 32 VBottom 2\nWINDOW 3 32 32 VTop 2"
            elif deg == 180:
                window  = "WINDOW 0 24 64 VLeft 2\nWINDOW 3 24 0 VLeft 2"
            elif deg == 270:
                window  = "WINDOW 0 32 32 VTop 2\nWINDOW 3 0 32 VBottom 2"
            self.d[name]["window"] = window
        self.coords.append({
            "start_x": x, 
            "start_y": y, 
            "end_x": x+round(np.sin(np.deg2rad(deg)))*16*5, 
            "end_y": y-round(np.cos(np.deg2rad(deg)))*16*5, 
        })
                     
    def voltage(self, x, y, deg, val):
        # x = initial position in x
        # y = initial position in y
        # deg = rotation (0, 90, 270)
        # val = capacitor value
        x, y = self.coordsSetter(x, y, "volt", deg)
        # Name of capacitor is equal to the number of components 
        name = f'V{len(self.v)}'
        # Coords and rotation
        header = f'SYMBOL voltage {x} {y} R{deg}'
        # Box sizes
        window = ""
        # Resistance name
        nameTag = f'SYMATTR InstName {name}'
        # Resistance value
        valueTag = f'SYMATTR Value {val}'
        # Change window size depends of rotation
        
        if deg == 0:
            window  = "WINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0"
        elif deg == 90:
            window  = "WINDOW 0 -32 56 VBottom 2\nWINDOW 3 32 56 VTop 2\nWINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0"
        elif deg == 180:
            window  = "WINDOW 0 24 96 VLeft 2\nWINDOW 3 24 16 VLeft 2\nWINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0"
        elif deg == 270:
            window  = "WINDOW 0 32 56 VTop 2\nWINDOW 3 -32 56 VBottom 2\nWINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0"
        # Object with info of capacitor
        self.v[name] = {
            "header":header,
            "nameTag":nameTag,
            "valueTag":valueTag,
            "window":window
        }
        self.coords.append({
            "start_x": x, 
            "start_y": y, 
            "end_x": x+round(np.sin(np.deg2rad(deg)))*16*5, 
            "end_y": y-round(np.cos(np.deg2rad(deg)))*16*5, 
        })

    def current(self, x, y, deg, val):
        # x = initial position in x
        # y = initial position in y
        # deg = rotation (0, 90, 270)
        # val = capacitor value
        x, y = self.coordsSetter(x, y)
        # Name of capacitor is equal to the number of components 
        name = f'I{len(self.v)}'
        # Coords and rotation
        header = f'SYMBOL current {x} {y} R{deg}'
        # Box sizes
        window = ""
        # Resistance name
        nameTag = f'SYMATTR InstName {name}'
        # Resistance value
        valueTag = f'SYMATTR Value {val}'
        # Change window size depends of rotation
        
        if deg == 90:
            window  = "WINDOW 0 -32 40 VBottom 2\nWINDOW 3 32 40 VTop "
        elif deg == 180:
            window  = "WINDOW 0 24 80 Left 2\nWINDOW 3 24 0 Left "
        elif deg == 270:
            window  = "WINDOW 0 32 40 VTop 2\nWINDOW 3 -32 40 VBottom "
        # Object with info of capacitor
        self.v[name] = {
            "header":header,
            "nameTag":nameTag,
            "valueTag":valueTag,
            "window":window
        }
        self.coords.append({
            "start_x": x, 
            "start_y": y, 
            "end_x": x+round(np.sin(np.deg2rad(deg)))*16*5, 
            "end_y": y-round(np.cos(np.deg2rad(deg)))*16*5, 
        })
        
    def Component(self, x, y, deg, compName):
        x, y = self.coordsSetter(x, y)
        # For mosfets name starts with M
        if compName == "nmos" or compName == "pmos":
            name = f'M{len(self.comp)}'
        # For bjts name starts with Q
        elif compName == "npn" or compName == "pnp":
            name = f'Q{len(self.comp)}'

        # For opamps name starts with OpAmps and add library
        elif compName == "opamp" or compName == "UniversalOpAmp":
            name = f'U{len(self.comp)}'
            compName = "OpAmps\\"+compName
            include = f'TEXT {x} {y-50} Left 2 !.inc opamp.sub'
        else:
            return
        
        header = f'SYMBOL {compName} {x} {y} R{deg}'
        nameTag = f'SYMATTR InstName {name}'
        self.comp[name] = {
            "header":header,
            "nameTag":nameTag,
        }
        try:
            self.comp[name][include] = include
        except:
            return
                
    def getWires(self):
        return self.wires
    def getR(self):
        return self.r
    def getC(self):
        return self.c
    def getL(self):
        return self.l
    def getD(self):
        return self.d
    def getV(self):
        return self.v
    def getComp(self):
        return self.comp
    def getCoords(self):
        return self.coords
    def getComponents(self):
        return ["ground", "res", "cap", "ind", "diode", "voltage", "current"]
    
    def compile(self, file_name = "output.asc"):
        self.asc = self.asc + '\n'.join([wire for wire in self.wires.values()]) + '\n'
        self.asc = self.asc + '\n'.join([g for g in self.g.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.r.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.c.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.l.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.d.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.v.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.comp.values()]) + '\n'
        self.asc = re.sub(r'\n+', '\n', self.asc)
        file = open(file_name, "w")
        a = file.write(self.asc)
        file.close()
        
    #def draw():