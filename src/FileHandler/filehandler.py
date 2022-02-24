from shutil import copy
from os import scandir, path
from AppLogging.applogging import *

availableProds = ['Demo']
base_product_path = '\\\\servername\\path\\to_product\\' #example of variable for pulling config files from network fileshare
prodInfoDict = {'Demo':'new\\','Example1':'subdirectory\\for\\service_config'} #examples to demonstrate logic for future support of multiple services

class filePath(str):
    def __init__(self,path,compPlacement):
        self.path = path
        self.path = ''
        self.compType = compType

        if self.name.startswith('cur'):
            self.compType = 'cur'
        elif self.name.startswith('new'):
            self.compType = 'new'
        else:
            raise Exception('Unknown filetype')

def productPath(prod):
    if prod == 'Demo':
        return prodInfoDict[prod]
    elif prod in availableProds and prod != 'Demo':
        return base_product_path+prodInfoDict[prod]
    else:
        raise Exception('We do not currently support that product')

def listVersions(x):
    ver_list = []
    if x == '':
        return ''
    elif x == 'Demo':
        return 'N/A'
    else:
        with scandir(productPath(x)) as entries:
            for entry in entries:
                if entry.name[0].isnumeric() == True:
                    if entry.name[0] >= '7':
                        ver_list.append(entry.name)
        return ver_list

def copyNewLocally(prod,ver):
    if prod == 'Demo':
        logging.info("Product is 'Demo' so we'll use the local properties in directory 'new' ")
        return path.abspath('new\\demo_new.properties')
    else:
        i = base_product_path+prodInfoDict[prod]+ver
        with scandir(i) as contents:
            for x in contents:
                logging.info("Scanning directory"+'"'+i+'"'+' for properties files')
                if x.is_file() == True and path.splitext(x)[1] == '.properties':
                    logging.info('Found a properties file and will copy it into the local '+'"'+'new'+'"'+' folder')
                    return copy(x.path,'new\\')


def createFinalFile(prop,kvtoadd):
    f = copy(prop,'output\\')
    logging.info("Created file "+"'"+f+"'"+" to save our updates")
    fo = open(f,"a")
    fo.write("\n"+'# THE FOLLOWING LINES HAVE BEEN APPENDED BY THE SERVICE PROPERTIES PPARSER UTILITY #'+"\r\n") #needs an update
    for key, value in kvtoadd.items():
        fo.write(key + ' = ' + value + "\r\n")
    fo.close
