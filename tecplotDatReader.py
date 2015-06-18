class tecplotDataReader(object):
    import numpy as np
    datafile=""
    fileLen=0
    sections=[]
    sectionName=[]
    sectionBegin=[]
    sectionEnd=[]
    sectionNodes=[]
    sectionData={}
    sectionLooporder=[]
    variables=[]
    index=0
    def __init__(self,datafile):
        self._clear()
        self.datafile=datafile
        # self.fileLen is using the throwaway returnvalue of the _getVariables method
        self.fileLen= self._getVariables() 
        self._getSections()
    
    def __iter__(self):
        return self
    def next(self):
        if self.index == len(self.sectionLooporder):
            raise StopIteration
        self.index = self.index +1
        return self.sectionLooporder[self.index-1]
    def resetIter(self):
        self.index = 0
#    
#    def __repr__(self):
#        return self.sections
#    
#    def __str__(self):
#        pass

    def _clear(self):
        self.datafile=""
        self.fileLen=0
        self.sections=[]
        self.SectionName=[]
        self.sectionBegin=[]
        self.sectionEnd=[]
        self.sectionNodes=[]
        self.sectionData={}
        self.variables=[]
        self.sectionLooporder=[]
        self.index=0
        
    def _getVariables(self):
        with open(self.datafile) as f:
            i=0
            for line in f:
                    i += 1
                    if line[0:9] == 'VARIABLES':
                        self.variables.append(re.findall(r'".*"', line)[0].strip('"'))
                    if line[0] == '"':
                        self.variables.append(re.findall(r'".*"', line)[0].strip('"'))    
        return i 
    
    def _getSections(self):
        with open(self.datafile) as f:
            i=0
            for line in f:
                    i += 1
                    if line[:4] == "ZONE":
                        self.sectionName.append(re.findall(r'".*"', line)[0].strip('"'))
                        self.sectionBegin.append(int(i+5))
                    if line[1:6] == "Nodes":
                        nodes=re.findall(r'Nodes=\d+',line)[0]
                        nodes=nodes[6:]
                        self.sectionNodes.append(nodes)
                        self.sectionEnd.append(self.sectionBegin[-1]+int(nodes)-1) 
            self.sections=range(len(self.sectionName))
            self.sectionLooporder=self.sections
        return i
    
    def readSection(self,section):
        self.sectionData[self.sections[section]]=np.genfromtxt(self.datafile,
              delimiter = " ",
              skip_header=(int(self.sectionBegin[section])-1),
              skip_footer=(self.fileLen-int(self.sectionEnd[section])),
              filling_values=0,
              invalid_raise=False,
              #Unpack true liefer eine Liste an listen statt einer matrix                               
              unpack=True 
              )

    def readAllSections(self):
        for i in range(len(self.sections)):
            self.readSection(i)
    
    def moveSectionToEnd(self,section):
        temp=self.sectionLooporder.pop(section)
        self.sectionLooporder.append(temp)
    
    def printSections(self):
        tempindex=self.index
        self.index=0
        for section in self:
            print str(section) + self.sectionName[section] 
        self.index=tempindex
