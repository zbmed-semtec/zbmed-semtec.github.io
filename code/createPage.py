import os
import json
import subprocess



def categorizePeople():
    """
    Categorize team members into current and former team members and append them to the associated arrays.

    Parameter/Input:
        None

    Returns:
        None
    """
    metadataPath = os.path.join(os.getcwd(), "metadata")
    peoplePath = os.path.join(metadataPath, "people")
    peopleDocs = os.path.join(os.path.join(os.getcwd(), "docs"), "people" + ".md")

    currentTeamData = []
    formerTeamData = []

    for dataCounter in os.listdir(peoplePath):
        if dataCounter.endswith(".json"):
            with open(os.path.join(peoplePath, dataCounter), "r", encoding="utf-8") as jsonFile:
                data = json.load(jsonFile)

            if isinstance(data, dict):
                memberOf = data.get("memberOf", [])
                if any(isinstance(item, dict) and item.get("@type") == "OrganizationRole" and item.get("roleName", "").startswith("SemTec team") for item in memberOf):
                    currentTeamData.append(data)
                else:
                    formerTeamData.append(data)

    generateCategorizePeopleTable(currentTeamData, formerTeamData, peopleDocs, "People")



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
        file.write(f'\n\n<script type="application/ ">\n{json.dumps(scriptCode, indent=4)}\n</script>\n\n')
        


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



def generateCategorizePeopleTable(currentTeamData, formerTeamData, outputFile, folderName):
    """
    Generates Markdown tables for the categorized arrays of current and former team members.

    Parameters/Input:
        currentTeamData: List of current team member data.
        formerTeamData: List of former team member data.
        outputFile: Path to the output Markdown file.
        folderName: Name of the folder used for the title.

    Returns:
        None
    """

    md = f'# {folderName.capitalize()} metadata\n\n'
    md2 = ""

    md += f'## {"current Team Members".capitalize()}\n\n'
    md += f'<p><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7V32zM64 352c-35.3 0-64 28.7-64 64v32c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V416c0-35.3-28.7-64-64-64H346.5l-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352H64zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/></svg><a href="https://ror.org/0259fwx54" target="_blank"> Visit Organization</a></p>\n'           # visit Organization direkt nach current Team member Überschrift

    currentMemory = []
    formerMemory = []

    for item in currentTeamData:
        if "givenName" in item and "familyName" in item:
            familyName = item.get("familyName", "")
            md += f'### {renderProperty("Name", item["givenName"] + " " + familyName)}\n'
        elif "familyName" in item and "givenName" not in item:
            md += f'### {renderProperty("Name", item["familyName"])}\n'

        item = createTableLink(item)

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
            aktuellesVerzeichnis = os.getcwd()
            pathJSONLD = aktuellesVerzeichnis + "/metadata/people/" + cuttedOwnPath + ".json"
            currentMemory.append(pathJSONLD)

        linkValue = item.get("@link", "")
        if linkValue:
            md += f'<p><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7V32zM64 352c-35.3 0-64 28.7-64 64v32c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V416c0-35.3-28.7-64-64-64H346.5l-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352H64zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/></svg><a href="{pathToJsonData}" target="_blank"> Get JSON-LD</a> | {linkValue}</p>\n'
        item.pop("@link", None)

        md += '<table style="background-color: #F5F5F5; width: 100%; text-align: left; border: 1px solid black;">\n<tbody>\n'
        
        for property, value in item.items():
            if "memberOf" in item:
                for counter in item["memberOf"]:
                    if isinstance(counter, dict) and "memberOf" in counter:
                        counter.pop("memberOf", None)
            if property == "@id":
                typeValue = item.get("@type", "")
                value = f'<a href="{value}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit {typeValue}</a>'
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
    for counterCurrent in currentMemory:
        appendScriptToMDFile(counterCurrent, outputFile)


    md2 += f'## {"former Team Members".capitalize()}\n\n'

    for item in formerTeamData:
        if "givenName" in item and "familyName" in item:
            familyName = item.get("familyName", "")
            md2 += f'### {renderProperty("Name", item["givenName"] + " " + familyName)}\n'
        elif "familyName" in item and "givenName" not in item:
            md2 += f'### {renderProperty("Name", item["familyName"])}\n'

        item = createTableLink(item)

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
            aktuellesVerzeichnis = os.getcwd()
            pathJSONLD = aktuellesVerzeichnis + "/metadata/people/" + cuttedOwnPath + ".json"
            formerMemory.append(pathJSONLD)

        linkValue = item.get("@link", "")
        if linkValue:
            md2 += f'<p><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7V32zM64 352c-35.3 0-64 28.7-64 64v32c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V416c0-35.3-28.7-64-64-64H346.5l-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352H64zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/></svg><a href="{pathToJsonData}" target="_blank"> Get JSON-LD</a> | {linkValue}</p>\n'
        item.pop("@link", None)

        md2 += '<table style="background-color: #F5F5F5; width: 100%; text-align: left; border: 1px solid black;">\n<tbody>\n'
        
        for property, value in item.items():
            if property == "alumniOf":
                continue
            if property == "@id":
                typeValue = item.get("@type", "")
                value = f'<a href="{value}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit {typeValue}</a>'
            if property not in ["@type", "@id", "@context", "http://purl.org/dc/terms/conformsTo"]:
                if isinstance(value, list):
                    md2 += f'<tr>\n<td>{property}</td>\n<td><ul>{renderInnerList(value)}</ul></td>\n</tr>\n'
                else:
                    renderedValue = renderProperty(property, value)
                    if renderedValue is not None:   
                        md2 += f'<tr>\n<td>{property}</td>\n<td>{renderedValue}</td>\n</tr>\n'

        md2 += '</tbody>\n</table>'

    with open(outputFile, "a", encoding="utf-8") as file:
        file.write(md2)
    for counterFormer in formerMemory:
        appendScriptToMDFile(counterFormer, outputFile)



