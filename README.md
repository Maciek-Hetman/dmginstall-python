# dmginstall-python
 Dmg installer script, written in python. Pkg and zips also work.

## Requirements
Homebrew  
python3 from Homebrew  
Xcode Command Line Tools (install by typing in terminal ```xcode-select --install```)  
vcp (optional, read below)

## Installation
```bash
cp dmginstall.py /usr/local/bin/dmginstall
cp vcp /usr/local/bin/vcp
```
Done.

## Usage
Type in terminal of your choice 
```bash
dmginstall /path/to/dmg/file.dmg 
```
You can also drag file to terminal window instead of manually typing whole path

## vcp
vcp is alternative to cp, with progress bar. It's optional if you don't necessarily
need it. It's compiled from [this github repo](https://github.com/Leask/VCP). See [copyright](vcp/COPYRIGHT).
