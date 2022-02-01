#!/usr/local/bin/python3
import os, subprocess, sys

def getCommandOutput(command):
    return subprocess.check_output(command, shell=True, universal_newlines=True)

def copyApp(cmd, path):
    # bruh vcp doesn't accept -r
    os.system('%s -R "%s" /Applications'%(cmd, path))

def installDmg(cpcmd, pathToFile):
    # Split output from commnad that mounts dmg file
    searchForBlock = getCommandOutput("hdiutil attach '%s' | grep /Volumes"%pathToFile).split(" ")
    # Remove \n from last element, since it caused problems
    searchForBlock[len(searchForBlock)-1] = searchForBlock[len(searchForBlock)-1].translate({ord('\n'): None})

    pathToApp = ""

    # Searching for volume name in /Volumes using output from above
    for i in range(0, len(searchForBlock)):
        if "/Volumes/" in searchForBlock[i]:
            searchForBlock[i] = searchForBlock[i].translate({ord('\t'): None})
            pathToApp = pathToApp + searchForBlock[i] + " "
            for j in range(i+1, len(searchForBlock)):
                pathToApp = pathToApp + searchForBlock[j] + " "

    pathToApp = pathToApp[:-1]

    isThereAnotherDmg = getCommandOutput('find "%s" -iname "*.dmg"'%pathToApp) != ''

    if isThereAnotherDmg == True:
        pathToSecondDmg = getCommandOutput('find "%s" -iname "*.dmg"'%pathToApp)
        pathToSecondDmg = pathToSecondDmg[:-1]
        os.system('cp "%s" /tmp/working.dmg'%pathToSecondDmg)
        # When there'are more than 1 dmg files, cp will throw errors, but it works (I'm too tired rn to fix this)
        installDmg(cpcmd, "/tmp/working.dmg")
        os.system('rm -f /tmp/working.dmg')

    # Search for .pkg and .dmg files
    isTherePkgFile = getCommandOutput('find "%s" -maxdepth 2 -iname "*.pkg"'%pathToApp) != ''
    isThereAppFile = getCommandOutput('find "%s" -maxdepth 2 -iname "*.app"'%pathToApp) != ''

    if isTherePkgFile == True:
        os.system('sudo installer -pkg "$(find "%s" -maxdepth 2 -iname "*.pkg")" -target /'%pathToApp)
    elif isThereAppFile == True:    
        copyApp(cpcmd, getCommandOutput('find "%s" -maxdepth 2 -iname "*.app"'%pathToApp)[:-1])
    else:
        sys.exit("File not found.")
    
    os.system("hdiutil detach %s"%searchForBlock[0])
        

# Original .dmg file location
File_location = ""
if __name__ == '__main__':
    # Check whether user has vcp installed
    if getCommandOutput('which vcp') != '':
        cpCmd = "vcp"
    else:
        cpCmd = "cp"
    
    # Get file name
    for i in range(1, len(sys.argv)):
        File_location = File_location + sys.argv[i] + " "

    File_location = File_location[:-1]

    if ".zip" in File_location:
        tmpDir = "/tmp/working"
        os.system('mkdir "%s" && unzip "%s" -d "%s"'%(tmpDir, File_location, tmpDir))
    
        # Check type of file in archive and install it
        if getCommandOutput('find "%s" -maxdepth 1 -iname "*.app"'%tmpDir) != '':
            AppLoc = getCommandOutput('find "%s" -maxdepth 1 -iname "*.app"'%tmpDir)
            copyApp(cmCmd, AppLoc[:-1])
            os.system('rm -rf "%s"'%tmpDir)
            sys.exit("Done.")
        
        elif getCommandOutput('find "%s" -maxdepth 1 -iname "*.pkg"'%tmpDir) != '':
            PkgLoc = getCommandOutput('find "%s" -maxdepth 1 -iname "*.pkg"'%tmpDir)
            os.system('sudo installer -pkg "%s" -target /'%PkgLoc[:-1])
            os.system('rm -rf "%s"'%tmpDir)
            sys.exit("Done.")
        
        elif getCommandOutput('find "%s" -maxdepth 1 -iname "*.dmg"'%tmpDir) != '':
            File_location = getCommandOutput('find "%s" -maxdepth 1 -iname "*.dmg"'%tmpDir)
            installDmg(cpCmd, File_location[:-1])
            os.system('rm -rf "%s"'%tmpDir)
        
        else:
            os.system('rm -rf "%s"'%tmpDir)
            sys.exit("No usable files in archive")
    
    elif ".dmg" not in File_location:
        sys.exit("File is not .dmg nor .zip")

    else:
        installDmg(cpCmd, File_location)
