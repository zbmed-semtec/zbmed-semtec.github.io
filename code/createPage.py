import os
import json
import subprocess


'''def sort_json_files(directory):
    json_files = [file for file in os.listdir(directory) if file.endswith(".json")]
    
    sorted_data = []

    for json_file in json_files:
        with open(os.path.join(directory, json_file), "r", encoding="utf-8") as file:
            data = json.load(file)
            sorted_data.append(data)

    # Hier sortieren wir die Daten anhand des Kriteriums "memberOf" und "@id"
    sorted_data.sort(key=lambda item: (
        0 if any(member.get("@id") == "https://ror.org/0259fwx54" for member in item.get("memberOf", [])) else 1
    ))

    return sorted_data'''


'''def test2():
    metadataPath = os.path.join(os.getcwd(), "metadata")
    peoplePath = os.path.join(metadataPath, "people")
    peopleDocs = os.path.join(os.path.join(os.getcwd(), "docs"), "people" + ".md")
    peopleMetadata = os.path.join(os.path.join(os.path.join(os.getcwd(), "metadata"), "people"), "people" + ".md")

    currentTeamData = []
    formerTeamData = []

    for dataCounter in os.listdir(peoplePath):
        if dataCounter.endswith(".json"):
            with open(os.path.join(peoplePath, dataCounter), "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)

            if isinstance(data, dict):
                memberOf = data.get("memberOf", [])
                if any(isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54" for item in memberOf):
                    currentTeamData.append(data)
                else:
                    formerTeamData.append(data)

    restoredData = currentTeamData + formerTeamData

    with open(peopleDocs, "w", encoding="utf-8") as docsFile:
        for item in restoredData:
            currentTeamData
    with open(peopleMetadata, "w", encoding="utf-8") as metadataFile:
        for item in restoredData:
            formerTeamData'''





