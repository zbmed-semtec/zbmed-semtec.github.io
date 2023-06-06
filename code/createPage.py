import os
import json

root = "C:/Users/Arbeit/Documents/GitHub/zbmed-semtec.github.io/"
rootMetadata = "C:/Users/Arbeit/Documents/GitHub/zbmed-semtec.github.io/metadata/"
rootDocs = "C:/Users/Arbeit/Documents/GitHub/zbmed-semtec.github.io/docs/"

listMetadata = os.listdir(rootMetadata)

list = []
for counter in listMetadata:
    subfolder = os.path.join(rootMetadata, counter)
    list.append(subfolder)

for subfolder in list:
    searchJson = [posJsons for posJsons in os.listdir(subfolder) if posJsons.endswith('.json')]
   
    for jsonData in searchJson:
        jsonPath = os.path.join(subfolder, jsonData)
        with open(jsonPath, "r") as jsonString:
            speicherJson = json.load(jsonString)

    compareName = ' '.join(searchJson)
    pointPosition = compareName.index('.')
    cuttedWord = compareName[:pointPosition]

    subfolderpath = os.path.join(rootDocs, cuttedWord)
    if  os.path.exists(subfolderpath):
        subfolderDocs = os.path.join(rootDocs, cuttedWord)
        neueNamenMD = os.path.join(subfolderDocs, cuttedWord + ".md")
        if os.path.exists(neueNamenMD):
            os.remove(neueNamenMD)
        with open(neueNamenMD, "w") as neueDateiMD:
            neueDateiMD.write(json.dumps(speicherJson, indent=4))

    else:
        os.makedirs(subfolderpath)
        neueNamenMD = os.path.join(subfolderpath, cuttedWord + ".md")
        with open(neueNamenMD, "w") as neueDateiMD:
            neueDateiMD.write(json.dumps(speicherJson, indent=4))