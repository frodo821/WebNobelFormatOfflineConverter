#-*- coding:utf-8 -*-
#import __main__ as mn
import xml.etree.ElementTree as et

class XmlParserWrapper:
    def __init__(self, path):
        self.__xmlpath__ = path
        self.xmldomtree = et.parse(self.__xmlpath__)
        self.tree = self.__gchldrn__(self.xmldomtree.getroot())

    def __gchldrn__(self, element):
         cldrn = list(element)
         ret = {element.tag:{}}
         if not len(element.attrib) == 0:
              ret[element.tag].update({"attribute":element.attrib})
         if not len(cldrn) == 0:
              ret[element.tag]["children"] = {}
              for e in cldrn:
                   ret[element.tag]["children"].update(self.__gchldrn__(e))
         return ret

    def getTranslationTable(self):
        ttr = self.xmldomtree.findall(".//translation")
        otr = self.xmldomtree.find(".//toc")
        ret = {}
        for t in ttr:
            ret[t.attrib["name"]] = t.attrib["regex"]
        ret["Others"] = otr.attrib["regex"]
        return ret

    def getTCHETranslationTable(self):
        tchet = self.xmldomtree.findall(".//class")
        ret = {}
        for t in tchet:
            ret[t.attrib["tag"]] = {"name":t.attrib["name"], "htmlentity":t.attrib["htmlentity"]}
        return ret
