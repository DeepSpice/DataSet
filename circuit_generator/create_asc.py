import numpy as np
import random
import sys
from LTSpice_generator import schematicAscGenerator

def create_asc(n=1, path=""):
    generator = schematicAscGenerator()
    elements = generator.getComponents()
    orientation = [0, 90]

    for i in range(n):
        n_elements = random.randint(2, 10)
        n_nodes = [i for i in range(random.randint(2, n_elements))]        
        positions = []
        for element in range(n_elements):
            node_i = random.choice(n_nodes)
            node_f = random.choice(np.delete(n_nodes, node_i))

            component = random.choice(elements)
            x_i, y_i = np.random.randint(10,100, size=2)*16

            if component == "ground":
                generator.ground(x_i, y_i)
            elif component == "res":
                generator.res(x_i, y_i, random.choice(orientation), random.randint(1,5))
            elif component == "cap":
                generator.cap(x_i, y_i, random.choice(orientation), random.randint(1,5))
            elif component == "ind":
                generator.ind(x_i, y_i, random.choice(orientation), random.randint(1,5))
            elif component == "diode":
                generator.diode(x_i, y_i, random.choice(orientation))
            elif component == "voltage":
                generator.voltage(x_i, y_i, random.choice(orientation), random.randint(1,5))
            elif component == "current":
                generator.current(x_i, y_i, random.choice(orientation), random.randint(1,5))

            positions.append({
                "node_i": node_i,
                "node_f": node_f,
                "element": element
            })

        init_end = [ [i["node_i"], i["node_f"], i["element"]] for i in positions]

        coords = generator.getCoords()
        for node in n_nodes:
            items = []
            for init, end, element in init_end:
                if init == node:
                    x_in = coords[element]["start_x"]
                    y_in = coords[element]["start_y"]
                    items.append([x_in, y_in])
                if end == node:
                    x_fin = coords[element]["end_x"]
                    y_fin = coords[element]["end_y"]
                    items.append([x_fin, y_fin])

            for index, item in enumerate(items):
                if index == 0:
                    continue
                generator.wire(item[0], item[1], items[0][0], items[0][1])
        generator.compile(path+"circuit_"+str(i)+".asc")
        
sys.modules[__name__] = create_asc