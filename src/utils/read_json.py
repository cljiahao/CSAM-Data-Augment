import json


def read_config():
    with open('./core/config.json','r') as f:
        config = json.load(f)
    
    return config


def write_config(dic):
    config = read_config()
    
    for k,v in dic.items():
        config[k] = v
    
    with open('core/config.json','w') as f:
        json.dump(config, f, indent=4)