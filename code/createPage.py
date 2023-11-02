import os
import json
import subprocess
import shutil

DOCS_SUBFOLDERS = ['consortia', 'projects', 'theses']
RO_CRATE_SUBFOLDERS = ['projects', 'theses']
MAPPINGS = [("employee", "Current project members"), ("alumni", "Previous project members"), ("member", "External contributors"), ("knowsAbout", "Outcomes"), ("parentOrganization", "Parent organization, consortium or research project"), ("subOrganization", "Sub-projects")]
MAPPINGS_FROM = [i[0] for i in MAPPINGS]
MAPPINGS_TO = [i[1] for i in MAPPINGS]

def createTableLink(data):
    """
    Checks the JSON data if there is @id and @type. If both exists the link will be created with the value of @id.

    Parameter/Input:
        data: The JSON data, which should be checked.

    Returns:
        created Link for the Table.
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

def createGetJsonLink(jsonFileURL) :
    """
    Checks the get JSON-LD link from the JSON file URL.

    Parameter/Input:
        jsonFileURL: The JSON file URL.

    Returns:
        JSON-LD link.
    """
    return f'<img src = "/images/get.svg" alt="Get JSON-LD"/><a href="{jsonFileURL}" target="_blank" download="metadata.json"> Get JSON-LD</a>'

def createGetROCrateLink(rocrateFileURL) :
    """
    Checks the get RO-Crate JSON-LD link from the RO-Crate JSON file URL.

    Parameter/Input:
        rocrateFileURL: The RO-Crate JSON file URL.

    Returns:
        RO-Crate JSON-LD link.
    """
    return f'<img src = "/images/get.svg" alt="Get RO-Crate"/><a href="{rocrateFileURL}" target="_blank" download="ro-crate-metadata.json"> Get RO Crate</a>'

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

def renderUrlAsHref(val):
    md = ""
    if isinstance(val, list):
        for elem in val:
            md += f'- URL: <a href="{elem}" target="_blank">{elem}</a>\n\n'
    else: 
        md += f'- URL: <a href="{val}" target="_blank">{val}</a>\n\n'
    
    return md

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
        if prop not in ["@type", "@id", "name", "http://purl.org/dc/terms/conformsTo", "funder", "givenName", "familyName"]:
            if prop == 'url':
                md += renderUrlAsHref(val)
            else :
                md += f'- {prop.capitalize()}: {val}\n'
    return md

def processProjectData(data, jsonFileURL, rocrateFileURL):
    """
    Process JSON data for the "project" subfolder in "metadata" and generate Markdown file in "docs".

    Parameters/Input:
        jsonFilePath: Path to the JSON file.

    Returns:
        A markdown text with the rendered metadata.
    """
    md = ""

    for property, value in data.items():
        if property not in ["@type", "@id", "@context", "http://purl.org/dc/terms/conformsTo", "name", "dissolutionDate", "foundingDate"]:
            if property in MAPPINGS_FROM :
                i = MAPPINGS_FROM.index(property)
                md += f'### {MAPPINGS_TO[i]}\n\n'
            else :
                md += f'### {property.capitalize()}\n\n'

            #ToDo: analyze and refactor code
            if property == 'url':
                md += renderUrlAsHref(value)
            elif isinstance(value, list):
                #knowsAbout is a list of objects
                #there is a bug with inner lists (keywords) and objects (license) inside those objects
                for item in value:
                    if isinstance(item, (dict, list)):
                        #each item is an object/dict
                        #loop on each key, value pair
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
        elif property == 'name':
            md += f'## {value}\n\n'
            md += f'<p>{createGetJsonLink(jsonFileURL)}</p>\n'
            if rocrateFileURL != "":
                md += f'<p>{createGetROCrateLink(rocrateFileURL)}</p>\n'
        elif property == "foundingDate" :
            md += f'_Started in {value}_\n'
        elif property == 'dissolutionDate':
            md += f'_Concluded in {value}_\n'

    return md

def prepareDocsSubfolder(docsPath):
    """
    Function that creates subfolders in the docs folder for those metadata folders corresponding to research projects.
    Some metadata folder will create a subfolder in docs rather than an MD file. 
    In particular, those corresponding to research project as they have to be rendered individually.
    The list of metadata folders used in this function are collected in a global variable docsSubfolders.
    Note: (limitation) The use of docsSubfoldersPath supposed the exact same order as docsSubfolders.

    Parameter/Input:
        docsPath: The path to the local docs folder

    Returns:
        A list with the local path for all docs subfolders corresponding to research projects
    """
    docsSubfoldersPath = [(docsPath + "/") + subfolder for subfolder in DOCS_SUBFOLDERS]
    docsSubfoldersPath = [subfolder + "/" for subfolder in docsSubfoldersPath] 
    
    for subfolder in docsSubfoldersPath:
        try:
            shutil.rmtree(subfolder)
        except:
            pass
        finally:  
            os.makedirs(subfolder)
    
    return docsSubfoldersPath

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
    docsSubfoldersPath = prepareDocsSubfolder(docsPath)
    
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
            if "ro-crate" in jsonFileName:
                continue

            jsonFilePath = os.path.join(mdFolderPath, jsonFileName)            
            with open(jsonFilePath, "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)
                allMetadata.append(data)

                md = ""
                folderIndex = -1
                fileNameNoExt = jsonFileName.removesuffix('.json')
                try:
                  folderIndex = DOCS_SUBFOLDERS.index(mdFolderName)                                    
                  jsonFileURL = f"../../metadata/{mdFolderName}/{fileNameNoExt}.json"
                  rocrateFileURL = ""
                  if mdFolderName in RO_CRATE_SUBFOLDERS:
                    rocrateFileURL = f"../../metadata/{mdFolderName}/{fileNameNoExt}/ro-crate-metadata.json"
                  md = f'# {mdFolderName.capitalize()} metadata\n\n'
                  md += processProjectData(data, jsonFileURL, rocrateFileURL)
                  docFileProjectsPath = os.path.join(docsSubfoldersPath[folderIndex], jsonFileName.removesuffix('.json') + ".md")
                  with open(docFileProjectsPath, "a", encoding="utf-8") as mdDocFile:
                    mdDocFile.write(md)    
                    mdDocFile.write(f'\n\n<script type="application/ld+json">\n{json.dumps(data, indent=2)}\n</script>\n\n')
                except Exception as e:
                  #print(e)
                  jsonFileURL = f"../metadata/{mdFolderName}/{fileNameNoExt}.json"
                  md = generateMDTableFromJSON(data, jsonFileURL)                    
                  with open(docFilePath, "a", encoding="utf-8") as mdDocFile:
                    mdDocFile.write(md)    
                    mdDocFile.write(f'\n\n<script type="application/ld+json">\n{json.dumps(data, indent=2)}\n</script>\n\n')    
       
        
fromMetadatatoDocs()