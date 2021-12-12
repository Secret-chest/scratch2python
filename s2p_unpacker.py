"""
This program generates a dictionary and objects based on the project.json file.
It also loads the project file set in main.py.

======= CLASS INFO =======
The various files with classes are used by this program and the correct data is
set. Those are then used to build the project in main.py.
"""
# This is the Scratch2Python unpacker.
# The main file you probably want to run is located at main.py.
import zipfile as zf
import json
import target, costume, sound, block, variable, monitor  # , broadcast
from pathlib import Path
from io import StringIO


def sb3_unpack(sb3):
    # If project does not exist, quit with exit code 1
    if not Path(sb3).exists():
        print("ERROR: Project file does not exist")
        exit(1)

    print("DEBUG: Loading project")
    project = zf.ZipFile(sb3, "r")
    project_json = json.loads(project.read("project.json"))
    targets = []

    print("DEBUG: Project JSON output:", project_json)
    # Generate the dictionary based on the contents of project.json
    for target_obj in project_json['targets']:
        # If stage, get background
        if target_obj["isStage"]:
            current_bg_file = project.read(target_obj["costumes"][target_obj["currentCostume"]]["assetId"] + "." + target_obj["costumes"][target_obj["currentCostume"]]["dataFormat"])
        t = target.Target()

        # Set sprite values
        if "x" in target_obj:
            t.x = target_obj["x"]
            t.y = target_obj["y"]
            t.direction = target_obj["direction"]
        t.currentCostume = target_obj["currentCostume"]

        # Get costumes
        for costume_obj in target_obj["costumes"]:
            c = costume.Costume()
            if "md5ext" in costume_obj:
                c.md5ext = costume_obj["md5ext"]
                c.rotationCenterX, c.rotationCenterY = costume_obj["rotationCenterX"], costume_obj["rotationCenterY"]
            c.file = project.read(costume_obj["assetId"] + "." + costume_obj["dataFormat"])
            t.costumes.append(c)

        # Set blocks to their correct values
        for block_id, block_obj in target_obj["blocks"].items():
            b = block.Block()
            b.blockID = block_id
            b.opcode = block_obj["opcode"]
            b.next = block_obj["next"]
            b.parent = block_obj["parent"]
            b.shadow = block_obj["shadow"]
            b.topLevel = block_obj["topLevel"]
            b.inputs = block_obj["inputs"]
            b.fields = block_obj["fields"]
            b.blockRan = False
            b.target = t
            t.blocks[block_id] = b
        targets.append(t)

    # Send to main.py
    return targets, current_bg_file, project

