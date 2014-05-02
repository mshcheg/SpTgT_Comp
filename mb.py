#!/bin/python 

import sys 
from os import listdir




#read in list of files here 

[prog name, infolder, outfolder]


myfolder = sys.argv[1] 
#name of folder 
outfolder = sys.argv[2]


MAKE A LIST OF _SEQ FILES 
SQList = [x for x in listdir(myfolder) if "_Seq" in x]

#loop through a folder of sequence block files 
for myfile in SQList:
    STnum = myfile.split("_")[2]
    with open(myfile, 'r') as infile:
        #read the header of the file 
        blackhole=[infile.next() for x in xrange(18)]
            
        #start looping on lines containing sequences
        for line in infile:
            test = line 
            if "Begin DATA" in test: 
                #create tmp
                treeName = test.split(";")[1].strip()[1:len(tmp)-1]
                outFileName = myfolder + treeName + "_" + STnum + ".nex"
                CREATE THE MR. BAYES FILE NAME FROM NEXUS NAME 
                "begin mrbayes;\nexecute temp.nex;\nset autoclose=yes nowarn=yes;\nprset brlenspr=clock:uniform;\nprset statefreqpr=dirichlet(1,1,1,1);\nlset  nst=2  rates=gamma Ngammacat=4;\nmcmc ngen=110000  Stoprule=yes Stopval=0.01 relburnin=yes burninfrac=0.25 samplefreq=100;\nsumt filename=%s AND STNUM Nruns=2 Contype=Allcompat;\nquit;\nend;" %THIS IS THE FILE NAME 
                with open(outFile, 'w') as outfile:
                    #write the matrix to the outfile                             
            if test == "END;":
                # stop witing to output file 
                print "we reached the end of block %s" %treeName 

#create list of nexus files 
for file in some list of nexus files: 
    #run mr bays   
    mb execute nameoffile       
    

