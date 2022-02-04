#!/usr/local/bin/python3
import os, subprocess, sys

# More number more newer
VERSION = "0.4.0"   # Yeah, it's just a random number

def printHelp():
    message = """
    dmginstall - universal dmg/pkg installer for MacOS
    Version: %s

    Usage:
    dmginstall /path/to/file
    dmginstall [-r|--recent] /path/to/directory
    
    Options:
    -r - installs recently modified file in given directory
    -h - prints this message
    
    --recent - same as "-r"
    --help - same as "-h"\n """%VERSION
   
    print(message)
    sys.exit() 

def getCommandOutput(command):
    return subprocess.check_output(command, shell=True, universal_newlines=True)

def copyApp(cmd, path):
    os.system('%s -R "%s" /Applications'%(cmd, path))

def installDmg(pathToFile, cpCmd):
    pathToApp = ""

    # Best way I found so far to get volume name and block device
    searchForBlock = getCommandOutput('hdiutil attach "%s" | grep /Volumes'%pathToFile).split(" ") 
    searchForBlock[len(searchForBlock)-1] = searchForBlock[len(searchForBlock)-1].translate({ord('\n'): None})

    for i in range(0, len(searchForBlock)):
        if "/Volumes/" in searchForBlock[i]:
            searchForBlock[i] = searchForBlock[i].translate({ord('\t'): None})
            pathToApp = pathToApp + searchForBlock[i] + " "
            for j in range(i+1, len(searchForBlock)):
                pathToApp = pathToApp + searchForBlock[j] + " "

    pathToApp = pathToApp[:-1]

    if getCommandOutput('find "%s" -iname "*.dmg"'%pathToApp) != '':
        pathToSecondDmg = getCommandOutput('find "%s" -iname "*.dmg"'%pathToApp)
        pathToSecondDmg = pathToSecondDmg[:-1]
        os.system('cp "%s" /tmp/working.dmg'%pathToSecondDmg)
        installDmg(cpcmd, "/tmp/working.dmg")   # cp throwed some errors but it worked anyways. Didn't tested with vcp yet.
        os.system('rm -f /tmp/working.dmg')
    
    installFromArchive(pathToApp, cpCmd)
    os.system("hdiutil detach %s"%searchForBlock[0])
     
def installFromArchive(workingDir, cpCmd):
    if getCommandOutput('find "%s" -maxdepth 1 -iname "*.app"'%workingDir) != '':
        copyApp(cpCmd, getCommandOutput('find "%s" -maxdepth 1 -iname "*.app"'%workingDir)[:-1])
    
    elif getCommandOutput('find "%s" -maxdepth 1 -iname "*.pkg"'%workingDir) != '':
        os.system('sudo installer -pkg "%s" -target /'%(getCommandOutput('find "%s" -maxdepth 1 -iname "*.pkg"'%workingDir)[:-1]))
    
    elif getCommandOutput('find "%s" -maxdepth 1 -iname "*.dmg"'%workingDir) != '':
        installDmg(getCommandOutput('find "%s" -maxdepth 1 -iname "*.dmg"'%workingDir)[:-1], cpCmd)
        if getCommandOutput('find "%s" -maxdepth 2 -iname "*.app"'%workingDir) != '':
            copyApp(cpCmd, getCommandOutput('find "%s" -maxdepth 2 -iname "*.app"'%workingDir)[:-1])
        elif getCommandOutput('find "%s" -maxdepth 2 -iname "*.pkg"'%workingDir) != '':
            os.system('sudo installer -pkg "$(find "%s" -maxdepth 2 -iname "*.pkg")" -target /'%workingDir)
    
    else:
        sys.exit("No usable files found.")   


##########################################################
# Main code, nicely separated from rest of the functions # 
##########################################################
if __name__ == '__main__':
    fileLocation = ""
    dirLocation = ""
    tmpDir = "/tmp/dmginstall"
    args = sys.argv
    delete = False

    if "-h" in args or "--help" in args:
        printHelp()
    
    if "-r" in args:
        for i in range(args.index("-r")+1, len(sys.argv)):
            dirLocation = dirLocation + sys.argv[i] + " "

        fileLocation = dirLocation[:-1] + "/" + getCommandOutput('ls -Art "%s" | tail -n 1'%dirLocation[:-1])
        del args[args.index('-r')+1]
        args.remove('-r')
        print(fileLocation)

    if "-d" in args:
        delete = True
        args.remove("-d")
    
    else:
        for i in range(1, len(args)):
            fileLocation = fileLocation + sys.argv[i] + " "
        
        fileLocation = fileLocation[:-1]
        
    if getCommandOutput('which vcp') != '':
        cpCmd = "vcp"
    else:
        cpCmd = "cp"

    print(fileLocation)

    if ".zip" in fileLocation:
        os.system('mkdir "%s" && unzip "%s" -d "%s"'%(tmpDir, fileLocation, tmpDir))
        installFromArchive(tmpDir, cpCmd)
        os.system('rm -rf "%s"'%tmpDir)
    
    elif ".tgz" in fileLocation or "tar.gz" in fileLocation:
        os.system('mkdir "%s" && tar -xf "%s" -C "%s"'%(tmpDir, fileLocation, tmpDir))
        installFromArchive(tmpDir, cpCmd)
        os.system('rm -rf "%s"'%tmpDir)
    
    elif ".tbz" in fileLocation or "tar.bz2" in fileLocation:
        os.system('mkdir "%s" && tar -xjf "%s" -C "%s"'%(tmpDir, fileLocation, tmpDir))
        installFromArchive(tmpDir, cpCmd)
        os.system('rm -rf "%s"'%tmpDir)
    
    elif ".dmg" not in fileLocation:
        sys.exit("File type is not supported")

    else:
        installDmg(fileLocation, cpCmd)
