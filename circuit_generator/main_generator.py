from circuit_generator.create_asc import create_asc
import os

pathASC = "./Data/ascs/"

def create_folder(folder_path):
    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # If not, create it
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

def generate(number_of_circuits):
    create_folder(pathASC)
    create_asc(number_of_circuits, pathASC)


