# Download the repo
Whereven on the T2 where you have the output from crab.

    git clone https://github.com/Oviedo-PAF/nanoAOD-tools.git
   
# Merge crab output

    cd xtools/rootfileReader/

Merge a single dataset into chunks of 2 Gb:

    python haddtrees.py ../../CRABOUTPUT/SAMPLE/DATASET/ --outname NAME --maxSize 2000
    
Merge all the samples in a given production

    paython haddtrees.py ../../CRABOUTPUT/ --prod myProd_DDMMYY --maxSize 1000
