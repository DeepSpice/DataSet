import numpy as np
import random
import sys
from tqdm import tqdm
from LTSpice_generator import SchematicAscGenerator
#from circuit_generator.LTSpice_generator import SchematicAscGenerator
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
    generator = SchematicAscGenerator()
    component_padding = generator.padding
    elements = generator.getComponents()
    orientation = [0, 90]


    # generator.create_component("volt", 2*component_padding, 2*component_padding, 0, random.randint(1,5))
    # generator.create_component("volt", 1*component_padding, 1*component_padding, 90, random.randint(1,5))
    # generator.create_component("volt", 2*component_padding, 0*component_padding, 180, random.randint(1,5))
    # generator.create_component("volt", 3*component_padding, 1*component_padding, 270, random.randint(1,5))
    for i in tqdm(range(n)):
        n_elements = random.randint(2, 10)
        n_nodes = [i for i in range(random.randint(2, 2+int(n_elements/2)))]        
        positions = []

        G = grid_graph(dim=(100, 100))


        for element in range(n_elements):
            node_i = random.choice(n_nodes)
            node_f = int(random.choice(np.delete(n_nodes, node_i)))

            component = random.choice(elements)
            coords_list = np.arange(10, 100, 5)
            x_i, y_i = np.random.choice(coords_list, size=2)*component_padding
            generator.create_component(component, x_i, y_i, random.choice(orientation), random.randint(1,5))

            positions.append({
                "node_i": node_i,
                "node_f": node_f,
                "element": element
            })

        init_end = [ [i["node_i"], i["node_f"], i["element"]] for i in positions]


        print("----components-----")
        print(positions)
        #print(init_end)
        

        G = grid_graph(dim=(100, 100))

        coords = generator.getCoords()
        print(coords)

        for node in n_nodes:
            items = []
            for init, end, element in init_end:
                x_in = int(coords[element]["start_x"])
                y_in = int(coords[element]["start_y"])
                x_fin = int(coords[element]["end_x"])
                y_fin = int(coords[element]["end_y"])

                if(x_in == x_fin):
                    nodes_in_component = np.linspace(int(y_in/component_padding), int(y_fin/component_padding), int(abs(y_in/component_padding - y_fin/component_padding))+1)
                    for k, node_element in enumerate(nodes_in_component):
                        if(len(nodes_in_component) == k+1):
                            break
                        if(((int(x_in/component_padding), int(node_element)), (int(x_fin/component_padding), int(nodes_in_component[k+1]))) in  G.edges):
                            G.remove_edge((x_in/component_padding, node_element), (x_fin/component_padding, nodes_in_component[k+1])) 

                if(y_in == y_fin):
                    nodes_in_component = np.linspace(int(x_in/component_padding), int(x_fin/component_padding), int(abs(x_in/component_padding - x_fin/component_padding))+1)
                    for k, node_element in enumerate(nodes_in_component):
                        if(len(nodes_in_component) == k+1):
                            break
                        if(((int(y_in/component_padding), int(node_element)), (int(y_fin/component_padding), int(nodes_in_component[k+1]))) in  G.edges):
                            G.remove_edge((int(y_in/component_padding), int(node_element)), (int(y_fin/component_padding), int(nodes_in_component[k+1]))) 

                if init == node:
                    items.append([x_in, y_in])
                if end == node:
                    items.append([x_fin, y_fin])

            # print(items)
            for index, item in enumerate(items):
                if index == 0:
                    continue
                
                path = dijkstra_path(G, (item[0]/component_padding, item[1]/component_padding), (items[0][0]/component_padding, items[0][1]/component_padding))

                simply_path = simplify_trajectory(path)
                
                for node_index, path_nodes in enumerate(simply_path):
                    # print("----Coords for generating wires-----")
                    # print((path_nodes[0]+1)*component_padding, (path_nodes[1]+1)*component_padding, (simply_path[node_index+1][0]+1)*component_padding, (simply_path[node_index+1][1]+1)*component_padding)
                    generator.wire(
                        int((path_nodes[0])*component_padding), 
                        int((path_nodes[1])*component_padding), 
                        int((simply_path[node_index+1][0])*component_padding), 
                        int((simply_path[node_index+1][1])*component_padding))
                    if(node_index+1 >= len(simply_path)-1):
                        break

        generator.compile(save_path+"circuit_"+str(i)+".asc")
        
# sys.modules[__name__] = create_asc

if __name__ == "__main__":
    create_asc()