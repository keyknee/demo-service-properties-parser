from tkinter import *
from tkinter import ttk, font, messagebox
from tkinter.filedialog import askopenfilename
from FileHandler.filehandler import availableProds, listVersions
from PParser.pparser import execPParser
from AppLogging.applogging import *


class PParserUI:

    def __init__(self, root):
        self.root = root
        root.title("Service Properties Parser")
        root.iconbitmap(self,default='.\\app.ico') 
        self.font = font.Font(family='Helvetica')
        
        self.upToFrame = ttk.LabelFrame(root,text="Updating To: ")
        self.upToFrame.grid(column=0,row=0,columnspan=2,rowspan=2,padx=10,pady=10)
        
    #First row
        #Left column
        self.productLabel = Label(self.upToFrame,text='Product: ')
        self.productLabel.grid(column=0,row=0)

        self.slctProdVar = StringVar()
        self.prdList = []
        self.productCombo = ttk.Combobox(self.upToFrame,values=availableProds,textvariable=self.slctProdVar,state="readonly")
        self.productCombo.grid(column=0,row=1)
        
        #Right column
        self.versionLabel = Label(self.upToFrame,text='Version : ')
        self.versionLabel.grid(column=1,row=0)
        """ if supportedProds.__len__() == 1:
            self.productCombo.current(0)
            self.ver_list = listVersions(supportedProds[0]) """
        self.verListforProd = []
        self.selectedVer = StringVar()
        self.versionCombo = ttk.Combobox(self.upToFrame,textvariable=self.selectedVer,state="readonly",postcommand=self.getVerList) #need to reviw and update
        self.versionCombo.grid(column=1,row=1)
        
        self.slctProdVar.trace('w', self.setVerList)
    #Second row
        self.selectcurLabel = ttk.LabelFrame(root,text='Browse to Your Current Properties File: ')
        self.selectcurLabel.grid(column=0,row=2,padx=10,pady=10)
        
        self.selectedFileVar=StringVar()
        self.curPropFilePathEntry = Entry(self.selectcurLabel,textvariable=self.selectedFileVar,width=50)
        self.curPropFilePathEntry.grid(column=0,row=0)
        self.filebrowseButton = Button(self.selectcurLabel,text='Browse',command=self.openCurPropFile)
        self.filebrowseButton.grid(column=1,row=0)
    #Next row
        self.goButton = Button(root,text='Go',command=self.initiatePParser)
        self.goButton.grid(column=0,row=6)

    def setVerList(self, *args):
        x = self.slctProdVar.get()
        logging.info('Selected product '+'"'+x+'"')
        try:
            self.verListforProd = listVersions(x)
            logging.info('Found the following available versions for product '+x+': '+', '.join(map(str,self.verListforProd)))
        except FileNotFoundError:
                logging.ERROR('Failed to fetch available versions. Make sure you are on the company network or that you use product Demo') 
    def getVerList(self):
        self.versionCombo.config(values=self.verListforProd)
    def openCurPropFile(self):
        curPropFile = askopenfilename(filetypes =[('Properties Files', '*.properties')], initialdir = ".\cur")
        self.selectedFileVar.set(str(curPropFile))
        logging.info('Setting the location for the "current" properties file to '+curPropFile)
    def initiatePParser(self):
        ourProd = self.slctProdVar.get()
        ourVer = self.selectedVer.get()
        ourProp = self.selectedFileVar.get()
        slctedOptionsSummary = ('Current Product is',ourProd,'\n','Selected version is',ourVer,'\n','We will be comparing to properties at',ourProp)
        logging.info(slctedOptionsSummary)
        resultsMessage = execPParser(ourProd,ourVer,ourProp)
        logging.info('Initiating PParser backend...')
        messagebox.showinfo(message=resultsMessage)

root = Tk()
app_gui = PParserUI(root)
root.mainloop()


