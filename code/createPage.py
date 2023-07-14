import os
import json
import subprocess


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
    with open(jsonFile, "r") as jsonFile:
        scriptCode = json.load(jsonFile)

    with open(mdFile, "a") as file:
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
    for propertyInner, valueInner in obj.items():
        if propertyInner == "@id":
            # Replace the value of the "@id" key with a link
            link = fr'<a href="{valueInner}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit object</a>'
            tableMD += f"\n<tr>{link}\n</tr>"
        elif propertyInner == "@type":
            tableMD += f"\n<tr>\n{valueInner} - \n</tr>"
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

    Returns:
        None
    """
    md = f'# {FolderName.capitalize()} metadata\n\n'
    for property, value in jsonData.items():
        if property == "name":
            md += f'## {renderProperty(property, value)}\n'
    md += f'<p><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7V32zM64 352c-35.3 0-64 28.7-64 64v32c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V416c0-35.3-28.7-64-64-64H346.5l-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352H64zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/></svg><a href="{jsonFile}" target="_blank"> Get JSON-LD</a></p>\n'
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

    with open(outputFile, "w") as file:
       file.write(md)



def AnotherJsonInSubfolder(jsonData, outputFile, jsonFile):
    """
    Similar method like "generateMDTableFromJSON" to append the following JSON files to the first one.

    Parameter/Input:
        jsonData: The JSON data to convert.
        outputFile: The path to the output file with the Markdown code.

    Returns:
        None
    """
    md = ""
    for property, value in jsonData.items():
        if property == "name":
            md += f'## {renderProperty(property, value)}\n'
    md += f'<p><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7V32zM64 352c-35.3 0-64 28.7-64 64v32c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V416c0-35.3-28.7-64-64-64H346.5l-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352H64zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/></svg><a href="{jsonFile}" target="_blank"> Get JSON-LD test</a></p>\n'
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

    with open(outputFile, "a") as file:
       file.write(md)



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
                        with open(fromMetadata, "r") as jsonFile:
                            data = json.load(jsonFile)

                        with open(toDocs, "a") as mdFile:
                            json.dump(data, mdFile, indent=4)

                        generateMDTableFromJSON(data, toDocs, counter, pathToJsonData)
                        appendScriptToMDFile(fromMetadata, toDocs)
                    else:
                        #if there is another JSON file in the same subfolder
                        with open(fromMetadata, "r") as jsonFile:
                            data = json.load(jsonFile)
                        with open(toDocs, "a") as mdFile:

                            AnotherJsonInSubfolder(data, toDocs, pathToJsonData)     
                            appendScriptToMDFile(fromMetadata, toDocs)
        else:
            newEmptyMD = os.path.join(subfolderDocs, counter + ".md")

            if not os.path.exists(newEmptyMD):
                open(newEmptyMD, "w").close()



fromMetadatatoDocs()