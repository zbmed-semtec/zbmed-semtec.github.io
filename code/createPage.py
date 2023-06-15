import os
import json

def fromMetadataToDocs():
    """
    Function that copies the subfolders of "metadata" as subfolders of "docs" and creating the subfolder if it doesn't exist.
    If the subfolder already exists, it checks if there is already a JSON file in the subfolder.
    If a JSON file exists, it is deleted and a new Markdown file is created with the content of the JSON file.
    If a JSON file doesn't exist, a new Markdown file is created directly from the JSON file with the content of the JSON file.

    Parameter/Input:
    None

    Returns:
    None
    """


    currentRoot = os.getcwd()
    rootMetadata = os.path.join(currentRoot, "metadata")
    rootDocs = os.path.join(currentRoot, "docs")

    listMetadata = os.listdir(rootMetadata)

    for counter in listMetadata:
        subfolderMetadata = os.path.join(rootMetadata, counter)
        subfolderDocs = os.path.join(rootDocs, counter)
        dataSubfolderMetadata = os.listdir(subfolderMetadata)
        
        if not os.path.exists(subfolderDocs):
            #if does not exists, creates the subfolder in "Docs"
            os.makedirs(subfolderDocs)

            newEmptyMD = os.path.join(subfolderDocs, counter + ".md")
            
            if not os.path.exists(newEmptyMD):
                open(newEmptyMD, "w").close()

            if any(fileCounter.endswith(".json") for fileCounter in dataSubfolderMetadata):
                #looks up if there is file with .json end in the subfolder from metadata
                for dataCounter in dataSubfolderMetadata:

                    if dataCounter.endswith(".json"):
                        # because there is one, it will be saved as .md in the subfolder under "docs" 
                        fromMetadata = os.path.join(subfolderMetadata, dataCounter)
                        toDocs = os.path.join(subfolderDocs, os.path.splitext(dataCounter)[0] + ".md")

                        with open(fromMetadata, "r") as jsonFile:
                            data = json.load(jsonFile)

                        with open(toDocs, "w") as mdFile:
                            json.dump(data, mdFile, indent=4)

        else:
            hasJSONFile = False
            
            for dataCounter in dataSubfolderMetadata:
                fromMetadata = os.path.join(subfolderMetadata, dataCounter)
                toDocs = os.path.join(subfolderDocs, dataCounter)

                if os.path.exists(toDocs) and dataCounter.endswith(".json"):
                    #looks up if the same the same json from "Metadata" exists in "Docs"
                    os.remove(toDocs)
                    hasJSONFile = True

                if dataCounter.endswith(".json"):
                    # after removing it it creates the new md file with the json content 
                    toDocs = os.path.splitext(toDocs)[0] + ".md"

                    with open(fromMetadata, "r") as jsonFile:
                        data = json.load(jsonFile)
                    
                    with open(toDocs, "w") as mdFile:
                        json.dump(data, mdFile, indent=4)

            if not hasJSONFile:
                    newEmptyMD = os.path.join(subfolderDocs, counter + ".md")

                    if not os.path.exists(newEmptyMD):
                        open(newEmptyMD, "w").close()




fromMetadataToDocs()