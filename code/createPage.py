import os
import json
import subprocess

def createTableLink(data):
    """
    Checks the JSON data if there is @id and @type. If both exists the link will be created with the value of @id.

    Parameter/Input:
        data: The JSON data, which should be checked.

    Returns:
        created Link für the Table.
    """
    if not isinstance(data, dict):
        return data
    
    idValue = data.get("@id", "")
    typeValue = data.get("@type", "")

    if idValue and typeValue:
        # Only if @id and @type are in the data and the value are saved then create link
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
        file.write(f'\n\n<script type="application/ld+json">\n{json.dumps(scriptCode, indent=2)}\n</script>\n\n')
        


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
        obj (dict): The nested object which will be rendered.

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



def generateMDTableFromJSON(jsonData, jsonFileURL):
    """
    Generate a Markdown file from JSON data.

    Parameter/Input:
        jsonData: The JSON data to convert.

    Returns:
        A markdown text with the rendered metadata.
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

    linkValue = jsonData.get("@link", "")
    if linkValue:
        md += f'<p><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7V32zM64 352c-35.3 0-64 28.7-64 64v32c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V416c0-35.3-28.7-64-64-64H346.5l-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352H64zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/></svg><a href="{jsonFileURL}" target="_blank"> Get JSON-LD</a> | {linkValue}</p>\n'
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

    return md


def processProjectData(data):
    """
    Process JSON data for the "project" subfolder in "metadata" and generate Markdown file in "docs".

    Parameters/Input:
        jsonFilePath: Path to the JSON file.

    Returns:
        A markdown text with the rendered metadata.
    """
    mappings = [("employee", "Current project members"), ("alumni", "Previous project members"), ("member", "External contributors"), ("knowsAbout", "Publications"), ("parentOrganization", "Research Institute"), ("subOrganization", "Sub-projects")]
    mappings_from = [i[0] for i in mappings]
    mappings_to = [i[1] for i in mappings]

    md = ""

    for property, value in data.items():
        if property == 'name':
            md += f'## {value.capitalize()}\n\n'

        if property == "foundingDate" :
            md += f'_Started in {value}_\n'
        elif property == 'dissolutionDate':
            md += f'_Concluded in {value}_\n'

        if property not in ["@type", "@id", "@context", "name", "dissolutionDate", "foundingDate"]:
            if property in mappings_from :
                i = mappings_from.index(property)
                md += f'### {mappings_to[i]}\n\n'
            else :
                md += f'### {property.capitalize()}\n\n'

            if isinstance(value, list):
                for item in value:
                    if isinstance(item, (dict, list)):
                        for mdFolderName in item:
                            subItem = item.get(mdFolderName, "")
                            if (isinstance(subItem,(dict, list))):
                                if "name" in subItem:
                                    md += f'#### {subItem["name"].capitalize()}\n\n'
                                if "givenName" in item and "familyName" in subItem:
                                    givenName = subItem["givenName"]
                                    lastName = subItem["familyName"]
                                    md += f'#### {givenName + " " +lastName}\n\n'
                                if "@type" in subItem and "@id" in subItem:
                                    subTypeURL = subItem["@type"]
                                    idURL = subItem["@id"]
                                    md += f'<a href="{idURL}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit {subTypeURL}</a>\n\n'
                                for prop, val in subItem.items():
                                    if prop not in ["@type", "@id", "name"]:
                                        md += f'- {prop.capitalize()}: {val}\n'
                        if "name" in item:
                            md += f'#### {item["name"].capitalize()}\n\n'
                        if "givenName" in item and "familyName" in item:
                            givenName = item["givenName"]
                            lastName = item["familyName"]
                            md += f'#### {givenName + " " +lastName}\n\n'
                        if "@type" in item and "@id" in item:
                            subTypeURL = item["@type"]
                            idURL = item["@id"]
                            md += f'<a href="{idURL}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit {subTypeURL}</a>\n\n'
                        for prop, val in item.items(): 
                            if prop not in ["@type", "@id", "name", "funder"]:
                                md += f'- {prop.capitalize()}: {val}\n'
            
            elif isinstance(value, dict):
                for subProperty, subValue in value.items():
                    if isinstance(subValue, (dict, list)):
                        if "name" in subValue:
                            md += f'#### {item["name"].capitalize()}\n\n'
                        if "givenName" in subValue and "familyName" in subValue:
                            givenName = subValue["givenName"]
                            lastName = subValue["familyName"]
                            md += f'#### {givenName +" " + lastName}\n\n'
                        if "@type" in subValue and "@id" in subValue:
                            subTypeURL = subValue["@type"]
                            subidURL= subValue["@id"]
                            md += f'<a href="{subidURL}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit {subTypeURL}</a>\n\n'
                        for prop, val in subValue.items():
                            if prop not in ["@type", "@id", "name"]:
                                md += f'- {prop.capitalize()}: {val}\n'
                    else: 
                        if "name" in subProperty:
                            md += f'#### {subValue.capitalize()}\n\n'
                            subTypeURL = value.get("@type", "")
                            subidURL = value.get("@id", "")
                            if subTypeURL and subidURL:
                                md += f'<a href="{subidURL}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style="margin-bottom: 50px"/></svg> Visit {subTypeURL}</a>\n\n'
                        if subProperty:
                            if subProperty not in ["@type", "@id", "name"]:
                                md += f'- {subProperty.capitalize()}: {subValue}\n'
            else:
                md += f'{value}\n'

    return md



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
    repoURL = getCurrentGitUrl().rsplit(".git", 1)[0]
    currentPath = os.getcwd()
    metadataPath = os.path.join(currentPath, "metadata")
    docsPath = os.path.join(currentPath, "docs")

    metadataFolderList = os.listdir(metadataPath)

    for mdFolderName in metadataFolderList:
        mdFolderPath = os.path.join(metadataPath, mdFolderName)
        mdFileList = os.listdir(mdFolderPath)

        docFilePath = os.path.join(docsPath, mdFolderName + ".md")
        md = f'# {mdFolderName.capitalize()} metadata\n\n'
        with open(docFilePath, "w", encoding="utf-8") as mdDocFile:
            mdDocFile.write(md)
        
        allJsonFileList = [fileName for fileName in mdFileList if fileName.endswith(".json")]

        for jsonFileName in allJsonFileList:
            jsonFilePath = os.path.join(mdFolderPath, jsonFileName)
            jsonFileURL = repoURL + "/blob/main/" + jsonFilePath[jsonFilePath.index("metadata"):]

            with open(jsonFilePath, "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)
                md = ""
                if mdFolderName == 'projects':
                    md = processProjectData(data)
                else: 
                    md = generateMDTableFromJSON(data, jsonFileURL)
                with open(docFilePath, "a", encoding="utf-8") as mdDocFile:
                    mdDocFile.write(md)    
                    mdDocFile.write(f'\n\n<script type="application/ld+json">\n{json.dumps(data, indent=2)}\n</script>\n\n')
            
        
fromMetadatatoDocs()