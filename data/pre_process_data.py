def get_instance_slot_from_file(name_slot, is_return_list = False):

    instances = []

    file_paths = [
        "data/MixSNIPS_clean/train.txt",
        "data/MixSNIPS_clean/test.txt",
        "data/MixSNIPS_clean/dev.txt"
    ]

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                words = line.split()
                if ("B-" + name_slot) in words:
                    instances.append("\n" + words[0])
                elif ("I-" + name_slot) in words:
                    instances[len(instances)-1] = instances[len(instances)-1] + " " + words[0]
    
    instances = list(set(instances))
    
    with open("data/MixSNIPS_clean/" + name_slot + "_instance.txt", "w") as file:
        file.writelines(instances)
    
    if is_return_list:
        return instances

import json

with open("intent_slot_mapping.json", "r") as json_file:
    slots = json.load(json_file)["slots"]

    for slot in slots:
        get_instance_slot_from_file(slot)