def test():
    metadataPath = os.path.join(os.getcwd(), "metadata")
    peoplePath = os.path.join(metadataPath, "people")
    peopleDocs = os.path.join(os.path.join(os.getcwd(), "docs"), "people" + ".md")
    peopleMetadata = os.path.join(os.path.join(os.path.join(os.getcwd(), "metadata"), "people"), "people" + ".md")

    currentTeamData = []
    formerTeamData = []

    for dataCounter in os.listdir(peoplePath):
        if dataCounter.endswith(".json"):
            with open(os.path.join(peoplePath, dataCounter), "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)

            if isinstance(data, dict):
                memberOf = data.get("memberOf", [])
                if any(isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54" for item in memberOf):
                    currentTeamData.append(data)
                else:
                    formerTeamData.append(data)

#    with open(peopleDocs, "w", encoding="utf-8") as mdFile:
#        mdFile.write("## Current Team\n\n")
#        json.dump(currentTeamData, mdFile, indent=4)
#
#        mdFile.write("\n\n## Former Team\n\n")
#        json.dump(formerTeamData, mdFile, indent=4)

#    MDdata = {
#        "current Team": currentTeamData,
#        "former Team": formerTeamData
#    }

    generateCombinedMDTable(currentTeamData, formerTeamData, peopleDocs, "People", "")



'''def test():
metadataPath = os.path.join(os.getcwd(), "metadata")
peoplePath = os.path.join(metadataPath, "people")
peopleDocs = os.path.join(os.path.join(os.getcwd(), "docs"), "people" + ".md")
peopleMetadata = os.path.join(os.path.join(os.path.join(os.getcwd(), "metadata"), "people"), "people" + ".md")

currentTeamData = []
formerTeamData = []

for dataCounter in os.listdir(peoplePath):
    if dataCounter.endswith(".json"):
        with open(os.path.join(peoplePath, dataCounter), "r", encoding="utf-8") as jsonFile:
            data = json.load(jsonFile)

        if isinstance(data, dict):
            memberOf = data.get("memberOf", [])
            if any(isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54" for item in memberOf):
                currentTeamData.append(data)
            else:
                formerTeamData.append(data)

    
    with open(peopleDocs, "w", encoding="utf-8") as mdFile:
        mdFile.write("## Current Team\n\n")
        json.dump(currentTeamData, mdFile, indent=4)

        mdFile.write("\n\n## Former Team\n\n")
        json.dump(formerTeamData, mdFile, indent=4)

    MDdata = {
        "current Team": currentTeamData,
        "former Team": formerTeamData
    }

generateCombinedMDTable(currentTeamData, formerTeamData, outputFile, folderName, jsonFile)'''
#complexDataInList(mdFile)
#generateMDTableFromJSON(mdFile, peopleDocs, "People", "")
    #print(currentTeamData)
#generateMDTableFromJSON(peopleDocs, peopleDocs, "people", "")
#generateMDTableFromJSON(currentTeamData, peopleDocs, "people", "link_to_json_data.json")
#AnotherJsonInSubfolder(formerTeamData, peopleDocs, "link_to_json_data.json")



def generateCombinedMDTable(currentTeamData, formerTeamData, outputFile, folderName, jsonFile):

    md = f'# {folderName.capitalize()} metadata\n\n'

    md += f'## {"current Team Members".capitalize()}\n\n'

    for item in currentTeamData:
        if "@id" in item:
            idValue = item["@id"]
            if "metadata" in idValue:
                cuttedOwnPath = idValue.split("metadata", 1)[-1]
            else:
                cuttedOwnPath = idValue.split("#", 1)[-1]
                if cuttedOwnPath.startswith("http"):
                     cuttedOwnPath = cuttedOwnPath.split("/", 3)[-1]
            cuttedCurrentGitUrl = getCurrentGitUrl().rsplit(".git", 1)[0]
            pathToJsonData = cuttedCurrentGitUrl + "/blob/main/metadata/people/" + cuttedOwnPath + ".json"

    linkValue = currentTeamData[0].get("@link", "")
    if linkValue:
        md += f'<p><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7V32zM64 352c-35.3 0-64 28.7-64 64v32c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V416c0-35.3-28.7-64-64-64H346.5l-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352H64zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/></svg><a href="{jsonFile}" target="_blank"> Get JSON-LD</a> | {linkValue}</p>\n'
        currentTeamData[0].pop("@link", None)

    for item in currentTeamData:

        if "givenName" in item and "familyName" in item:
            familyName = item.get("familyName", "")
            md += f'### {renderProperty("Name", item["givenName"] + " " + familyName)}\n'
        elif "familyName" in item and "givenName" not in item:
            md += f'### {renderProperty("Name", item["familyName"])}\n'

        md += '<table style="background-color: #F5F5F5; width: 100%; text-align: left; border: 1px solid black;">\n<tbody>\n'
        
        for property, value in item.items():
            if property == "@id":
                property = "ID"
                typeValue = item.get("@type", "")
                value = f'<a href="{value}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit {typeValue}</a>'
            if property not in ["@type", "@context", "http://purl.org/dc/terms/conformsTo"]:
                if isinstance(value, list):
                    md += f'<tr>\n<td>{property}</td>\n<td><ul>{renderInnerList(value)}</ul></td>\n</tr>\n'
                else:
                    renderedValue = renderProperty(property, value)
                    if renderedValue is not None:   
                        md += f'<tr>\n<td>{property}</td>\n<td>{renderedValue}</td>\n</tr>\n'

        md += '</tbody>\n</table>'

    #formerTeamData = complexDataInList(formerTeamData)
    #formerTeamData = createTableLink(formerTeamData)

    md += f'## {"former Team Members".capitalize()}\n\n'

    formerTeamData = complexDataInList(formerTeamData)
    formerTeamData = createTableLink(formerTeamData)


    linkValue = formerTeamData[0].get("@link", "")
    if linkValue:
        md += f'<p><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7V32zM64 352c-35.3 0-64 28.7-64 64v32c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V416c0-35.3-28.7-64-64-64H346.5l-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352H64zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/></svg><a href="{jsonFile}" target="_blank"> Get JSON-LD</a> | {linkValue}</p>\n'
        currentTeamData[0].pop("@link", None)

    for item in formerTeamData:

        if "@id" in item:
            idValue = item["@id"]
            if "metadata" in idValue:
                cuttedOwnPath = idValue.split("metadata", 1)[-1]
            else:
                cuttedOwnPath = idValue.split("#", 1)[-1]
                if cuttedOwnPath.startswith("http"):
                     cuttedOwnPath = cuttedOwnPath.split("/", 3)[-1]
            cuttedCurrentGitUrl = getCurrentGitUrl().rsplit(".git", 1)[0]
            pathToJsonData = cuttedCurrentGitUrl + "/blob/main/metadata/people/" + cuttedOwnPath + ".json"

        if "givenName" in item and "familyName" in item:
            familyName = item.get("familyName", "")
            md += f'### {renderProperty("Name", item["givenName"] + " " + familyName)}\n'
        elif "familyName" in item and "givenName" not in item:
            md += f'### {renderProperty("Name", item["familyName"])}\n'

        md += '<table style="background-color: #F5F5F5; width: 100%; text-align: left; border: 1px solid black;">\n<tbody>\n'

        for property, value in item.items():
            if property == "@id":
                property = "ID"
                typeValue = item.get("@type", "")
                value = f'<a href="{value}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit {typeValue}</a>'
            if property not in ["@type", "@context", "http://purl.org/dc/terms/conformsTo"]:
                if isinstance(value, list):
                    md += f'<tr>\n<td>{property}</td>\n<td><ul>{renderInnerList(value)}</ul></td>\n</tr>\n'
                else:
                    renderedValue = renderProperty(property, value)
                    if renderedValue is not None:   
                        md += f'<tr>\n<td>{property}</td>\n<td>{renderedValue}</td>\n</tr>\n'
        #appendScriptToMDFile(pathToJsonData, md)
        md += '</tbody>\n</table>'

    with open(outputFile, "w", encoding="utf-8") as file:
        file.write(md)

        
'''
# Nach der letzten if else zweig
    with open("CurrentTeam.json", "w", encoding="utf-8") as currentTeamFile:
        currentTeamFile.write("## Current Team\n\n")
        json.dump(currentTeamData, currentTeamFile, indent=4)

    
    with open("FormerTeam.json", "w", encoding="utf-8") as formerTeamFile:
        formerTeamFile.write("## Former Team\n\n")
        json.dump(formerTeamData, formerTeamFile, indent=4)

    with open("combinedTeam.json", 'w', encoding="utf-8") as combinedTeamFile:
        with open("CurrentTeam.json", "r", encoding="utf-8") as currentTeamFile:
            combinedTeamFile.write(currentTeamFile.read())
        
        combinedTeamFile.write('\n---\n\n')
        
        with open("FormerTeam.json", 'r', encoding="utf-8") as formerTeamFile:
            combinedTeamFile.write(formerTeamFile.read())'''
            
        

    


'''def test():
    MetadataPath = os.path.join(os.getcwd(), "metadata")
    PeoplePath = os.path.join(MetadataPath, "people")
    PeopleDocs = os.path.join(os.path.join(os.getcwd(), "docs"), "people")

    currentTeamData = []
    formerTeamData = []

    for dataCounter in os.listdir(PeoplePath):
        if dataCounter.endswith(".json"):
            with open(os.path.join(PeoplePath, dataCounter), "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)

            if isinstance(data, dict):
                memberOf = data.get("memberOf", [])
                if any(isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54" for item in memberOf):
                    currentTeamData.append(data)
                else:
                    formerTeamData.append(data)

    
    with open("CurrentTeam.md", "w", encoding="utf-8") as currentTeamFile:
        currentTeamFile.write("## Current Team\n\n")
        json.dump(currentTeamData, currentTeamFile, indent=4)

    
    with open("FormerTeam.md", "w", encoding="utf-8") as formerTeamFile:
        formerTeamFile.write("## Former Team\n\n")
        json.dump(formerTeamData, formerTeamFile, indent=4)

    
    combinedData = {
        "currentTeam": currentTeamData,
        "formerTeam": formerTeamData
    }

    
    with open("CombinedData.md", "w", encoding="utf-8") as combinedFile:
        json.dump(combinedData, combinedFile, indent=4)

    
    generateMDTableFromJSON(combinedData, PeopleDocs, "People", "test")'''





'''def test():
    MetadataPath = os.path.join(os.getcwd(), "metadata")
    PeoplePath = os.path.join(MetadataPath, "people")
    PeopleDocs = os.path.join(os.path.join(os.getcwd(), "docs"), "people")

    currentTeamData = []
    formerTeamData = []

    for dataCounter in os.listdir(PeoplePath):
        if dataCounter.endswith(".json"):
            with open(os.path.join(PeoplePath, dataCounter), "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)

            if isinstance(data, dict):
                memberOf = data.get("memberOf", [])
                if any(isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54" for item in memberOf):
                    currentTeamData.append(data)
                else:
                    formerTeamData.append(data)

    
    with open("CurrentTeam.md", "w", encoding="utf-8") as currentTeamFile:
        currentTeamFile.write("## Current Team\n")
        json.dump(currentTeamData, currentTeamFile, indent=4)

    
    with open("FormerTeam.md", "w", encoding="utf-8") as formerTeamFile:
        formerTeamFile.write("## Former Team\n")
        json.dump(formerTeamData, formerTeamFile, indent=4)

    
    combinedData = {
        "currentTeam": currentTeamData,
        "formerTeam": formerTeamData
    }

    
    with open("CombinedData.json", "w", encoding="utf-8") as combinedFile:
        json.dump(combinedData, combinedFile, indent=4)

    
    generateMDTableFromJSON(combinedData, PeopleDocs, "People", "test")'''






'''def test():
    MetadataPath = os.path.join(os.getcwd(), "metadata")
    PeoplePath = os.path.join(MetadataPath, "people")
    PeopleDocs = (os.path.join(os.path.join(os.getcwd(), "docs"), "people"))

    currentTeamData = []
    formerTeamData = []

    for dataCounter in os.listdir(PeoplePath):
        if dataCounter.endswith(".json"):
            with open(os.path.join(PeoplePath, dataCounter), "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)

            if isinstance(data, dict):
                memberOf = data.get("memberOf", [])
                if any(isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54" for item in memberOf):
                    currentTeamData.append(data)
                else:
                    formerTeamData.append(data)

    
    with open("CurrentTeam", "w", encoding="utf-8") as currentTeamFile:
        currentTeamFile.write("## Current Team\n")
        json.dump(currentTeamData, currentTeamFile, indent=4)

    
    with open("FormerTeam", "w", encoding="utf-8") as formerTeamFile:
        formerTeamFile.write("## Former Team\n")
        json.dump(formerTeamData, formerTeamFile, indent=4)

    
    combinedData = {
        "currentTeam": currentTeamData,
        "formerTeam": formerTeamData
    }

    with open("CombinedData.md", "w", encoding="utf-8") as combinedFile:
        json.dump(combinedData, combinedFile, indent=4)

    generateMDTableFromJSON(combinedFile, PeopleDocs, "People", "test")'''


'''def test():
    MetadataPath = os.path.join(os.getcwd(), "metadata")
    PeoplePath = os.path.join(MetadataPath, "people")

    for dataCounter in os.listdir(PeoplePath):
        if dataCounter.endswith(".json"):
            jsonFilePath = os.path.join(PeoplePath, dataCounter)

            with open(jsonFilePath, "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)

            if isinstance(data, dict):
                memberOf = data.get("memberOf", [])
                if any(isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54" for item in memberOf):
                    currentTeamPath = os.path.join(PeoplePath, "CurrentTeam.md")
                    with open(currentTeamPath, "w", encoding="utf-8") as currentTeam:
                        currentTeam.write("## Current Team\n")
                        json.dump(data, currentTeam, indent=4)
                else:
                    formerTeamPath = os.path.join(PeoplePath, "FormerTeam.md")
                    with open(formerTeamPath, "w", encoding="utf-8") as formerTeam:
                        formerTeam.write("## Former Team\n")
                        json.dump(data, formerTeam, indent=4)'''




'''def test():

    MetadataPath = os.path.join(os.getcwd(), "metadata")
    PeoplePath = os.path.join(MetadataPath, "people")


    for dataCounter in os.listdir(PeoplePath):
        if dataCounter.endswith(".json"):

            with open(dataCounter, "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)

            if isinstance(data, dict):
                memberOf = data.get("memberOf", [])
                if any(isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54" for item in memberOf):
                    #memberFiles.append(data)
                    with open(data, "w", encoding="utf-8") as currentTeam:
                        currentTeam.write("## Current Team\n")
                        json.dump(data, currentTeam, indent=4)
                else:
                    with open(data, "w", encoding="utf-8") as formerTeam:
                        formerTeam.write("## Current Team\n")
                        json.dump(data, formerTeam, indent=4)
                        print(formerTeam)'''


'''def processPeopleSubfolder(rootMetadata, counter):
    metadataFilePath = os.path.join(rootMetadata, counter, "metadata.json")
    
    with open(metadataFilePath, "r", encoding="utf-8") as jsonFile:
        metadata = json.load(jsonFile)
    
    if "CurrentTeam.json" in metadata:
        currentTeamFilePath = os.path.join(rootMetadata, counter, metadata["CurrentTeam.json"])
        
        with open(currentTeamFilePath, "r", encoding="utf-8") as jsonFile:
            currentTeamData = json.load(jsonFile)
        
        outputFolder = os.path.join(rootMetadata, counter, "output")
        os.makedirs(outputFolder, exist_ok=True)
        
        outputFileName = "CurrentTeam.md"
        outputFile = os.path.join(outputFolder, outputFileName)
        
        generateMDTableFromJSON(currentTeamData, outputFile, "Current Team", "CurrentTeam.json")
    else:
        print(f"Metadata for 'CurrentTeam.json' not found for {counter}")'''


'''def processPeopleSubfolder(peopleFolder):
    currentMember = []
    formerMember = []

    for dataCounter in os.listdir(peopleFolder):
        if dataCounter.endswith(".json"):
            fromMetadata = os.path.join(peopleFolder, dataCounter)

            with open(fromMetadata, "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)

            if isinstance(data, dict):
                memberOf = data.get("memberOf", [])
                if any(isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54" for item in memberOf):
                    currentMember.append(data)
                else:
                    formerMember.append(data)

    currentOutputFile = "CurrentTeam.json"
    formerOutputFile = "FormerTeam.json"

    with open(currentOutputFile, "w", encoding="utf-8") as currentFile:
        json.dump(currentMember, currentFile, indent=4)

    with open(formerOutputFile, "w", encoding="utf-8") as formerFile:
        json.dump(formerMember, formerFile, indent=4)

    generateMDTableFromJSON(currentMember, "CurrentTeam.md", "Current Team", "CurrentTeam.json")
    generateMDTableFromJSON(formerMember, "FormerTeam.md", "Former Team", "FormerTeam.json")

    appendScriptToMDFile("CurrentTeam.json", "CurrentTeam.md")
    appendScriptToMDFile("FormerTeam.json", "FormerTeam.md")'''



'''def sortPeopleFolder(peopleFolder):

    memberFiles = []
    otherFiles = []

    for dataCounter in os.listdir(peopleFolder):
        if dataCounter.endswith(".json"):
            fromMetadata = os.path.join(peopleFolder, dataCounter)

            with open(fromMetadata, "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)

            if isinstance(data, dict):
                memberOf = data.get("memberOf", [])
                if any(isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54" for item in memberOf):
                    memberFiles.append(data)
                else:
                    otherFiles.append(data)

    sortedFiles = memberFiles + otherFiles
    return sortedFiles'''



'''def Membership2():
    currentMembers = []
    formerMembers = []

    currentRoot = os.getcwd()
    rootMetadata = os.path.join(currentRoot, "metadata")
    peopleMetadata = os.path.join(rootMetadata, "people")

    for dataCounter in os.listdir(peopleMetadata):
        if dataCounter.endswith(".json"):
            fromMetadata = os.path.join(peopleMetadata, dataCounter)

            with open(fromMetadata, "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)

            if isinstance(data, dict):
                memberOf = data.get("memberOf", [])
                if any(isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54" for item in memberOf):
                    currentMembers.append(data)
                else:
                    formerMembers.append(data)

    return currentMembers, formerMembers'''




'''def sortAndAppendTables(jsonData):
    """
    Sorts the team members into current and former team members.

    Parameter/Input:
        jsonData: The JSON data containing the team members.

    Returns:
        The updated Markdown content with sorted team members.
    """
    currentTeam = []
    formerTeam = []

    if "memberOf" in jsonData:
        memberOf = jsonData["memberOf"]
        if isinstance(memberOf, list):
            for item in memberOf:
                if isinstance(item, dict) and item.get("@id") == "https://ror.org/0259fwx54":
                    currentTeam.append(json.dumps(item, indent=4))
                else:
                    formerTeam.append(json.dumps(item, indent=4))

    if "alumniOf" in jsonData:
        alumniOf = jsonData["alumniOf"]
        if isinstance(alumniOf, list):
            for item in alumniOf:
                formerTeam.append(json.dumps(item, indent=4))

    md = ""

    # Append the sorted tables to the markdown file
    if currentTeam:
        md += "<h3>Current team member</h3>"

    if formerTeam:
        md += "<h3>Former team member</h3>"

    return md'''









def createTableLink(data):
    """
    Checks the JSON data if there is @id and @type. If both exists the link will be created 
    with the value of @id

    Parameter/Input:
        data: The JSON data, which should be checked

    Returns:
        created Link für the Table
    """
    if not isinstance(data, dict):
        return data
    
    idValue = data.get("@id", "")
    typeValue = data.get("@type", "")

    if idValue and typeValue:
        # Only if @id and @type are in the data and the valaue are saved then create link
        visitLink = f'<a href="{idValue}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit {typeValue}</a>'
        data["@link"] = visitLink
    return data



def complexDataInList(data):
    """
    Converts complex JSON element into a single element list.

    Parameter/Input:
        data: The JSON data to be converted.

    Returns:
        The converted complex JSON Data in a single element list.
    """
    if not isinstance(data, dict):
        return data

    complexData = {}
    for property, value in data.items():
        if isinstance(value, list):
            # The case if inside a complex element is another complex element so it repeats itself. 
            complexData[property] = [complexDataInList(item) for item in value]
            # It should be represented as an table.
        elif isinstance(value, dict):
            complexData[property] = [value]
        else:
            #it will be handled as a simple element.
            complexData[property] = complexDataInList(value)

    return complexData



def getCurrentGitUrl():
    """
    Returns the URL of the current Git repository.

    Parameter/Input:
        None

    Returns:
        The URL of the current Git repository as a String.
    """
    url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url']).decode().strip()
    # first part retrieves the output of "git config --get remote.origin.url" command as a byte string.
    # decode() decodes the byte string into a normal String, strip() removes unnecessary spaces and line breaks
    return url
    


def appendScriptToMDFile(jsonFile, mdFile):
    """
    Appending the script to the new Markdown file.

    Parameter/Input:
        jsonFile: The JSON file whose content should be appended.
        mdFile: The newly created Markdown file which the jsonFile should bet attached to.

    Returns:
        None
    """
    with open(jsonFile, "r", encoding="utf-8") as jsonFile:
        scriptCode = json.load(jsonFile)

    with open(mdFile, "a", encoding="utf-8") as file:
        file.write(f'\n\n<script type="application/ld+json">\n{json.dumps(scriptCode, indent=4)}\n</script>\n\n')
        


def renderProperty(propertyName, propertyValue):
    """
    Function, which renders the property values as HTML.

    Paramater/Input:
        propertyName: The name of the property.
        propertyValue: The value of the property.

    Returns:
        The representation of the property value in HTML.
    """
    if isinstance(propertyValue, dict):
        return renderInnerTable(propertyValue)
    elif isinstance(propertyValue, list):
        return renderInnerList(propertyValue)
    elif isinstance(propertyValue, str) and propertyValue.startswith("http"):
        return f'<a href="{propertyValue}" target="_blank">{propertyValue}</a>'
    else:
        return str(propertyValue)



def renderInnerTable(obj):
    """
    Function, which renders a nested table as HTML.

    Paramater/Input:
        obj (dict): The nested object which will be rendered

    Returns:
        The representation of the nested table in HTML.
    """
    tableMD = ""
    valueInnerType = ""
    for propertyInner, valueInner in obj.items():
        if propertyInner == "@id":
            link = fr'<a href="{valueInner}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit {valueInnerType} Object</a>'
            tableMD += f"\n<tr>{link}\n</tr>"
        elif propertyInner == "@type":
            valueInnerType = valueInner
        else:
            # Render other properties as usual
            renderedInnerValue = renderProperty(propertyInner, valueInner)
            if renderedInnerValue is not None:
                tableMD += f"\n<tr>\n<td>{propertyInner}</td>\n<td>{renderedInnerValue}</td>\n</tr>"

    return tableMD



def renderInnerList(lst):
    """
    Function, which renders a nested list as HTML.

    Parameter/Input:
        lst: The nested list to render.

    Returns:
        The representation of the nested list in HTML.
    """
    listMD = ""
    for item in lst:
        if isinstance(item, dict):
            listMD += f'\n<li><table style="background-color: #F5F5F5; width: 100%; text-align: left; border: 1px solid black; border-right: 1px solid black;">\n<tbody>{renderInnerTable(item)}</tbody>\n</table></li>'
        elif isinstance(item, list):
            listMD += f'\n<li>{renderInnerList(item)}</li>'
        elif isinstance(item, str) and item.startswith("@id"):
            itemID = item.split(":")[1]
            itemURL = generateMDTableFromJSON.jsonData[itemID]
            itemType = generateMDTableFromJSON.jsonData[itemID].get("@type", "")
            link = f'<a href="{itemURL}" target="_blank"> Visit object</a>'
            listMD += f'\n<li>{itemType} - {link}</li>'
        else:
            listMD += f"\n<li>{renderProperty('', item)}</li>"
        listMD += "\n<hr></hr>"
    return listMD



def generateMDTableFromJSON(jsonData, outputFile, FolderName, jsonFile):
    """
    Generate a Markdown file from JSON data.

    Parameter/Input:
        jsonData: The JSON data to convert.
        outputFile: The path to the output file with the Markdown code.
        FolderName: The name of the folder used for the title.
        jsonFile: The link to the JSON-LD file associated with the metadata.

    Returns:
        None
    """
    md = f'# {FolderName.capitalize()} metadata\n\n'

    #jsonData.pop("memberOf", None)
    #jsonData.pop("alumniOf", None)
    jsonData = complexDataInList(jsonData)
    jsonData = createTableLink(jsonData)

    for property, value in jsonData.items():
        if property == "name":
            md += f'## {renderProperty(property, value)}\n'
        if property == "givenName" and "familyName" in jsonData:
            familyName = jsonData.get("familyName", "")
            md += f'### {renderProperty("Name", value + " " + familyName)}\n'
        if property == "familyName" and "givenName" not in jsonData:
            md += f'### {renderProperty("Name", value)}\n'

    #md += sortAndAppendTables(jsonData)

    linkValue = jsonData.get("@link", "")
    if linkValue:
        md += f'<p><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7V32zM64 352c-35.3 0-64 28.7-64 64v32c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V416c0-35.3-28.7-64-64-64H346.5l-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352H64zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/></svg><a href="{jsonFile}" target="_blank"> Get JSON-LD</a> | {linkValue}</p>\n'
    jsonData.pop("@link", None)

    md += '<table style="background-color: #F5F5F5; width: 100%; text-align: left; border: 1px solid black;">\n<tbody>\n'
    
    for property, value in jsonData.items():
        if property not in ["@type", "@id", "@context", "http://purl.org/dc/terms/conformsTo"]:
            if isinstance(value, list):
                md += f'<tr>\n<td>{property}</td>\n<td><ul>{renderInnerList(value)}</ul></td>\n</tr>\n'
            else:
                renderedValue = renderProperty(property, value)
                if renderedValue is not None:   
                    md += f'<tr>\n<td>{property}</td>\n<td>{renderedValue}</td>\n</tr>\n'
    md += '</tbody>\n</table>'

    with open(outputFile, "w", encoding="utf-8") as file:
       file.write(md)



def AnotherJsonInSubfolder(jsonData, outputFile, jsonFile):
    """
    Similar method like "generateMDTableFromJSON" to append the following JSON files to the first one.

    Parameter/Input:
        jsonData: The JSON data to convert.
        outputFile: The path to the output file with the Markdown code.
        jsonFile: The link to the JSON-LD file associated with the metadata.

    Returns:
        None
    """
    md = ""
    jsonData = complexDataInList(jsonData)
    jsonData = createTableLink(jsonData)

    for property, value in jsonData.items():
        if property == "name":
            md += f'## {renderProperty(property, value)}\n'
        if property == "givenName" and "familyName" in jsonData:
            familyName = jsonData.get("familyName", "")
            md += f'### {renderProperty("Name", value + " " + familyName)}\n'
        if property == "familyName" and "givenName" not in jsonData:
            md += f'### {renderProperty("Name", value)}\n'

    #md += sortAndAppendTables(jsonData)

    linkValue = jsonData.get("@link", "")
    if linkValue:
        md += f'<p><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7V32zM64 352c-35.3 0-64 28.7-64 64v32c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V416c0-35.3-28.7-64-64-64H346.5l-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352H64zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/></svg><a href="{jsonFile}" target="_blank"> Get JSON-LD</a> | {linkValue}</p>\n'
    jsonData.pop("@link", None)

    md += '<table style="background-color: #F5F5F5; width: 100%; text-align: left; border: 1px solid black;">\n<tbody>\n'
    
    for property, value in jsonData.items():
        if property not in ["@type", "@id", "@context", "http://purl.org/dc/terms/conformsTo"]:
            if isinstance(value, list):
                md += f'<tr>\n<td>{property}</td>\n<td><ul>{renderInnerList(value)}</ul></td>\n</tr>\n'
            else:
                renderedValue = renderProperty(property, value)
                if renderedValue is not None:   
                    md += f'<tr>\n<td>{property}</td>\n<td>{renderedValue}</td>\n</tr>\n'
    md += '</tbody>\n</table>'

   

    with open(outputFile, "a", encoding="utf-8") as file:
       file.write(md)



'''def generateMDTableFromJSONList(jsonList, outputFile, FolderName, jsonFile):
    """
    Generate a Markdown file from a list of JSON data.

    Parameters:
        jsonList: The list of JSON data to convert.
        outputFile: The path to the output file with the Markdown code.
        FolderName: The name of the folder used for the title.
        jsonFile: The link to the JSON-LD file associated with the metadata.

    Returns:
        None
    """
    # Load the JSON data from the provided file
    with open(jsonFile, "r", encoding="utf-8") as jsonFile:
        jsonData = json.load(jsonFile)

    # Create the Markdown header
    md = f'# {FolderName.capitalize()} metadata\n\n'

    # Iterate through each entry in the JSON list
    for entry in jsonList:
        # Process each entry in the list
        entryData = complexDataInList(entry)
        entryData = createTableLink(entryData)

        # Iterate through each property and value in the entry data
        for property, value in entryData.items():
            # Check if the property value is a list
            if isinstance(value, list):
                # Render inner lists as HTML and append to Markdown
                md += f'\n## {property}\n<ul>'
                for item in value:
                    md += f'\n<li>{renderProperty("", item)}</li>'
                md += '\n</ul>'
            else:
                # Render other properties as HTML and append to Markdown
                md += f'\n## {property}\n<p>{renderProperty("", value)}</p>'

        md += '\n\n---\n\n'

    # Write the generated Markdown content to the output file
    with open(outputFile, "a", encoding="utf-8") as file:
        file.write(md)'''



'''def generateMDTableFromJSONList(jsonList, outputFile, FolderName):
    """
    Generate a Markdown file from a list of JSON data.

    Parameters:
        jsonList: The list of JSON data to convert.
        outputFile: The path to the output file with the Markdown code.
        FolderName: The name of the folder used for the title.

    Returns:
        None
    """
    # Create the Markdown header
    md = f'# {FolderName.capitalize()} metadata\n\n'

    # Iterate through each entry in the JSON list
    for entry in jsonList:
        # Process each entry in the list
        entryData = complexDataInList(entry)
        entryData = createTableLink(entryData)

        # Iterate through each property and value in the entry data
        for property, value in entryData.items():
            # Check if the property value is a list
            if isinstance(value, list):
                # Render inner lists as HTML and append to Markdown
                md += f'\n## {property}\n<ul>'
                for item in value:
                    md += f'\n<li>{renderProperty("", item)}</li>'
                md += '\n</ul>'
            else:
                # Render other properties as HTML and append to Markdown
                md += f'\n## {property}\n<p>{renderProperty("", value)}</p>'

        md += '\n\n---\n\n'

    # Write the generated Markdown content to the output file
    with open(outputFile, "a", encoding="utf-8") as file:
        file.write(md)'''






def fromMetadatatoDocs():
    """
    Function that copies the subfolders of "metadata" as Markdown files in "docs" folder.
    If a JSON file exists in the subfolder, a new Markdown file is created with the content of the JSON file.
    The content of the JSON file is appended at the end of the Markdown file.

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
        subfolderDocs = rootDocs
        dataSubfolderMetadata = os.listdir(subfolderMetadata)
        if counter == "people":
        #   peopleDocs = os.path.join(os.path.join(os.getcwd(), "docs"), "people" + ".md")
        #    sorted = sort_json_files(subfolderMetadata)
        #    print(sorted)
        #    complexDataInList(sorted)
        #    generateCombinedMDTable(sorted, sorted, peopleDocs, counter, jsonFile)
            #print(toDocs)
            #print(os.path.join(rootDocs, "people" + ".md"))
            #print(os.path.join(subfolderDocs, counter + ".md"))
            '''toDocs = os.path.join(subfolderDocs, counter + ".md")
            cuttedOwnPath = fromMetadata[fromMetadata.index("metadata"):]
            #cutted from the right site ".git", which is important for the path
            cuttedCurrentGitUrl = getCurrentGitUrl().rsplit(".git", 1)[0]
            pathToJsonData = cuttedCurrentGitUrl + "/blob/main/" + cuttedOwnPath'''

            #test2()
            #processPeopleSubfolder(rootMetadata ,(os.path.join(rootMetadata, counter)))
            '''toDocs = os.path.join(subfolderDocs, counter + ".md")
            fromMetadata = subfolderMetadata
            cuttedOwnPath = fromMetadata[fromMetadata.index("metadata"):]
            #cutted from the right site ".git", which is important for the path
            cuttedCurrentGitUrl = getCurrentGitUrl().rsplit(".git", 1)[0]
            pathToJsonData = cuttedCurrentGitUrl + "/blob/main/" + cuttedOwnPath

            sortedPeopleData = sortPeopleFolder(fromMetadata)

        with open(toDocs, "a", encoding="utf-8") as mdFile:
            for sortedData in sortedPeopleData:
                json.dump(sortedData, mdFile, indent=4)
                mdFile.write("\n\n")

        appendScriptToMDFile(sortedPeopleData[0], toDocs)'''

        #generateMDTableFromJSON(data, toDocs, counter, pathToJsonData)

        ''' toDocs = os.path.join(subfolderDocs, counter + ".md")
            fromMetadata = subfolderMetadata
            cuttedOwnPath = fromMetadata[fromMetadata.index("metadata"):]
            #cutted from the right site ".git", which is important for the path
            cuttedCurrentGitUrl = getCurrentGitUrl().rsplit(".git", 1)[0]
            pathToJsonData = cuttedCurrentGitUrl + "/blob/main/" + cuttedOwnPath

            sortedMembers = Membership()

            with open(toDocs, "a", encoding="utf-8") as mdFile:
                json.dump(sortedMembers, mdFile, indent=4)
            
            generateMDTableFromJSON(sortedMembers, toDocs, counter, pathToJsonData)
            appendScriptToMDFile(fromMetadata, toDocs)'''


        if any(fileCounter.endswith(".json") for fileCounter in dataSubfolderMetadata):
            # Looks up if there is a JSON file with .json extension in the subfolders from "metadata"
            firstJsonFile = None
            for dataCounter in dataSubfolderMetadata:
                if dataCounter.endswith(".json"):
                    # Because there is one, it will be saved as .md in the "docs" folder
                    fromMetadata = os.path.join(subfolderMetadata, dataCounter)
                    toDocs = os.path.join(subfolderDocs, counter + ".md")

                    cuttedOwnPath = fromMetadata[fromMetadata.index("metadata"):]
                    #cutted from the right site ".git", which is important for the path
                    cuttedCurrentGitUrl = getCurrentGitUrl().rsplit(".git", 1)[0]
                    pathToJsonData = cuttedCurrentGitUrl + "/blob/main/" + cuttedOwnPath
                    

                    #if there is JSON file
                    if firstJsonFile is None:
                        firstJsonFile = True
                        with open(fromMetadata, "r", encoding="utf-8") as jsonFile:
                            data = json.load(jsonFile)

                        with open(toDocs, "a", encoding="utf-8") as mdFile:
                            json.dump(data, mdFile, indent=4)

                        generateMDTableFromJSON(data, toDocs, counter, pathToJsonData)
                        appendScriptToMDFile(fromMetadata, toDocs)
                    else:
                        #if there is another JSON file in the same subfolder
                        with open(fromMetadata, "r", encoding="utf-8") as jsonFile:
                            data = json.load(jsonFile)
                        with open(toDocs, "a", encoding="utf-8") as mdFile:

                            AnotherJsonInSubfolder(data, toDocs, pathToJsonData)     
                            appendScriptToMDFile(fromMetadata, toDocs)
        else:
            newEmptyMD = os.path.join(subfolderDocs, counter + ".md")

            if not os.path.exists(newEmptyMD):
                open(newEmptyMD, "w", encoding="utf-8").close()



fromMetadatatoDocs()
test()