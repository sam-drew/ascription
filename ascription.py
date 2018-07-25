import os
import sys
import subprocess

# Get the name of the CWD.
cwd = os.getcwd().split("/")[-1]

# Find all Python files below the root.
py_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py") and file != "ascription.py":
            py_files.append({
                'Name': str(file),
                'Path': os.path.join(root, file),
                'pkgs': []
                })
 # Find all imports to files below root, and then get information about these
 # from PIP.
for file in py_files:
    lines = [line.rstrip('\n') for line in open(file['Path'])]
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
            pkg_info = subprocess.check_output([sys.executable, '-m', 'pip', 'show', pkg['Name'].split(".")[0]]).decode("utf-8")
            pkg_info = pkg_info.splitlines()
            for info in pkg_info:
                # Split on the first colon.
                split_info = info.split(": ", 1)
                if split_info[0] in ['Name', 'Version', 'Summary', 'Home-page', 'Author', 'Licence']:
                    if split_info[0] != 'Name':
                        pkg[split_info[0]] = split_info[1]
                    else:
                        if "." not in pkg['Name']:
                            pkg[split_info[0]] = split_info[1]
        except subprocess.CalledProcessError as e:
            print(e, "PIP has no info for this package. Package is likely a Python built in.")

# Now all information has been collected, format it into a nice MD doc.
f = open((cwd + "_attribution.md"), 'w')
f.write(str("# " + cwd + " Attribution.  \n"))
for file in py_files:
    f.write(str("## " + file['Name'] + ":  \n"))
    for pkg in file['pkgs']:
        f.write(str("Package: " + pkg['Name'] + "  \n"))
        f.write(str("Version: " + pkg['Version'] + "  \n"))
        f.write(str("Summary: " + pkg['Summary'] + "  \n"))
        f.write(str("Website: " + "[{0}]({0})".format(pkg['Home-page']) + "  \n"))
        f.write(str("Author: " + pkg['Author'] + "  \n"))
        f.write(str("Licence: " + "[{0}]({0})".format(pkg['Licence']) + "  \n\n"))

f.close()
