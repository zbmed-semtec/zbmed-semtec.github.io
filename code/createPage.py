import os
import json



def appendScriptToMDFile(mdFile):
    """
    Append the script to the new Markdown file.

    Parameter/Input:
        mdFile: The path to the Markdown file.

    Returns:
        None
    """
    script_code = '''<script type="application/ld+json">
{ 
    "@context": "https://schema.org", 
    "@type": "Dataset",
    "@id": "https://github.com/BioSchemas/github-markup-example/blob/main/data/sample.csv",
    "http://purl.org/dc/terms/conformsTo": "https://bioschemas.org/profiles/Dataset/0.4-DRAFT", 

    "description": "Toy data used as an example on how to add Bioschemas markup to your data",
    "identifier": "https://github.com/BioSchemas/github-markup-example/blob/main/data/sample.csv",
    "keywords":  [
      {
        "@type": "DefinedTerm", 
        "@id": "http://edamontology.org/data_0006", 
        "name": "Data"
      },
      "Sample data"
    ], 
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "name": "Hello fruit data",
    "url": "https://bioschemas.org/github-markup-example/data.html" 
}
</script>'''

    with open(mdFile, "a") as file:
        file.write('\n' + script_code)
        


def renderProperty(name, value):
    """
    Function, which renders the property values as HTML.

    Paramater/Input:
        name: The name of the property.
        value: The value of the property.

    Returns:
        The representation of the property value in HTML.
    """
    if isinstance(value, dict):
        return renderInnerTable(value)
    elif isinstance(value, list):
        return renderInnerList(value)
    elif isinstance(value, str) and value.startswith("http"):
        return f'<a href="{value}" target="_blank">{value}</a>'
    else:
        return str(value)



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
            link = f'<a href="{valueInner}" target="_blank">Click here for more information on this object</a>'
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
            listMD += f'\n<li><table class="blueTable">\n<tbody>{renderInnerTable(item)}</tbody>\n</table></li>'
        elif isinstance(item, list):
            listMD += f'\n<li>{renderInnerList(item)}</li>'
        elif isinstance(item, str) and item.startswith("@id"):
            itemID = item.split(":")[1]
            itemURL = generateMDTableFromJSON.jsonData[itemID]
            itemType = generateMDTableFromJSON.jsonData[itemID].get("@type", "")
            link = f'<a href="{itemURL}" target="_blank">Click here for more information on this object</a>'
            listMD += f'\n<li>{itemType} - {link}</li>'
        else:
            listMD += f"\n<li>{renderProperty('', item)}</li>"
    return listMD



def generateMDTableFromJSON(jsonData, outputFile, FolderName):
    """
    Generate a Markdown file from JSON data.

    Parameter/Input:
        jsonData: The JSON data to convert.
        outputFile: The path to the output file with the MD-Code.
        FolderName: The name of the folder used for the title.

    Returns:
        None
    """
    md = f'<h1>{FolderName.capitalize()} information</h1>\n'
    md += f'<p><a href="{jsonData["@id"]}" target="_blank">Click here to get the metadata for this object in JSON-LD</a></p>\n'
    md += '<table class="blueTable">\n<tbody>\n'
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
    appendScriptToMDFile(outputFile)



def fromMetadatatoDocs():
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
                        
                        generateMDTableFromJSON(data, toDocs, counter)

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
                    generateMDTableFromJSON(data, toDocs, counter)

            if not hasJSONFile:
                    newEmptyMD = os.path.join(subfolderDocs, counter + ".md")

                    if not os.path.exists(newEmptyMD):
                        open(newEmptyMD, "w").close()





fromMetadatatoDocs()