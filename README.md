# dmginstall-python
 Dmg installer script, written in python. Pkg, tgz, tbz, tar.gz, tar,bz and zips also work.

## Requirements
Homebrew  
python3 from Homebrew  
Xcode Command Line Tools (install by typing in terminal ```xcode-select --install```)  
vcp (optional, read below)

## Installation
### Manual
```bash
git clone https://github.com/Maciek-Hetman/dmginstall-python.git
cd dmginstall-python
cp dmginstall.py /usr/local/bin/dmginstall
cp vcp /usr/local/bin/vcp
```
Done.
### A bit less manual
```bash
git clone https://github.com/Maciek-Hetman/dmginstall-python.git
cd dmginstall-python
./update
``` 
## vcp
vcp is alternative to cp, with progress bar. It's optional if you don't necessarily
need it. It's compiled from [this github repo](https://github.com/Leask/VCP). See [copyright](vcp/COPYRIGHT).

## How to use it
When given zip file, it unzips it, detects file type installs and remove unzipped files. It can also
Script detect given file format, in case of dmg it automatically mounts, copy and umount dmg file.
install .pkg files using ```sudo installer -pkg [filename] -target /```.
You can also use ```dmginstall -d``` option to delete installed file and ```dmginstall -r``` to
install newest file in given directory. For example:  
```dmginstall -d -r ~/Downloads``` - this will pick newest file in your downloads folder,
install it and delete original file  
```dmginstall -d ~/Downloads/app.dmg``` - this will install file and delete app.dmg  
All options you can see with ```dmginstall -h```  
![dmg](Screenrecords/dmg_install.gif)
![dmg in zip](Screenrecords/dmg_in_zip.gif)
![pkg in zip](Screenrecords/pkg_in_zip.gif)

## Updating
Use update script
```bash
./update.py
```