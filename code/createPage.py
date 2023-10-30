import os
import json
import subprocess
import shutil

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
        visitLink = f'<a href="{idValue}" target="_blank"><img src = "/images/visit.svg" alt="Visit URL"/> Visit {typeValue}</a>'
        data["@link"] = visitLink
    return data

def createGetJsonLink (jsonFileURL) :
    """
    Checks the get raw JSON-LD link from the JSON file URL.

    Parameter/Input:
        jsonFileURL: The JSON file URL.

    Returns:
        JSON-LD raw link.
    """
    return f'<img src = "/images/get.svg" alt="Get JSON-LD"/><a href="{jsonFileURL.replace("github.com", "raw.githubusercontent.com").replace("blob/", "")}" target="_blank"> Get JSON-LD</a>'

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
            link = fr'<a href="{valueInner}" target="_blank"><img src = "/images/visit.svg" alt="Visit URL"/> Visit {valueInnerType} Object</a>'
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
        md += f'<p>{createGetJsonLink(jsonFileURL)} | {linkValue}</p>\n'
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

def processNamesInProject(item) :
    """
    Generate a Markdown text from a JSON item.

    Parameter/Input:
        item: JSON item to convert.

    Returns:
        A markdown text with the rendered metadata.
    """
    md = ""
    if "name" in item:
        md += f'#### {item["name"]}\n\n'
    if "givenName" in item and "familyName" in item:
        givenName = item["givenName"]
        lastName = item["familyName"]
        md += f'- {givenName + " " +lastName}\t\t'
    if "@type" in item and "@id" in item:   
        subTypeURL = item["@type"]
        idURL = item["@id"]
        md += f'<a href="{idURL}" target="_blank"><img src = "/images/visit.svg" alt="Visit URL"/> Visit {subTypeURL}</a>\n\n'
    for prop, val in item.items(): 
        if prop not in ["@type", "@id", "name", "funder", "givenName", "familyName"]:
            if prop == 'url':
                md += f'- URL: <a href="{val}" target="_blank">{val}</a>\n\n'
            else :
                md += f'- {prop.capitalize()}: {val}\n'
    return md

def processProjectData(data, jsonFileURL):
    """
    Process JSON data for the "project" subfolder in "metadata" and generate Markdown file in "docs".

    Parameters/Input:
        jsonFilePath: Path to the JSON file.

    Returns:
        A markdown text with the rendered metadata.
    """
    mappings = [("employee", "Current project members"), ("alumni", "Previous project members"), ("member", "External contributors"), ("knowsAbout", "Outcomes"), ("parentOrganization", "Parent organization, consortium or research project"), ("subOrganization", "Sub-projects")]
    mappings_from = [i[0] for i in mappings]
    mappings_to = [i[1] for i in mappings]

    md = ""

    for property, value in data.items():
        if property == 'name':
            md += f'## {value}\n\n'
            md += f'<p>{createGetJsonLink(jsonFileURL)}</p>\n'

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
                                md += processNamesInProject(subItem) 
                        md += processNamesInProject(item) 
            
            elif isinstance(value, dict):
                for subProperty, subValue in value.items():
                    if isinstance(subValue, (dict, list)):
                        md += processNamesInProject(subValue) 
                    else: 
                        if "name" in subProperty:
                            md += f'#### {subValue}\n\n'
                            subTypeURL = value.get("@type", "")
                            subidURL = value.get("@id", "")
                            if subTypeURL and subidURL:
                                md += f'<a href="{subidURL}" target="_blank"><img src = "/images/visit.svg" alt="Visit URL"/> Visit {subTypeURL}</a>\n\n'
                        if subProperty:
                            if subProperty not in ["@type", "@id", "name"]:
                                if subProperty == "url" :
                                    md += f'- URL: <a href="{subValue}" target="_blank">{subValue}</a>\n\n'
                                else :
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

    docsProjectPath = docsPath + "/projects/"
    shutil.rmtree(docsProjectPath)
    os.makedirs(docsProjectPath)

    allMetadata = []

    metadataFolderList = os.listdir(metadataPath)

    for mdFolderName in metadataFolderList:
        mdFolderPath = os.path.join(metadataPath, mdFolderName)
        mdFileList = os.listdir(mdFolderPath)
        docFilePath = os.path.join(docsPath, mdFolderName + ".md")
        allJsonFileList = [fileName for fileName in mdFileList if fileName.endswith(".json")]

        with open(docFilePath, "w", encoding="utf-8") as mdDocFile:
            md = f'# {mdFolderName.capitalize()} metadata\n\n'
            mdDocFile.write(md)

        for jsonFileName in allJsonFileList:
            jsonFilePath = os.path.join(mdFolderPath, jsonFileName)
            jsonFileURL = repoURL + "/blob/main/" + jsonFilePath[jsonFilePath.index("metadata"):]

            with open(jsonFilePath, "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)
                allMetadata.append(data)

                md = ""
                if mdFolderName == 'projects':
                    md = f'# {mdFolderName.capitalize()} metadata\n\n'
                    md += processProjectData(data, jsonFileURL)
                    docFileProjectsPath = os.path.join(docsProjectPath, jsonFileName.removesuffix('.json') + ".md")
                    with open(docFileProjectsPath, "a", encoding="utf-8") as mdDocFile:
                        mdDocFile.write(md)    
                        mdDocFile.write(f'\n\n<script type="application/ld+json">\n{json.dumps(data, indent=2)}\n</script>\n\n')
                else:                                         
                    md = generateMDTableFromJSON(data, jsonFileURL)                    
                    with open(docFilePath, "a", encoding="utf-8") as mdDocFile:
                        mdDocFile.write(md)    
                        mdDocFile.write(f'\n\n<script type="application/ld+json">\n{json.dumps(data, indent=2)}\n</script>\n\n')
    
    #needs to find way not to append the json-ld multiple times
    #with open(docsPath+"/index.md", "a", encoding="utf-8") as indexFile :
        #indexFile.write(f'\n\n<script type="application/ld+json">\n{json.dumps(allMetadata, indent=2)}\n</script>\n\n')
            
        
fromMetadatatoDocs()