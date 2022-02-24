from pyjavaproperties import Properties
from FileHandler.filehandler import copyNewLocally, createFinalFile

def execPParser(prod,ver,prop):
    pathToCur = prop
    pathToNew = copyNewLocally(prod,ver)
    kvToAdd = {}
    if prod == 'Demo': #utility designed for possible future use with more than one product type
        agencyProfileTags = []
        defaultProfileTags = ['TABLETS','PHONES','OTHER'] #create generic profile tags
        deviceKeys = ('device.config.example.ipaddr','device.config.example.id','device.config.example.pairing')


        class DemoProps():
            def gatherPropAttributes(self,keyname):
                def cleanUpKey(keyname):
                    if a5['isOBDEntry'] == True:
                        return keyname[keyname.find('.')+1:keyname.find('(')]
                        #self.attributes['cleanedUpKey'] = keyname[keyname.find('.')+1:keyname.find('(')]
                    elif a3['startswithTag'] == True and a4['endswithDigit'] == True:
                        return keyname[keyname.find('.')+1:keyname.rfind('.')]
                        #self.attributes['cleanedUpKey'] = keyname[keyname.find('.')+1:keyname.rfind('.')]
                    elif a3['startswithTag'] == True:
                        return keyname[keyname.find('.')+1:]
                        #self.attributes['cleanedUpKey'] = keyname[keyname.find('.')+1:]
                    elif a4['endswithDigit'] == True:
                        return keyname[:keyname.rfind('.')]
                        #self.attributes['cleanedUpKey'] = keyname[:keyname.rfind('.')]
                    else: #this key has neither a tag nor a digit, so we take the name
                        return keyname
                        #self.attributes['cleanedUpKey'] = keyname
                x = {}

                a1 = {'valBeforeFirstDot': str(keyname)[:str(keyname).find('.')]}
                x.update(a1)

                a2 = {'valAfterLastDot': str(keyname)[str(keyname).rfind('.')+1:]}
                x.update(a2)

                a3 =  {'startswithTag': bool()}
                if a1['valBeforeFirstDot'] in defaultProfileTags or a1['valBeforeFirstDot'] in agencyProfileTags:
                    a3['startswithTag'] = True
                else:
                    a3['startswithTag'] = False
                x.update(a3)

                a4 = {'endswithDigit': bool()}
                if a2['valAfterLastDot'].isdigit() == True:
                    a4['endswithDigit'] = True
                else:
                    a4['endswithDigit'] = False
                x.update(a4)

                a5 = {'isOBDEntry': bool()}
                if a3['startswithTag'] == True and str(keyname)[str(keyname).find('.')+1:].startswith(deviceKeys):
                    a5['isOBDEntry'] = True
                else:
                    a5['isOBDEntry'] = False
                x.update(a5)

                a6 = {'cleanedUpKey': cleanUpKey(keyname)}
                x.update(a6)

                return x

            def __init__(self,keyname,keyval):
                self.key = {keyname: keyval}
                self.attributes = self.gatherPropAttributes(keyname)

            def __eq__(self, other):
                return self.attributes['cleanedUpKey'] == other.attributes['cleanedUpKey']

    def gatherKeys(file,compPlace):
        p = Properties()
        p.load(open(file))
        #logging.info('Opened file '+"'"+file+"'"+ 'as properties for desired version')
        if prod == 'Demo':
            def generateListofProfileTags(compPlace):
                for k, v in p.items():
                    if k.startswith('device.server.profile.tag'):
                        if compPlace == 'cur':
                            agencyProfileTags.append(v)
                            #logging.info('adding '+v+' to list of profile agency profile tags')
                        else:
                            defaultProfileTags.append(v) #we discovered that our files from Deliverables will have uncommented values for profile tags that weren't explicitly (or properly) declared, so we'll add those tags to the default list
                            #logging.info('adding '+v+' to list of default profile tags for selected version')
            generateListofProfileTags(compPlace)
            i = []
            for k,v in p.items():
                i.append(DemoProps(k,v))
        p.close
        return i

    def fetchMissingKV(cur,new):
        optkeyCleanedUp = ['payment.info']
        for x in new:
            if x not in cur:
                if x.attributes['isOBDEntry'] == True: 
                    print('skipping '+x.attributes['cleanedUpKey'])
                elif x.attributes['startswithTag'] == True and x.attributes['endswithDigit'] == True and x.attributes['cleanedUpKey'] not in optkeyCleanedUp:
                    for i in agencyProfileTags:
                        counter = 1
                        for item in x.key:
                            key = i+'.'+x.attributes['cleanedUpKey']+'.'+str(counter)
                            keyVal = x.key[item]
                            if key not in kvToAdd.keys():
                                kvToAdd.update({key: keyVal})
                        counter += 1
                elif x.attributes['startswithTag'] == True and x.attributes['cleanedUpKey'] not in optkeyCleanedUp:
                    for i in agencyProfileTags:
                        counter = 1
                        for item in x.key:
                            key = i+'.'+x.attributes['cleanedUpKey']
                            keyVal = x.key[item]
                            if key not in kvToAdd.keys():
                                kvToAdd.update({key: keyVal})
                        counter += 1
                elif x.attributes['endswithDigit'] == True and x.attributes['cleanedUpKey'] not in optkeyCleanedUp:
                    for item in x.key:
                        key = x.attributes['cleanedUpKey']+'.'+1
                        keyVal = x.key[item]
                        if key not in kvToAdd.keys():
                                kvToAdd.update({key: keyVal})
                elif x.attributes['cleanedUpKey'] not in optkeyCleanedUp:
                    for item in x.key:
                        key = x.attributes['cleanedUpKey']
                        keyVal = x.key[item]
                        if key not in kvToAdd.keys():
                                kvToAdd.update({key: keyVal})
        #return keysToAdd

    curProps = gatherKeys(pathToCur,'cur')
    newProps = gatherKeys(pathToNew,'new')
    fetchMissingKV(curProps,newProps)
    if len(kvToAdd) > 0:
        createFinalFile(prop,kvToAdd)
        return 'Added '+str(len(kvToAdd))+' to new output file'
    else:
        return 'There were no key differences between the current and new properties files. Your original file has not been altered'
