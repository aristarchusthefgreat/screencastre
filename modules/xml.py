import xml.etree.cElementTree as ET
import os


class ParseXMLSettings:
    root = None
    tree = None
    settings_list = dict()

    def __init__(self):
        self.root = ET.parse(os.path.join(os.path.dirname(os.path.realpath('settings.xml')), 'settings.xml')).getroot()
        for elem in self.root:
            for item in elem:
                self.settings_list[item.tag] = item.text

    def get(self):
        return self.settings_list

    def set(self):
        for elem in self.root:
            for item in elem:
                self.settings_list[item.tag] = item.text

    def edit(self, tagname="", fieldvalue=""):
        self.tree = ET.parse(os.path.join(os.path.dirname(os.path.realpath('settings.xml')), 'settings.xml'))
        self.tree.find('DEFAULTS/'+tagname).text = fieldvalue
        self.tree.write(os.path.join(os.path.dirname(os.path.realpath('settings.xml')), 'settings.xml'))

