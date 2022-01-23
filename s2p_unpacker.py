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
import io
import pygame
import scratch


def sb3_unpack(sb3):
    # If project does not exist, quit with exit code 1
    if not Path(sb3).exists():
        print("ERROR: Project file does not exist")
        exit(1)

    print("DEBUG: Loading project")
    project = zf.ZipFile(sb3, "r")
    projectJSON = json.loads(project.read("project.json"))
    targets = []

    print("DEBUG: Project JSON output:", projectJSON)
    # Generate the dictionary based on the contents of project.json
    for targetObj in projectJSON['targets']:
        t = target.Target()

        # Set sprite values
        if "x" in targetObj:
            t.x = targetObj["x"]
            t.y = targetObj["y"]
            t.direction = targetObj["direction"]
        t.currentCostume = targetObj["currentCostume"]

        # Get costumes
        for costumeObj in targetObj["costumes"]:
            c = costume.Costume()
            if "md5ext" in costumeObj:
                c.md5ext = costumeObj["md5ext"]
                c.rotationCenterX, c.rotationCenterY = costumeObj["rotationCenterX"], costumeObj["rotationCenterY"]
            c.dataFormat = costumeObj["dataFormat"]
            c.file = project.read(costumeObj["assetId"] + "." + costumeObj["dataFormat"])
            c.bitmapResolution = int(costumeObj["bitmapResolution"])
            t.costumes.append(c)

        # Set blocks to their correct values
        for blockId, blockObj in targetObj["blocks"].items():
            b = block.Block()
            b.blockID = blockId
            b.opcode = blockObj["opcode"]
            b.next = blockObj["next"]
            b.parent = blockObj["parent"]
            b.shadow = blockObj["shadow"]
            b.topLevel = blockObj["topLevel"]
            b.inputs = blockObj["inputs"]
            b.fields = blockObj["fields"]
            b.blockRan = False
            b.target = t
            t.blocks[blockId] = b
        targets.append(t)

    return targets, project
