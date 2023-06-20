# GitHub pages for the SemTec team at ZB MED

_Combining semantic technologies and data analytics_

We are a multidisciplinary Research and Development team combining semantic technologies and data analytics. We work on the development of softare components and services to support and improve research on information retrieval, data science and literature-based knowledge discovery with a particular focus on reproducibility. Our areas of application include the evaluation of experimental retrieval and recommendation systems, practical support to FAIR+R principles for software and data science, and data analytics from the combination of ontologies and literature-extracted data in the Life Sciences domain.

The Semantic Technologies team is part of the [Knowledge Management group](https://www.zbmed.de/en/research/research-at-zb-med/research-knowledge-management/) at [ZB MED Information Centre for Life Sciences](https://www.zbmed.de/en).

Visit us at https://zbmed-semtec.github.io/





# Developer Documentation

This documentation provides an overview of the Python code used to convert metadata JSON files from the /metadata directory into Markdown files under the /docs directory, with each file placed in a subfolder named after the original file. The metadata is represented as tables in the generated Markdown files.


## Getting Started

To run the code, follow these steps:

1. Ensure you have Python installed on your system.
2. Ensure that you have the necessary dependencies installed. In this case, the code relies on the os and json modules, which are built-in and typically available by default with Python installations.
3. The script will start executing, converting metadata JSON files to Markdown files.


## Code Overview

The Python code provided performs the following tasks divided in fnctions:

1. **`fromMetadatatoDocs()`**: Copies subfolders from the "metadata" directory to the "docs" directory, converting JSON files to Markdown files.
2. **`generateMDTableFromJSON(jsonData, outputFile, FolderName)`**: Generates a Markdown file from JSON data.
    It uses Subfunctions
    2.1. **`renderProperty(name, value)`**: Renders property values as HTML.
    2.2. **`renderInnerTable(obj)`**: Renders a nested table as HTML.
    2.3. **`renderInnerList(lst)`**: Renders a nested list as HTML.    
    2.4. **`appendScriptToMDFile(mdFile)`**: Appends a script to a Markdown file.


## Output

Once the script is executed successfully, it will generate Markdown files based on the metadata JSON files under the docs directory in a subfolder named after the original file. It will be in a table in HTML format