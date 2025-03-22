import os
import json

def get_data(path : str) -> dict:
   #get json data
    with open(path) as f:
        data = json.load(f)
       
    return data

data = get_data("./test/inventory.json")
ninv = 0

for id in data :
    ninv += 1
    id_inv = data[id]
    with open(f"./test/inventory/{str(id)}.json", "w", encoding="utf-8") as f:
        json.dump(id_inv, f, indent=2)
    print(f"created inv of {id}, inv {str(ninv)}")