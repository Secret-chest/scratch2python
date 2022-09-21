import httpx

import json
import zipfile
import os

client = httpx.Client()


def downloadByID(projectID, location="./", zipName=None, metaInArchive=True):
    projectMetadataJSONRaw = client.get(f"https://api.scratch.mit.edu/projects/{projectID}").text
    projectMetadataJSON = json.loads(projectMetadataJSONRaw)
    projectTitle = projectMetadataJSON["title"]

    if not zipName:
        zipName = projectTitle + ".sb3"
    zipSaveName = os.path.join(location, zipName)

    with zipfile.ZipFile(zipSaveName, "w") as projectFile:
        projectJSONRaw = client.get(f"https://projects.scratch.mit.edu/{projectID}").text
        projectFile.writestr("project.json", projectJSONRaw)
        if metaInArchive:
            projectFile.writestr("metadata.json", projectMetadataJSONRaw)

        projectJSON = json.loads(projectJSONRaw)
        objectsToDownload = []
        for t in projectJSON["targets"]:
            for c in t["costumes"]:
                objectsToDownload.append(c["assetId"] + "." + c["dataFormat"])
            for s in t["sounds"]:
                objectsToDownload.append(s["assetId"] + "." + s["dataFormat"])
        for filename in objectsToDownload:
            projectFile.writestr(filename, client.get(
                f"https://cdn.assets.scratch.mit.edu/internalapi/asset/{filename}/get/").content)

    return zipSaveName
