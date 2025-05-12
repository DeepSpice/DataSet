import re
import numpy as np

class SchematicAscGenerator:
    def __init__(self):
        self.components = {
            'wires': {},
            'ground': {},
            'res': {},
            'cap': {},
            'ind': {},
            'diode': {},
            'volt': {},
            'current': {},
            'comp': {}
        }

        self.rotation = {
            # deg: [sign x, sign y, length x, length y]
            0: [1, 1, 0, 1],
            90: [-1, 1, 1, 0],
            180: [-1, -1, 0, -1],
            270: [1, -1, -1, 0],
        }
        self.components_offsets = {
            # "comp": [x, y, length, phase]
            'wire': [0,0,0,0],
            'ground': [0,0,0,0],
            'res': [16,16,96-16,0],
            'cap': [16,0,64,0],
            'ind': [16,16,96-16,0],
            'diode': [16,0,64,90],
            'volt': [0,16,112-16,90],
            'current': [0,0,80,90],
            'comp': [0,0,80,0]

        }
        self.coords = []
        self.padding = 16
        # File header
        self.asc = "Version 4\nSHEET 1 880 680\n"

    def rotation_matrix(self, deg, init_coords):

        r_matrix = np.asarray([[np.cos(deg*np.pi/180), -np.sin(deg*np.pi/180)],
                               [np.sin(deg*np.pi/180), np.cos(deg*np.pi/180)]])
        
        init_coords = np.asarray(init_coords)

        rotated_coords =  np.dot(r_matrix, init_coords)


        return rotated_coords.astype("int32")


    def reset(self):
        for key in self.components:
            self.components[key] = {}
        self.coords = []
        self.asc = "Version 4\nSHEET 1 880 680\n"

    def coords_setter(self, x0, y0, comp="wire", deg=0):
        initial_x0 = round(x0 / self.padding) * self.padding if x0 % self.padding != 0 else x0
        initial_y0 = round(y0 / self.padding) * self.padding if y0 % self.padding != 0 else y0

        component_off = self.rotation_matrix(deg+self.components_offsets[comp][3], self.components_offsets[comp][:2])

        # Coords for wiring
        new_x0 = initial_x0 + component_off[0]
        new_y0 = initial_y0 + component_off[1]

        new_x1 = new_x0 + self.components_offsets[comp][2]*self.rotation[deg][2]
        new_y1 = new_y0 + self.components_offsets[comp][2]*self.rotation[deg][3]

        return round(new_x0), round(new_y0), round(new_x1), round(new_y1)

    def create_component(self, comp_type, x, y, deg, val=None, extra_config=None):
        component_info = {
            'res': (f'R{len(self.components["res"])}', self.components['res'], "SYMBOL res", val, "resistance"),
            'cap': (f'C{len(self.components["cap"])}', self.components['cap'], "SYMBOL cap", val, "capacitance"),
            'ind': (f'L{len(self.components["ind"])}', self.components['ind'], "SYMBOL ind", val, "inductance"),
            'diode': (f'D{len(self.components["diode"])}', self.components['diode'], "SYMBOL diode", val, None),
            'volt': (f'V{len(self.components["volt"])}', self.components['volt'], "SYMBOL voltage", val, "voltage"),
            'current': (f'V{len(self.components["current"])}', self.components['current'], "SYMBOL current", val, "current"),
            'comp': (f'I{len(self.components["current"])}', self.components['current'], "SYMBOL current", val, "current")
        }

        if comp_type == "current":
            comp_type = "volt"

        if comp_type == "ground":
            self.ground(x, y)

        if comp_type not in component_info:
            return

        name, comp_dict, symbol, value, value_tag = component_info[comp_type]
        x_start, y_start, x_end, y_end = self.coords_setter(x, y, comp_type, deg)
        header = f'{symbol} {x} {y} R{deg}'
        name_tag = f'SYMATTR InstName {name}'
        value_tag = f'SYMATTR Value {value}'

        self.components[comp_type][name] = {
            "header": header,
            "nameTag": name_tag,
            "valueTag": value_tag
        }

        self.coords.append({
            "start_x": x_start, 
            "start_y": y_start, 
            "end_x": x_end,
            "end_y": y_end
        })

    def ground(self, x, y):
        # x = initial position in x
        # y = initial position in y
        x, y, _, _ = self.coords_setter(x, y)
        g_len = self.components['ground']
        name = f'G{len(g_len)}'
        self.components['ground'][name] = f'FLAG {x:-} {y:-} 0'
        self.coords.append({
            "start_x": x, 
            "start_y": y, 
            "end_x": x, 
            "end_y": y, 
        })

    def wire(self, x0, y0, x1, y1):
        # x0, y0, _, _ = self.coords_setter(x0, y0)
        # x1, y1, _, _ = self.coords_setter(x1, y1)

        name = f'W{len(self.components["wires"])}'
        if x0 == x1 or y0 == y1:
            self.components["wires"][name] = f'WIRE {x0:-} {y0:-} {x1:-} {y1:-}'
        else:
            self.components["wires"][name] = f'WIRE {x0:-} {y0:-} {x1:-} {y0:-}\nWIRE {x1:-} {y0:-} {x1:-} {y1:-}'

    def component(self, x, y, deg, comp_name):
        x1, y1 = self.coordsSetter(x, y)
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
            self.components["comp"][name][include] = include
        except:
            return
                
    def getWires(self):
        return self.components["wires"]
    def getR(self):
        return self.components["res"]
    def getC(self):
        return self.components["cap"]
    def getL(self):
        return self.components["ind"]
    def getD(self):
        return self.components["diode"]
    def getV(self):
        return self.components["volt"]
    def getComp(self):
        return self.components["comp"]
    def getCoords(self):
        return self.coords
    def getComponents(self):
        return ["ground", "res", "cap", "ind", "diode", "volt", "current"]
    
    def compile(self, file_name = "output.asc"):
        self.asc = self.asc + '\n'.join([wire for wire in self.components["wires"].values()]) + '\n'
        self.asc = self.asc + '\n'.join([g for g in self.components["ground"].values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.components["res"].values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.components["cap"].values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.components["ind"].values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.components["diode"].values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.components["volt"].values()]) + '\n'
        self.asc = self.asc + '\n'.join(['\n'.join([item for item in symbol.values()]) for symbol in self.components["comp"].values()]) + '\n'
        self.asc = re.sub(r'\n+', '\n', self.asc)
        with open(file_name, "w") as f:
            f.write(self.asc)
            f.close()
        self.reset()
        