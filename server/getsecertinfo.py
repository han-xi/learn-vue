import yaml
import os


class secert(object):
    def __init__(self):
        fileNamePath = os.path.abspath(os.path.join(os.getcwd(),'../'))
        yamlPath = os.path.join(fileNamePath,'namespace.yaml')
        with open(yamlPath,'r',encoding="utf-8") as f:
            serverinfo=yaml.load(f.read())
            self.server=serverinfo['server']
            self.mail=serverinfo['mail']
        


# fileNamePath = os.path.abspath(os.path.join(os.getcwd()))
# print(fileNamePath)
# yamlPath = os.path.join(fileNamePath,'namespace.yaml')
# print(yamlPath)
# with open(yamlPath,'r',encoding="utf-8") as f:
#     x=yaml.load(f.read())
#     print(type(x['mail']['send_mail']))
#     print(type(x['server']['port']))
#     x1=5
#     y=6
#     str(x1)+"{}".format(x['cal']['cal1'])+str(y)

