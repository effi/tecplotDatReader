# tecplotDatReader
A class to read ASCII Tecplot-Files with multiple sections with Python and store them in numpys ndarrays for manipulation and matplotlib visualization 

# Shortcomings
Currently solutiontime-parsing is not included! 

# How to use it

Initiate a new parser with 
parser = tecplotDataReader('path/to/dat/file.dat')

The parser automatically generates metadata about your dat-file:
* A List of Seciton-Names: parser.sectionName
* A List of Variables: parser.variables
..

the sections are ordered for looping. You can show the looporder by calling
parser.printSections()
if you don't like the order, you can move entries to the end by calling
parser.moveSectionToEnd(sectionNumberInTheOutputList!)

The parses will not automatically parse the whole data!
You can now parse the data section by section by calling:
parser.readSection(indexOfSection)

or read all sections by calling:
parser.readAllSections()
!!reading all sections can slow down programm execution for excessive .dat files!!

the data itself is stored in a list at
parser.sectionData.

You can Adress it by the original order of the file:
parser.sectionData[originalNumber]

or by the reordered number that you created with the "moveSectionToEnd()" method:
parser.reorderedData(orderedNumber)





