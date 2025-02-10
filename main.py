from asc2png.main_asc2png import convert
from circuit_generator.main_generator import generate
import time
import sys
from io import StringIO
import os



if __name__ == "__main__":
    number_of_circuits = int(input("Ingrese el número de circuitos a generar: "))

    start_time = time.time()
    print("-------------ASC---------------")
    generate(number_of_circuits)
    print("-------------TEX, PDF & PNG---------------")
    # Configura un StringIO para capturar la salida de writeCircuiTikz
    #output_buffer = StringIO()
    # Sobrescribe el atributo stdout de sys
    #sys.stdout = output_buffer

    print(os.listdir("./Data/ascs/"))

    convert()

    # Restaura el stdout original
    #sys.stdout = sys.__stdout__

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Tiempo transcurrido generacion: {elapsed_time} segundos")
