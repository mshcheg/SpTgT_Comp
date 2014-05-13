
#!/bin/python 

'''
    A python script for concatonating nexus files in multiples of 3 and *optional* running Mr. Bayes.    
'''

import sys 
import os
#from random import randint 
#did not end up using random numbers, built up the concatonated files in the order they were encounted in the input directory  

def CreateNexus(SequenceList, OutName, nchar):
    MrBayesOut = os.path.splitext(OutName)[0]
    
    #Retain "begin mrbayes" block only once
    command = ["\nbegin mrbayes;", "\n\tset autoclose=yes nowarn=yes;", "\n\tprset brlenspr=clock:uniform;", "\n\tprset statefreqpr=dirichlet(1,1,1,1);", "\n\tlset nst=2 rates=gamma Ngammacat=4;", "\n\tmcmc ngen=110000  Stoprule=yes Stopval=0.01 relburnin=yes burninfrac=0.25 samplefreq=100;", "\n\tsumt Nruns=2 Contype=Allcompat;", "\n\tfilename=%s;"%MrBayesOut, "\nquit;\nend;"]
    header = ["Begin DATA; [Tree 1]\n", "\tDimensions NTAX=8 NCHAR=%s;\n"%nchar, "\tFormat MISSING=? GAP=- DATATYPE=DNA;\n", "\tMatrix\n"]
	
    with open(OutName, 'w') as outfile:
        outfile.write("#NEXUS\n\n")
        outfile.write(''.join(header))
        outfile.write(''.join(SequenceList))
        outfile.write('\t;\nEND;\n\n')
        outfile.write(''.join(command))

def ReadFile(currentNexusFile):
    blackhole = [currentNexusFile.readline() for x in xrange(6)] #Read the first 6 lines of the nexus file, we don't need these 
    SequenceList = [currentNexusFile.readline().strip("\n") for x in xrange(8)] #Read the 8 sequence lines from the nexus file
    SplitSequenceList = [(x.split()[0], [x.split()[1]]) for x in SequenceList] 
    
    return SplitSequenceList

#Define variables from program arguments 
infolder = sys.argv[1] #Argument 1 = input folder  
try: #Test for the presence of an optional outfolder argument
    assert len(sys.argv) == 3
    outfolder = sys.argv[2] #Argument 2 = output folder
except AssertionError:
    print "You did not provide an output directory. Please rerun with an outdir option."
    exit(1) 

#Perform action for files with common _ST#
#Make a list of all nexus files in the input folder 
NexusList = [x for x in os.listdir(infolder) if ".nex" in x]

SpTreeName = NexusList[0].split("_")[1].split(".")[0]

concatonatedSequenceDictionary={}
#Continue loop by threes (and modify script/additional scripts for looping by 9s and by 27s)
#For concatenating by 3s, consider e.g. Tree1_ST1.nex Tree2_ST1.nex and Tree3_ST1.nex - then the next three
for counter in range(3,len(NexusList)+3,3):
    NextthreeFiles = NexusList[counter-3:counter]
    outFileName = os.path.join(outfolder, "Tree%sx%s_%s.nex"%(1, counter, SpTreeName))
    #Change nchar to 3000 for concatenating by 3s (to 9000 for 9s, to 27000 for 27s)
    sequenceLength = counter*1000
    #Add species sequences for Tree2 and Tree3, paying attention to species (signified by 1, 2,...8)
    if counter == 3:		
        for nexusFile in NextthreeFiles:
            nexusPath = os.path.join(infolder, nexusFile)
            with open(nexusPath, 'r') as currentNexusFile:		
                SplitSequenceList = ReadFile(currentNexusFile)  
            if NextthreeFiles.index(nexusFile) == 0:
                concatonatedSequenceDictionary = dict(SplitSequenceList)                
            else:
                for pair in SplitSequenceList:
                    concatonatedSequenceDictionary[pair[0]].extend(pair[1])
        linelist = []
        for lineNum, sequences in concatonatedSequenceDictionary.items():
            linelist.append('%s %s\n'%(lineNum,''.join(sequences)))
        CreateNexus(linelist, outFileName, sequenceLength)
    else:
        for nexusFile in NextthreeFiles:
            nexusPath = os.path.join(infolder, nexusFile)
            with open(nexusPath, 'r') as currentNexusFile:		
                SplitSequenceList = ReadFile(currentNexusFile)  
            for pair in SplitSequenceList:
                concatonatedSequenceDictionary[pair[0]].extend(pair[1])
        linelist = []
        for lineNum, sequences in concatonatedSequenceDictionary.items():
            linelist.append('%s %s\n'%(lineNum,''.join(sequences)))
        #Save new mrbayes file as, e.g. Tree1x3_ST1.nex
        CreateNexus(linelist, outFileName, sequenceLength)

'''
This is an optional block of code to run Mr. Bayes for the concatonated nexus files. Uncomment it if you want to run Mr. Bayes as part of this script.

NEXUSList = [x for x in os.listdir(outfolder) if ".nex" in x] #create a list of the nexus files written to the output directory

for NexusFile in NEXUSList:
    NexusPath = os.path.join(outfolder, NexusFile)
    os.system("mb %s" %NexusPath) #run mr bays   
    print "Mr. BayEs ran sucessfully from file %s" %NexusFile
'''
