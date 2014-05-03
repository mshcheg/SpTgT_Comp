#!/bin/python 

'''
    A python script for generating nexus files and running Mr. Bayes.    
'''

import sys 
import os

def CreateNexus(LineList, OutName):
    MrBayesOut = os.path.splitext(OutName)[0]
    command = ["\nbegin mrbayes;", "\n\tset autoclose=yes \
nowarn=yes;", "\n\tprset brlenspr=clock:uniform;",\
    "\n\tprset statefreqpr=dirichlet(1,1,1,1);", "\n\tlset nst=2 rates=gamma \
Ngammacat=4;", "\n\tmcmc ngen=110000  Stoprule=yes Stopval=0.01 relburnin=\
yes burninfrac=0.25 samplefreq=100;", "sumt Nruns=2 Contype=Allcompat;", "\n\tfilename=%s;"%MrBayesOut, "\nquit;\nend;"]

    with open(OutName, 'w') as outfile:
        outfile.write("#NEXUS\n\n")
        outfile.write(''.join(LineList))
        outfile.write(''.join(command))

#Define variables from program arguments 
infolder = sys.argv[1] #Argument 1 = input folder  
try: #Test for the presence of an optional outfolder argument
    assert len(sys.argv) == 3
    outfolder = sys.argv[2] #Argument 2 = output folder
except AssertionError:
    outfolder = infolder #There is no second argument, output will go in the input folder 

#Make a list of all sequence files in the input folder 
SQList = [x for x in os.listdir(infolder) if "_Seq" in x]

'''
Nexus files for running Mr. Bayes are generated in this loop. 
'''

for sequenceFile in SQList: #Loop through the sequence file list
    STnum = sequenceFile.split("_")[2] #Extract the species tree number from the file name 
    sequencePath = os.path.join(infolder, sequenceFile)
    with open(sequencePath, 'r') as infile: #Open the sequence file for reading
        blackhole=[infile.readline() for x in xrange(17)] #Read the first 18 lines of the equence file, we don't need these 
        #Check if we read too many lines into the blackhole 
        for headerline in blackhole:
            if "Begin DATA;" in headerline:
                print "I discarded too many lines from the header of your \
                sequence file. Please open me and fix the xrange(#) in line 28."
                exit(1)
            else: # loop through the remaining lins in the sequence file and build the nexus files 
                line = True
                while line:
                    line = infile.readline()
                    if "Begin DATA" in line: #check to see if the line is the beginning of a new sequence block 
                        TreeNameSplit = line.split(";")[1].strip()
                        treeName = ''.join(TreeNameSplit[1:len(TreeNameSplit)-1].split(' ')) #get the tree number from the Begin Data line
                        outFileName = os.path.join(outfolder, treeName + "_" + STnum + ".nex") # concatonate the output directory name with the output file name 
                        Nexuslist=[line] #Lines to be written in the Nexus file will be stored here
                        while True: #append lines to the nexus file list until you reach the end of the sequence block
                            line = infile.readline()
                            Nexuslist.extend(line)
                            if line.strip().strip('\n') == "END;":
                                CreateNexus(Nexuslist, outFileName)
                                print "Sucessfully wrote nexus file for block %s from file %s." %(treeName, sequenceFile)  
                                break
                            else:
                                continue

 
NEXUSList = [x for x in os.listdir(outfolder) if ".nex" in x] #create a list of the nexus files written to the output directory

for NexusFile in NEXUSList:
    NexusPath = os.path.join(outfolder, NexusFile)
    os.system("mb %s" %NexusPath) #run mr bays   
    print "Mr. BayEs ran sucessfully from file %s" %NexusFile       
    

