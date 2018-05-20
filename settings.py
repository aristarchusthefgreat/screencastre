#!/usr/bin/python3

import configparser, os.path, types
from pathlib2 import Path

class InitConfig:

    def __init__(self):
        self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        
        settings_file = Path('config.ini')

        if settings_file.exists():
            self.config.read(settings_file)

    def modifySettings(self, setting_section, setting_key, setting_new_value):
        if type(setting_new_value) is list:
            tmp_val = ','.join(str(e) for e in setting_new_value)

        if 'tmp_val' in locals():
            self.config.set(setting_section, setting_key, tmp_val)
            tmp_val = tmp_val.encode('utf-8')
        else:
            self.config.set(setting_section, setting_key, setting_new_value)
            tmp_val = setting_new_value.encode('utf-8')

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile) 
    
    def getSettings(self):
        pass
    
    
        