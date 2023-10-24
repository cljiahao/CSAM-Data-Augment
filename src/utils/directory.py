import os
from shutil import rmtree, make_archive

from utils.read_json import read_config
from utils.transfer import grab_images


def zip_check_dataset(base_dir):
    
    # TODO: Reset version and delete old folder if takes up too much space
    # TODO: Check if there is more than 1 version in folder (Due to user intervention)
    
    dataset_dir = os.path.join(base_dir,"dataset") if os.path.basename(base_dir) != "dataset" else base_dir
    old_dir = os.path.join(dataset_dir,"old")
    if not os.path.exists(old_dir): os.makedirs(old_dir)
    fol_arr = [fol for fol in os.listdir(dataset_dir) if fol != "old"]
    
    # Archiving / zipping old versions to make way for new version
    if len(fol_arr) > 0: 
        latest_version = fol_arr[0]                       # Assuming only 1 version in the folder
        make_archive(os.path.join(old_dir,latest_version),"zip",dataset_dir,latest_version)
        rmtree(os.path.join(dataset_dir,latest_version))
        new_version = f"V{int(latest_version[1:]) + 1}"
    elif len(os.listdir(old_dir)) > 0:
        last_old_version = sorted(os.listdir(old_dir),reverse=True)[0]
        lov_name = last_old_version.split(".")[0]
        new_version = f"V{int(lov_name[1:]) + 1}"
    else: new_version = "V1"
    
    dataset_fols = {}
    for i in ["training","validation"]:
        for j in ["ng","good","others"]:
            dataset_fols[f"{i}_{j}"] = os.path.join(dataset_dir,new_version,i,j)
            if not os.path.exists(dataset_fols[f"{i}_{j}"]): os.makedirs(dataset_fols[f"{i}_{j}"])
    
    return dataset_fols


def create_holder(regrab=False):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    holder_dir = os.path.join(base_dir,"holder")
    config = read_config()
    holder_qty = config['quantity']['ng']
    good_dir = os.path.join(config['directories']['input'],"good")

    if regrab:
        if os.path.exists(holder_dir): rmtree(holder_dir)
        grab_images(good_dir,holder_dir,holder_qty)
    else:
        if not os.path.exists(holder_dir): os.makedirs(holder_dir)
        if len(os.listdir(holder_dir)) == 0 or len(os.listdir(holder_dir)) != holder_qty: grab_images(good_dir,holder_dir,holder_qty)
    
    return holder_dir


def get_breakdown_qty():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    breakdown_dir = os.path.join(base_dir,"breakdown")
    if not os.path.exists(breakdown_dir): os.makedirs(breakdown_dir)

    config = read_config()

    fol_qty = {}
    for fol in config['breakdown']:
        if fol in os.listdir(breakdown_dir): fol_qty[fol] = len(os.listdir(os.path.join(breakdown_dir,fol)))
        else: os.makedirs(os.path.join(breakdown_dir,fol))

    for i in config['breakdown']:
        if i not in fol_qty.keys(): fol_qty[i] = 0

    return fol_qty