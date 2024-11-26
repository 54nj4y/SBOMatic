# SBOMatic

**Automating SBOM Generation Across Multiple Tech Stacks**

SBOMatic is an automated tool that makes it easy to generate **Software Bills of Materials (SBOMs)** for projects across different programming languages, including **Java, Python, Go, and Node.js**. It simplifies the process of managing dependencies by automatically generating a detailed list of all components, libraries, and dependencies used in your codebase.

This tool utilizes CycloneDX plugins to generate SBOMs in the CycloneDX standard format. Check out our [blog post on generating SBOMs](https://medium.com/@podhavenx/understanding-sbom-and-sca-how-to-secure-software-and-generate-sboms-for-java-python-node-js-5ed64772ce9e) for guidance on generating SBOMs for each language.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)

## Prerequisites

This tool uses CycloneDX plugins to generate SBOMs. To run this tool, you need to install the following plugins as per the installation instructions in their respective repositories:

- CycloneDX Python: [https://github.com/CycloneDX/cyclonedx-python](https://github.com/CycloneDX/cyclonedx-python)
- CycloneDX Go: [https://github.com/CycloneDX/cyclonedx-gomod](https://github.com/CycloneDX/cyclonedx-gomod)
- CycloneDX Node.js: [https://github.com/CycloneDX/cyclonedx-node-npm](https://github.com/CycloneDX/cyclonedx-node-npm)
- Node.js and npm: Install via `sudo apt install nodejs npm` (for linux)
- Java (Maven plugin): Install via `sudo apt install maven` (for Linux)

## Usage

To run the tool, execute the following command:

`python3 sbomatic.py <folder path> `

This tool automatically identifies and lists project files such as **`pom.xml`**, **`package.json`**, etc., in the specified folder and its subfolders. The generated SBOM file's path will be displayed at the end.

For a sample run, you can use the "sample" folder included in this repository.

Command:  `python3 sbomatic.py sample`

![image](https://github.com/user-attachments/assets/4f50914a-5543-455a-8228-7cf7f46f1fa9)



