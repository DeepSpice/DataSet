import pandas as pd
import os
from pathlib import Path   
import tqdm 



print(os.getcwd())

data = pd.DataFrame(columns=["image", "conversation"])

asc_path = Path(os.getcwd()+"/Data/ascs/")
png_path = Path(os.getcwd()+"/Data/pngs/")
files_asc = [file.name for file in asc_path.iterdir() if file.is_file()]
files_png = [file.name for file in png_path.iterdir() if file.is_file()]

print(asc_path.absolute)


def read_asc(path, folder):
    with open(folder+"/"+path, 'r') as file:
        content = file.read()
        file.close()

    return content

conversation_data = [[{"from": "human",
                        "value": "<image>\nTake this circuit and transform it in an asc file, set the values of each component, and put the wires and components orientation propertly"
                      },{
                        "from": "gpt",
                        "value": read_asc(text, asc_path.as_posix())
                      }] for text in files_asc]

print("Files ASCs:", files_asc)
print("Files PNGs:", files_png)
print(conversation_data)


if(len(conversation_data)==len(files_png)):
    data["image"] = files_png
    data["conversation"] = conversation_data
    data["id"] = data.index

data.to_json("data_for_tl.json",orient="records")