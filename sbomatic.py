#!/usr/bin/env python3

import os
import subprocess
import json
from pathlib import Path
import sys

def detect_project_types(path):
    """Detect all types of projects based on key files"""
    files = os.listdir(path)
    project_types = []
    project_files = []

    # Check for specific project files
    if "pom.xml" in files:
        project_types.append("java")
        project_files.append("pom.xml")
    if "package.json" in files:
        project_types.append("nodejs")
        project_files.append("package.json")
    if "go.mod" in files:
        project_types.append("go")
        project_files.append("go.mod")
    if "requirements.txt" in files:
        project_types.append("python")
        project_files.append("requirements.txt")
    if "setup.py" in files:
        project_types.append("python")
        project_files.append("setup.py")

    return project_types, project_files

def generate_java_sbom(project_path):
    """Generate SBOM for Java/Maven projects"""
    print(f"Generating SBOM for Java project at {project_path}")
    subprocess.run([
        "mvn", "org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom", "-q"
    ], cwd=project_path)
    
    # Check for either bom.json or bom.xml
    bom_json_path = os.path.join(project_path, "target/bom.json")
    bom_xml_path = os.path.join(project_path, "target/bom.xml")

    # Check if either BOM file exists
    if (os.path.exists(bom_json_path) and os.path.getsize(bom_json_path) > 0) or \
       (os.path.exists(bom_xml_path) and os.path.getsize(bom_xml_path) > 0):
        return bom_json_path if os.path.exists(bom_json_path) else bom_xml_path
    else:
        return None

def generate_python_sbom(project_path):
    """Generate SBOM for Python projects"""
    print(f"Generating SBOM for Python project at {project_path}")
    output_path = os.path.join(project_path, "bom-python.json")
    subprocess.run([
        "cyclonedx-py",
        "requirements",
        "requirements.txt",
        "-o", "bom-python.json"
    ], cwd=project_path)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        return output_path
    else:
        return None

def generate_go_sbom(project_path):
    """Generate SBOM for Go projects"""
    print(f"Generating SBOM for Go project at {project_path}")
    output_path = os.path.join(project_path, "bom-go.json")
    subprocess.run([
        "cyclonedx-gomod",
        "app",
        "-json=true",
        "-output", "bom-go.json"
    ], cwd=project_path)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        return output_path
    else:
        return None

def generate_nodejs_sbom(project_path):
    """Generate SBOM for Node.js projects"""
    print(f"Generating SBOM for Node.js project at {project_path}")
    output_path = os.path.join(project_path, "bom-nodejs.json")
    subprocess.run(["npm", "install", "--silent"], cwd=project_path)
    subprocess.run(["cyclonedx-npm", "--output-file", "bom-nodejs.json"], cwd=project_path)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        return output_path
    else:
        return None

def scan_directory(base_path):
    """Scan directory recursively for projects, excluding node_modules"""
    projects = []

    for root, dirs, files in os.walk(base_path):
        # Skip the node_modules directory
        if "node_modules" in dirs:
            dirs.remove("node_modules")  # Prevent os.walk from scanning this directory

        project_types, project_files = detect_project_types(root)

        # Only add the relevant project files
        if project_files:
            for proj_type, proj_file in zip(project_types, project_files):
                file_path = os.path.join(root, proj_file)  # Get full file path
                projects.append({
                    "file": proj_file,
                    "path": root,  # Use root directory (not file path)
                    "type": proj_type
                })

    return projects

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 sbomatic.py <folder path>")
        return
    base_path = sys.argv[1]
    projects = scan_directory(base_path)

    if not projects:
        print("No supported projects found!")
        return

    # Group projects by path for better display
    projects_by_path = {}
    for project in projects:
        if project['path'] not in projects_by_path:
            projects_by_path[project['path']] = []
        projects_by_path[project['path']].append((project['file'], project['type']))

    # Display found projects
    print("\nFound projects:")
    for i, (path, files_and_types) in enumerate(projects_by_path.items(), 1):
        print(f"{i}. Path: {path}")
        for file, proj_type in files_and_types:
            print(f"\033[92m   File: {file}, Tech Stack: {proj_type}\033[0m")

    # Generate SBOMs and track results
    print("\nGenerating SBOMs...")
    generated_sboms = []

    for project in projects:
        try:
            sbom_path = None
            if project['type'] == 'java':
                sbom_path = generate_java_sbom(project['path'])
            elif project['type'] == 'python':
                sbom_path = generate_python_sbom(project['path'])
            elif project['type'] == 'go':
                sbom_path = generate_go_sbom(project['path'])
            elif project['type'] == 'nodejs':
                sbom_path = generate_nodejs_sbom(project['path'])

            if sbom_path:
                generated_sboms.append({
                    'language': project['type'],
                    'path': sbom_path,
                    'project_path': project['path']
                })
            else:
                print(f"SBOM generation failed for {project['path']} ({project['type']}).")

        except Exception as e:
            print(f"\033[91mError generating SBOM for {project['path']} ({project['type']}): {str(e)}\033[0m")

    # Display summary of generated SBOMs
    print("\nGenerated SBOM Summary:")
    print("-" * 50)
    for sbom in generated_sboms:
        print(f"Language: {sbom['language']}")
        print(f"Project Location: {sbom['project_path']}")
        if sbom['path']:
            print(f"\033[92mSBOM Location: {sbom['path']}\033[0m")
        else:
            print(f"SBOM generation failed for {sbom['project_path']} ({sbom['language']}).")
        print("-" * 50)

if __name__ == "__main__":
    main()

