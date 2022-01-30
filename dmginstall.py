#!/usr/local/bin/python3
import os, subprocess, sys

File_location = ""

for i in range(1, len(sys.argv)):
    File_location = File_location + sys.argv[i] + " "

if ".dmg" not in File_location:
    sys.exit("File is not .dmg")

File_location = File_location[:-1]

def install(pathToFile):
    searchForBlock = subprocess.check_output("hdiutil attach '%s' | grep /Volumes"%pathToFile, shell=True, universal_newlines=True).split(" ")
    searchForBlock[len(searchForBlock)-1] = searchForBlock[len(searchForBlock)-1].translate({ord('\n'): None})

    pathToApp = ""

    for i in range(0, len(searchForBlock)-1):
        if "/Volumes/" in searchForBlock[i]:
            searchForBlock[i] = searchForBlock[i].translate({ord('\t'): None})
            pathToApp = pathToApp + searchForBlock[i] + " "
            for j in range(i+1, len(searchForBlock)):
                pathToApp = pathToApp + searchForBlock[j] + " "

    pathToApp = pathToApp[:-1]

    isThereAnotherDmg = subprocess.check_output('find "%s" -iname "*.dmg"'%pathToApp, shell=True, universal_newlines=True) != ''

    if isThereAnotherDmg == True:
        pathToSecondDmg = subprocess.check_output('find "%s" -iname "*.dmg"'%pathToApp, shell=True, universal_newlines=True)
        pathToSecondDmg = pathToSecondDmg[:-1]
        os.system('cp "%s" /tmp/working.dmg'%pathToSecondDmg)
        install("/tmp/working.dmg")
        os.system('rm -f /tmp/working.dmg')

    os.system('cp -r "$(find "%s" \( -iname "*.app" ! -iname "Autoupdate*" \))" /Applications/'%pathToApp)
    os.system("hdiutil detach %s"%searchForBlock[0])

install(File_location)
