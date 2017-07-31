#-*- coding:utf-8 -*-
import __main__ as mn
from xmlpw import XmlParserWrapper as xpw
import util.decorator as decos
import util.exception as errs
import re
from datetime import datetime as dt

InsertPart = "<!--[*PAGEBODY*]-->"

class FileOperator:
    def __init__(self, filename):
        self.log = ""
        self.__xmlpw__ = xpw(mn.module_path + "tcHameln.xml")
        self.tagSpecifier = [self.__xmlpw__.xmldomtree.getroot().attrib["tagbegin"], self.__xmlpw__.xmldomtree.getroot().attrib["tagend"]]
        regexes = self.__xmlpw__.getTranslationTable()
        self.regexes = dict()
        for rk in list(regexes.keys()):
            self.regexes[rk] = re.compile(regexes[rk].replace("$tagbegin",self.tagSpecifier[0]).replace("$tagend",self.tagSpecifier[1]))
        self.bbregex = self.regexes["Others"]
        del self.regexes["Others"]
        self.bbtc = self.__xmlpw__.getTCHETranslationTable()
        self.tagClasses = list(self.bbtc.keys())
        self.__sourcepath__ = filename
        __source__ = open(filename, 'r', encoding='utf-8')
        self.source = __source__.read().replace('\r', '')
        __source__.close()
        self.lines = self.source.split("\n")
        tmp = open(mn.module_path + "Template.html", 'r', encoding='utf-8')
        self.template = tmp.read()
        tmp.close()

    def parseTag(self):
        ret = self.source
        while True:
            matched = self.bbregex.search(ret)
            if id(matched) == id(None):
                break
            if not matched.group(1) in self.tagClasses:
                line = 0
                for l in self.lines:
                    line = line + 1
                    if not l.find(matched.group(0)) == -1:
                        break
                raise errs.ParseException("The tag neme '" + matched.group(1) + "' is unexpected. Please check source.\nat " + self.__sourcepath__ +
                ", line " + str(line) + ", Exception " + matched.group(0))
            hent = self.bbtc[matched.group(1)]["htmlentity"]
            atrb = "class=" + self.bbtc[matched.group(1)]["name"]
            print(matched.group(0) + "\treplaced as " + htmldcw(hent, matched.group(2), atrb))
            self.log = self.log + matched.group(0) + "\treplaced as " + htmldcw(hent, matched.group(2), atrb) + "\n"
            ret = ret.replace(matched.group(0), htmldcw(hent, matched.group(2), atrb))
        try:
            for e in list(self.regexes.keys()):
                while True:
                    matched = self.regexes[e].search(ret)
                    if id(matched) == id(None):
                        raise errs.ThroughLoop
                    if e == "ruby":
                        print(matched.group(0) + "\treplaced as " + setruby(matched.group(1), matched.group(2)))
                        self.log = self.log + matched.group(0) + "\treplaced as " + setruby(matched.group(1), matched.group(2)) + "\n"
                        ret = ret.replace(matched.group(0), setruby(matched.group(1), matched.group(2)))
                    elif e == "dotamark":
                        rby = "&#x30fb;" * len(matched.group(1))
                        print(matched.group(0) + "\treplaced as " + setruby(matched.group(1), rby))
                        self.log = self.log + matched.group(0) + "\treplaced as " + setruby(matched.group(1), rby) + "\n"
                        ret = ret.replace(matched.group(0), setruby(matched.group(1), rby))
        except errs.ThroughLoop:
            pass
        ret = ret.replace('\n', '<br>')
        return self.template.replace(InsertPart, ret)

    def writeToLog(self):
        if self.log == "":
            return
        f = open(mn.workdir + mn.dirsept + "processlog" + dt.now().strftime("%Y%m%d_%H%M%S") + ".log", 'w')
        f.write(self.log)
        f.close()


@decos.tagAdder_ruby
def setruby(tgt = "",rby = ""):
    	return tgt + "<rt>" + rby + "</rt>"

def htmldcw(tag:str, value:str, attr = ""):
    @decos.tagAdder(tag, attr)
    def _sfunc(val):
        return val
    return _sfunc(value)
