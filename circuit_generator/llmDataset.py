import os
from PIL import Image
import json
from io import BytesIO
import requests

ascs_path = os.path.join("Data/ascs")
pngs_path = os.path.join("Data/pngs")

ascs_files = os.listdir(ascs_path)
pngs_files = os.listdir(pngs_path)

train_dataset = []
test_dataset = []


# Generate train dataset
for text, image in zip(ascs_files, pngs_files):

    if(text.replace(".asc","") != image.replace(".png","")):
        print("asc with name " + text + " not match with image " + image)
        break

    # Read ascs
    file = open(ascs_path+"/"+text, "r")
    asc_text = file.read()

    # Read image
    pil_image = Image.open(pngs_path+"/"+image)

    # Structure for LLaVA JSON
    json_data = {
        "messages": [{
            "content": [
            {
                "index": 0,
                "text": None,
                "type": "image"
            }],
            "role": "user"
        },
        {
            "content": [{
                "index": None,
                "text" : asc_text,
                "type": "text"
            }],
            "role": "assistant"
        }
        ],
        "images": [pil_image]
    }

    print(json_data)


    file.close()
    pil_image.close()