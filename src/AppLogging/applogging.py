import logging
import datetime
#from PParser.pparser import *

formattedDateTime = datetime.datetime.now().strftime("%H%M%S_%y%m%d")
logging.basicConfig(filename='.\\logs\\DEBUG_for_'+formattedDateTime+'.log',level=logging.INFO)
