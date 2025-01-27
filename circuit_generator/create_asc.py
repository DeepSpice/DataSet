import numpy as np
import random
import sys
from tqdm import tqdm
#from LTSpice_generator import schematicAscGenerator
from circuit_generator.LTSpice_generator import schematicAscGenerator
from networkx import grid_graph, dijkstra_path

def simplify_trajectory(trajectory):
    # Lista para almacenar los nodos simplificados
    simplified_nodes = []
    
    # Dirección previa inicializada como None
    direccion_previa = None
    
    for i in range(len(trajectory) - 1):
        # Calculamos la dirección actual como un vector (diferencia entre nodos consecutivos)
        direccion_actual = (
            trajectory[i + 1][0] - trajectory[i][0],
            trajectory[i + 1][1] - trajectory[i][1]
        )
        
        # Si la dirección actual es diferente de la dirección previa, añadimos el nodo actual
        if direccion_actual != direccion_previa:
            simplified_nodes.append(trajectory[i])
            direccion_previa = direccion_actual
    
    # Añadimos el último nodo de la trayectoria
    simplified_nodes.append(trajectory[-1])
    
    return simplified_nodes

def create_asc(n=1, save_path=""):
    generator = schematicAscGenerator()
    elements = generator.getComponents()
    orientation = [0, 90]

    for i in tqdm(range(n)):
        n_elements = random.randint(2, 10)
        n_nodes = [i for i in range(random.randint(2, n_elements))]        
        positions = []

        G = grid_graph(dim=(100, 100))


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
        

        G = grid_graph(dim=(100, 100))

        #G.remove_edge(node_i, node_f)

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
                path = dijkstra_path(G, (item[0]/16, item[1]/16), (items[0][0]/16, items[0][1]/16))
                simply_path = simplify_trajectory(path)
                
                for node_index, path_nodes in enumerate(simply_path):
                    generator.wire(path_nodes[0]*16, path_nodes[1]*16, simply_path[node_index+1][0]*16, simply_path[node_index+1][1]*16)
                    if(node_index+1 >= len(simply_path)-1):
                        break

        generator.compile(save_path+"circuit_"+str(i)+".asc")
        
# sys.modules[__name__] = create_asc

if __name__ == "__main__":
    create_asc()