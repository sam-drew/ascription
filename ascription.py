import os
import sys
import subprocess
# First find all Python files below the root.
py_files = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py") and file != "ascripion.py":
            py_files.append({
                'name': str(file),
                'path': os.path.join(root, file),
                'pkgs': []
                })
 # Find all imports to files below root, and then get information about these
 # from PIP.
for file in py_files:
    lines = [line.rstrip('\n') for line in open(file['path'])]
    for line in lines:
        if line[0:7] == "import ":
            file['pkgs'].append({
                'Name': line[7:],
                'Version': "",
                'Summary': "",
                'Home-page': "",
                'Author': "",
                'Licence': ""
                })
    for pkg in file['pkgs']:
        try:
            pkg_info = subprocess.check_output([sys.executable, '-m', 'pip', 'show', pkg['Name']]).decode("utf-8")
            pkg_info = pkg_info.splitlines()
            for info in pkg_info:
                # Split on the first colon.
                split_info = info.split(": ", 1)
                if split_info[0] in ['Name', 'Version', 'Summary', 'Home-page', 'Author', 'Licence']:
                    pkg[split_info[0]] = split_info[1]
        except subprocess.CalledProcessError as e:
            print(e, "PIP has no info for this package. Package is likely a Python built in.")

print(py_files)
