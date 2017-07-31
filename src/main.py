#-*- coding:utf-8 -*-
import sys
import os
dirsept = os.path.sep
workdir = os.path.dirname(__file__)
module_path = workdir + dirsept + "modules" + dirsept
sys.path.append(module_path)
from openfile import FileOperator as fo
import xml.etree.ElementTree as et

def main():
    wpr = et.parse(workdir + dirsept + "settings.xml")
    sp = ""
    for s in wpr.findall(".//source"):
        if s.attrib["type"] == "defaultfile":
            sp = s.attrib["href"].replace("$USERPROFILE", os.environ.get('USERPROFILE'))
            break
    flo = fo(sp)
    ofp = open(workdir + dirsept + "temp.html", 'w', encoding='utf-8')
    ofp.write(flo.parseTag())
    ofp.close()
    flo.writeToLog()
    del flo

if __name__ == "__main__":
    main()
