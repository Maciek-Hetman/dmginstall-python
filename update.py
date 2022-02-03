#!/usr/local/bin/python3
from operator import ge
import subprocess
import os

def getCommandOutput(command):
    subprocess.check_output(command, shell=True, universal_newlines=True)

if getCommandOutput('which dmginstall') == '':
    os.system('cp dmginstall.py /usr/local/bin/dmginstall')
else:
    os.system('rm $(which dmginstall)')
    os.system('cp dmginstall.py /usr/local/bin/dmginstall')