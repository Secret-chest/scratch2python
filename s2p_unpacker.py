# This is the Scratch2Python unpacker.
# The main file you probably want to run is located at main.py.
import zipfile as zf
import json
import target, costume, sound, block, variable, monitor  # , broadcast
from pathlib import Path
from io import StringIO


def sb3_unpack(sb3):
    if not Path(sb3).exists():
        print("ERROR: Project file does not exist")
        exit(1)
    project = zf.ZipFile(sb3, "r")
    project_json = json.loads(project.read("project.json"))
    targets = []
    print("DEBUG: Project JSON output:", project_json)
    for target_obj in project_json['targets']:
        if target_obj["isStage"]:
            current_bg_file = project.read(target_obj["costumes"][target_obj["currentCostume"]]["md5ext"])
        else:
            t = target.Target()
            t.x = target_obj["x"]
            t.y = target_obj["y"]
            t.currentCostume = target_obj["currentCostume"]
            for costume_obj in target_obj["costumes"]:
                c = costume.Costume()
                c.md5ext = costume_obj["md5ext"]
                c.file = project.read(costume_obj["md5ext"])
                t.costumes.append(c)
            for block_id, block_obj in target_obj["blocks"].items():
                b = block.Block()
                b.blockID = block_id
                b.opcode = block_obj["opcode"]
                b.next = block_obj["next"]
                b.parent = block_obj["parent"]
                b.shadow = block_obj["shadow"]
                b.topLevel = block_obj["topLevel"]
                b.inputs = block_obj["inputs"]
                b.fields = block_obj["inputs"]
                b.blockRan = False
                t.blocks[block_id] = b
            targets.append(t)
    return targets, current_bg_file, project

