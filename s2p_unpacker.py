# This is the Scratch2Python unpacker.
# The main file you probably want to run is located at main.py.
import zipfile as zf
import json
import target, costume, sound
from io import StringIO

# load project
project = zf.ZipFile("two_sprites.sb3", "r")
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
        targets.append(t)
