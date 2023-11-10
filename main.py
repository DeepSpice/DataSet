from asc2png.main_asc2png import convert
from circuit_generator.main_generator import generate
import time
import sys

def show_spinner():
    spinner = "|/-\\"
    for _ in range(10):
        for char in spinner:
            sys.stdout.write(char)
            sys.stdout.flush()
            # time.sleep(0.1)
            sys.stdout.write("\b")

if __name__ == "__main__":
    number_of_circuits = int(input("Ingrese el número de circuitos a generar: "))

    start_time = time.time()

    print("Generating images...")
    show_spinner()

    generate(number_of_circuits)

    convert()


    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Tiempo transcurrido generacion: {elapsed_time} segundos")