def processProjectData(fromMetadata, toDocs):
    """
    Process JSON data for the "project" subfolder in "metadata" and generate Markdown file in "docs".

    Parameters/Input:
        fromMetadata: Path to the JSON file.
        toDocs: Path to the output Markdown file.

    Returns:
        None
    """
    md = ""
    
    with open(fromMetadata, "r", encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)
        
        for property, value in data.items():
            if property == 'name':
                md += f'# {value.capitalize()}\n\n'
            if property not in ["@type", "@id", "@context", "name"]:
                md += f'## {property.capitalize()}\n\n'

                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, (dict, list)):
                            for counter in item:
                                subItem = item.get(counter, "")
                                if (isinstance(subItem,(dict, list))):
                                    if "name" in subItem:
                                        md += f'### {subItem["name"].capitalize()}\n\n'
                                    if "givenName" in item and "familyName" in subItem:
                                        givenName = subItem["givenName"]
                                        lastName = subItem["familyName"]
                                        md += f'### {givenName + " " +lastName}\n\n'
                                    if "@type" in subItem and "@id" in subItem:
                                        subTypeURL = subItem["@type"]
                                        idURL = subItem["@id"]
                                        md += f'<a href="{idURL}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit {subTypeURL}</a>\n\n'
                                    for prop, val in subItem.items():
                                        if prop not in ["@type", "@id", "name"]:
                                            md += f'- {prop.capitalize()}: {val}\n'
                            if "name" in item:
                                md += f'### {item["name"].capitalize()}\n\n'
                            if "givenName" in item and "familyName" in item:
                                givenName = item["givenName"]
                                lastName = item["familyName"]
                                md += f'### {givenName + " " +lastName}\n\n'
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
                                md += f'### {item["name"].capitalize()}\n\n'
                            if "givenName" in subValue and "familyName" in subValue:
                                givenName = subValue["givenName"]
                                lastName = subValue["familyName"]
                                md += f'### {givenName +" " + lastName}\n\n'
                            if "@type" in subValue and "@id" in subValue:
                                subTypeURL = subValue["@type"]
                                subidURL= subValue["@id"]
                                md += f'<a href="{subidURL}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style = "margin-bottom: 50px"/></svg> Visit {subTypeURL}</a>\n\n'
                            for prop, val in subValue.items():
                                if prop not in ["@type", "@id", "name"]:
                                    md += f'- {prop.capitalize()}: {val}\n'
                        else: 
                            if "name" in subProperty:
                                md += f'### {subValue.capitalize()}\n\n'
                                subTypeURL = value.get("@type", "")
                                subidURL = value.get("@id", "")
                                if subTypeURL and subidURL:
                                  md += f'<a href="{subidURL}" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z" style="margin-bottom: 50px"/></svg> Visit {subTypeURL}</a>\n\n'
                            if subProperty:
                                if subProperty not in ["@type", "@id", "name"]:
                                    md += f'- {subProperty.capitalize()}: {subValue}\n'
                else:
                    md += f'{value}\n'

    with open(toDocs, "w", encoding="utf-8") as file:
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
        
        if counter == "people":
            categorizePeople()
            
        if counter =="projects":
            processProjectData(fromMetadata, toDocs)
            appendScriptToMDFile(fromMetadata, toDocs)
        else:
            newEmptyMD = os.path.join(subfolderDocs, counter + ".md")

            if not os.path.exists(newEmptyMD):
                open(newEmptyMD, "w", encoding="utf-8").close()



fromMetadatatoDocs()