# GitHub pages for the SemTec team at ZB MED

Combining semantic technologies and data analytics

We are a multidisciplinary Research and Development team combining semantic technologies and data analytics. We work on the development of softare components and services to support and improve research on information retrieval, data science and literature-based knowledge discovery with a particular focus on reproducibility. Our areas of application include the evaluation of experimental retrieval and recommendation systems, practical support to FAIR+R principles for software and data science, and data analytics from the combination of ontologies and literature-extracted data in the Life Sciences domain.

The Semantic Technologies team is part of the [Knowledge Management group](https://www.zbmed.de/en/research/research-at-zb-med/research-knowledge-management/) at [ZB MED Information Centre for Life Sciences](https://www.zbmed.de/en).

Visit us at https://zbmed-semtec.github.io/





# Developer Documentation

This documentation provides an overview of the Python code used to convert metadata JSON files from subfolders under the /metadata directory into Markdown files under the /docs directory, Each Markdown file is named after the original subfolder in the /metadata directory. The content of these new Markdown files is created by appending the content of each JSON file that was previously located in the subfolder. The metadata is presented as tables for each JSON file in the new generated Markdown files.


## Getting Started

To run the code, follow these steps:

1. Ensure you have Python installed on your system.
2. Ensure that you have the necessary dependencies installed. In this case, you can find the full list of dependencies in the `requirement.txt`
   You can use the following command to install the dependencies directly
   pip install -r requirement.txt
3. Make sure to execute the code while being in the \zbmed-semtec.github.io\ path.
4. The script will start executing, converting JSON files to Markdown files.


## Code Overview

The Python code provided performs the following tasks divided in functions:

1. `fromMetadatatoDocs()`: Copies subfolders from the "metadata" directory to the "docs" directory, converting JSON files to Markdown files.
2. `generateMDTableFromJSON(jsonData, outputFile, FolderName, jsonFile)`: Generates a Markdown file from JSON data.
    It uses Subfunctions
    2.1. `renderProperty(name, value)`: Renders property values as HTML.
    2.2. `renderInnerTable(obj)`: Renders a nested table as HTML.
    2.3. `renderInnerList(lst)`: Renders a nested list as HTML.    
    2.4. `appendScriptToMDFile(mdFile)`: Appends a script to a Markdown file.
3. `AnotherJsonInSubfolder(jsonData, outputFile, jsonFile)`: Same as **`generateMDTableFromJSON` only for Appending further JSON file to a current Markdown file
4. `appendScriptToMDFile(jsonFile, mdFile)`: Appending the JSON as script.
5. `getCurrentGitUrl()`: Getting the current Git repository.
6. `complexDataInList(data)`: Converts complex JSON element into a single element list.
7. `createTableLink(data)`: Creates a link for the table with @id URL 

## Output

After the code has been executed successfully, a new Markdown file is created with the the same name as the subfolder from /metadata. The Markdown file contains the contents of all JSON files that were presented in the subfolder in /metadata and it presents them as HTML Tables. One table for each JSON file on the same Page.