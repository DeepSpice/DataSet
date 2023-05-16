import re

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
        self.asc = "Version 4\nSHEET 1 880 680"
        
    def wire(self, x0, y0, x1, y1):
        name = f'W{len(self.wires)}'
        self.wires[name] = f'WIRE {x0} {y0} {x1} {y1}'
    
    def ground(self, x, y):
        name = f'G{len(self.g)}'
        self.wires[name] = f'FLAG {x} {y} 0'
            
    def res(self, x, y, deg, val):
        name = f'R{len(self.r)}'
        header = f'SYMBOL res {x} {y} R{deg}'
        window = ""
        nameTag = f'SYMATTR InstName {name}'
        valueTag = f'SYMATTR Value {val}'
        self.r[name] = {
            "header":header,
            "nameTag":nameTag,
            "valueTag":valueTag
        }
        if deg == 90 or deg==270:
            window  = "WINDOW 0 0 56 VBottom 2\nWINDOW 3 32 56 VTop 2" if deg == 90 else "WINDOW 0 32 56 VBottom 2\nWINDOW 3 0 56 VTop 2"
            self.r[name]["window"] = window
            
    def cap(self, x, y, deg, val):
        name = f'C{len(self.c)}'
        header = f'SYMBOL cap {x} {y} R{deg}'
        window = ""
        nameTag = f'SYMATTR InstName {name}'
        valueTag = f'SYMATTR Value {val}'
        self.c[name] = {
            "header":header,
            "nameTag":nameTag,
            "valueTag":valueTag
        }
        if deg != 0:
            if deg == 90:
                window  = "WINDOW 0 0 32 VBottom 2\nWINDOW 3 32 32 VTop 2"
            elif deg == 180:
                window  = "WINDOW 0 25 56 VLeft 2\nWINDOW 3 24 8 VLeft 2"
            elif deg == 270:
                window  = "WINDOW 0 32 32 VTop 2\nWINDOW 3 0 32 VBottom 2"
            self.c[name]["window"] = window
            
    def ind(self, x, y, deg, val):
        name = f'L{len(self.l)}'
        header = f'SYMBOL ind {x} {y} R{deg}'
        window = ""
        nameTag = f'SYMATTR InstName {name}'
        valueTag = f'SYMATTR Value {val}'
        self.l[name] = {
            "header":header,
            "nameTag":nameTag,
            "valueTag":valueTag
        }
        if deg != 0:
            if deg == 90:
                window  = "WINDOW 0 5 56 VBottom 2\nWINDOW 3 32 56 VTop 2"
            elif deg == 180:
                window  = "WINDOW 0 36 80 VLeft 2\nWINDOW 3 36 40 VLeft 2"
            elif deg == 270:
                window  = "WINDOW 0 32 56 VTop 2\nWINDOW 3 5 56 VBottom 2"
            self.l[name]["window"] = window
            
            
    def diode(self, x, y, deg):
        name = f'D{len(self.d)}'
        header = f'SYMBOL diode {x} {y} R{deg}'
        window = ""
        nameTag = f'SYMATTR InstName {name}'
        self.d[name] = {
            "header":header,
            "nameTag":nameTag,
        }
        if deg != 0:
            if deg == 90:
                window  = "WINDOW 0 0 32 VBottom 2\nWINDOW 3 32 32 VTop 2"
            elif deg == 180:
                window  = "WINDOW 0 24 64 VLeft 2\nWINDOW 3 24 0 VLeft 2"
            elif deg == 270:
                window  = "WINDOW 0 32 32 VTop 2\nWINDOW 3 0 32 VBottom 2"
            self.d[name]["window"] = window
            
            
    def voltage(self, x, y, deg, val):
        name = f'V{len(self.v)}'
        header = f'SYMBOL voltage {x} {y} R{deg}'
        window = ""
        nameTag = f'SYMATTR InstName {name}'
        valueTag = f'SYMATTR Value {val}'
        
        if deg == 0:
            window  = "WINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0"
        elif deg == 90:
            window  = "WINDOW 0 -32 56 VBottom 2\nWINDOW 3 32 56 VTop 2\nWINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0"
        elif deg == 180:
            window  = "WINDOW 0 24 96 VLeft 2\nWINDOW 3 24 16 VLeft 2\nWINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0"
        elif deg == 270:
            window  = "WINDOW 0 32 56 VTop 2\nWINDOW 3 -32 56 VBottom 2\nWINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0"
            
        self.v[name] = {
            "header":header,
            "nameTag":nameTag,
            "valueTag":valueTag,
            "window":window
        }
        
    def Component(self, x, y, deg, compName):
        if compName == "nmos" or compName == "pmos":
            name = f'M{len(self.comp)}'
        elif compName == "npn" or compName == "pnp":
            name = f'Q{len(self.comp)}'
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
    
    
    def compile(self):
        self.asc = self.asc + '\n'.join([wire for wire in self.wires.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.r.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.c.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.l.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.d.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.v.values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.comp.values()]) + '\n'
        self.asc = re.sub(r'\n+', '\n', self.asc)
        file = open("output.asc", "w")
        a = file.write(self.asc)
        file.close()
        
    #def draw():