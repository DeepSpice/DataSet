import re
import numpy as np

class SchematicAscGenerator:
    def __init__(self):
        self.components = {
            'wires': {},
            'g': {},
            'r': {},
            'c': {},
            'l': {},
            'd': {},
            'v': {},
            'comp': {}
        }
        self.coords = []
        self.padding = 16
        # File header
        self.asc = "Version 4\nSHEET 1 880 680\n"

    def reset(self):
        for key in self.components:
            self.components[key] = {}
        self.coords = []
        self.asc = "Version 4\nSHEET 1 880 680\n"

    def coords_setter(self, x, y, comp="wire", deg=0):
        new_x = round(x / self.padding) * self.padding if x % self.padding != 0 else x
        new_y = round(y / self.padding) * self.padding if y % self.padding != 0 else y

        adjustments = {
            "res": (-np.sign(np.cos(np.deg2rad(deg + 1))), -np.sign(np.sin(np.deg2rad(deg + 1)))),
            "ind": (-np.sign(np.cos(np.deg2rad(deg + 1))), -np.sign(np.sin(np.deg2rad(deg + 1)))),
            "diode": (-round(np.cos(np.deg2rad(deg))), -round(np.sin(np.deg2rad(deg)))),
            "cap": (-round(np.cos(np.deg2rad(deg))), -round(np.sin(np.deg2rad(deg)))),
            "volt": (round(np.sin(np.deg2rad(deg))), -round(np.cos(np.deg2rad(deg)))),
            "curr": (0, 0),
            "wire": (0, 0)
        }

        if comp in adjustments:
            adj_x, adj_y = adjustments[comp]
            new_x += self.padding * adj_x
            new_y += self.padding * adj_y

        return round(new_x), round(new_y)

    def create_component(self, comp_type, x, y, deg, val=None, extra_config=None):
        component_info = {
            'res': (f'R{len(self.components["r"])}', self.components['r'], "SYMBOL res", val, "resistance"),
            'cap': (f'C{len(self.components["c"])}', self.components['c'], "SYMBOL cap", val, "capacitance"),
            'ind': (f'L{len(self.components["l"])}', self.components['l'], "SYMBOL ind", val, "inductance"),
            'diode': (f'D{len(self.components["d"])}', self.components['d'], "SYMBOL diode", val, None),
            'volt': (f'V{len(self.components["v"])}', self.components['v'], "SYMBOL volt", val, "voltage"),
            'current': (f'I{len(self.components["comp"])}', self.components['comp'], "SYMBOL current", val, "current")
        }

        if comp_type not in component_info:
            return

        name, comp_dict, symbol, value, value_tag = component_info[comp_type]
        x1, y1 = self.coords_setter(x, y, comp_type, deg)
        header = f'{symbol} {x1} {y1} R{deg}'
        name_tag = f'SYMATTR InstName {name}'
        value_tag = f'SYMATTR Value {value}'

        comp_dict[name] = {
            "header": header,
            "nameTag": name_tag,
            "valueTag": value_tag
        }

        def wire(self, x0, y0, x1, y1):
        header = f'{symbol} {x1} {y1} R{deg}'
        #'''
        name_tag = f'SYMATTR InstName {name}'
        # x0 = initial position in x
        value_tag = f'SYMATTR Value {value}'
        # y0 = initial position in y
        # x1 = final position in x
        # y1 = final position in y
        # '''
        x0, y0 = self.coordsSetter(x0, y0)
        x1, y1 = self.coordsSetter(x1, y1)
 
 
        if (x0 == x1) or (y0 == y1): ### Cable recto
        comp_dict[name] = {
            name = f'W{len(self.wires)}'        
            "header": header,
            self.wires[name] = f'WIRE {x0:-} {y0:-} {x1:-} {y1:-}'
            "nameTag": name_tag,
        else:
            "valueTag": value_tag
            name = f'W{len(self.wires)}'
            self.wires[name] = f'WIRE {x0:-} {y0:-} {x1:-} {y0:-}\nWIRE {x1:-} {y0:-} {x1:-} {y1:-}'


        def ground(self, x, y):
        # x = initial position in x
        # y = initial position in y
        x, y = self.coordsSetter(x, y)
        name = f'G{len(self.g)}'
        self.g[name] = f'FLAG {x:-} {y:-} 0'
        self.coords.append({
            "start_x": x, 
            "start_y": y, 
            "end_x": x, 
            "end_y": y, 
        })

        if deg != 0:
            window_sizes = {
                90: "WINDOW 0 0 32 VBottom 2\nWINDOW 3 32 32 VTop 2",
                180: "WINDOW 0 24 56 VLeft 2\nWINDOW 3 24 8 VLeft 2",
                270: "WINDOW 0 32 32 VTop 2\nWINDOW 3 0 32 VBottom 2"
            }
            if comp_type in ['volt', 'current']:
                window_sizes = {
                    0: "WINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0",
                    90: "WINDOW 0 -32 56 VBottom 2\nWINDOW 3 32 56 VTop 2\nWINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0",
                    180: "WINDOW 0 24 96 VLeft 2\nWINDOW 3 24 16 VLeft 2\nWINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0",
                    270: "WINDOW 0 32 56 VTop 2\nWINDOW 3 -32 56 VBottom 2\nWINDOW 123 0 0 VLeft 0\nWINDOW 39 0 0 VLeft 0"
                }
            comp_dict[name]["window"] = window_sizes.get(deg, "")

        self.coords.append({
            "start_x": x,
            "start_y": y,
            "end_x": x - round(np.sin(np.deg2rad(deg))) * self.padding * 4,
            "end_y": y + round(np.cos(np.deg2rad(deg))) * self.padding * 4,
        })

    def wire(self, x0, y0, x1, y1):
        x0, y0 = self.coords_setter(x0, y0)
        x1, y1 = self.coords_setter(x1, y1)

        name = f'W{len(self.components["wires"])}'
        if x0 == x1 or y0 == y1:
            self.components["wires"][name] = f'WIRE {x0:-} {y0:-} {x1:-} {y1:-}'
        else:
            self.components["wires"][name] = f'WIRE {x0:-} {y0:-} {x1:-} {y0:-}\nWIRE {x1:-} {y0:-} {x1:-} {y1:-}'

    def ground(self, x, y):
        x, y = self.coords_setter(x, y)
        name = f'G{len(self.components["g"])}'
        self.components["g"][name] = f'FLAG {x:-} {y:-} 0'
        self.coords.append({
            "start_x": x,
            "start_y": y,
            "end_x": x,
            "end_y": y,
        })

    def current(self, x, y, deg, val):
        x1, y1 = self.coords_setter(x, y)
        name = f'I{len(self.v)}'
        header = f'SYMBOL current {x1} {y1} R{deg}'
        name_tag = f'SYMATTR InstName {name}'
        value_tag = f'SYMATTR Value {val}'

        window = ""
        if deg == 90:
            window = "WINDOW 0 -32 40 VBottom 2\nWINDOW 3 32 40 VTop 2"
        elif deg == 180:
            window = "WINDOW 0 24 80 VLeft 2\nWINDOW 3 24 0 VLeft 2"
        elif deg == 270:
            window = "WINDOW 0 32 40 VTop 2\nWINDOW 3 -32 40 VBottom 2"
            
        # Object with info of capacitor
        self.v[name] = {
            "header": header,
            "nameTag": name_tag,
            "valueTag": value_tag,
            "window": window
        }
        self.coords.append({
            "start_x": x,
            "start_y": y,
            "end_x": x - round(np.sin(np.deg2rad(deg))) * self.padding * 5,
            "end_y": y + round(np.cos(np.deg2rad(deg))) * self.padding * 5,
        })

    def component(self, x, y, deg, comp_name):
        x1, y1 = self.coords_setter(x, y)
        if comp_name in ["nmos", "pmos"]:
            name = f'M{len(self.comp)}'
        elif comp_name in ["npn", "pnp"]:

         

        # For opamps name starts with OpAmps and add library
        elif compName == "opamp" or compName == "UniversalOpAmp":
            name = f'U{len(self.comp)}'
            compName = "OpAmps\\"+compName
            include = f'TEXT {x1} {y1-50} Left 2 !.inc opamp.sub'
        else:
            return
        
        header = f'SYMBOL {compName} {x1} {y1} R{deg}'
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
        with open(file_name, "w") as f:
            f.write(self.asc)
            f.close()
        self.reset()
        

