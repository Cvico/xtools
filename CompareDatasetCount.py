'''
 [CompareDatasetsCount.py] by Xuan (jrgonzal@cern.ch) 
 Description: Execute this program to compare the numbers in the 'Count' histogram
 contained in your nanoAOD, corresponding to the total number of events of the processed trees,
 with the number of events of the dataset in DAS
 You need to have 'rootfilesReader' and 'crabtools'
 Usage:
   python CompareDatasetCount.py dataset/data2017.txt --path nanoAODcrab/ --prodName prod
   python CompareDatasetCount.py dataset/data2017.txt --path nanoAOD/data2017/
   python CompareDatasetCount.py --dataset dataset --path nanoAOD/data2017/
'''

from crabTools.GetEventsDataset import GetEntriesDAS
from crabTools.SubmitDatasets import ReadLines
from rootfileReader.rootfileReader import SearchFiles, GetAllTrees, GetOnlyCount, FixStringLength, GetFiles

import argparse
parser = argparse.ArgumentParser(description='Check events with events in das')
parser.add_argument('--verbose','-v'    , action='store_true'  , help = 'Activate the verbosing')
parser.add_argument('--pretend','-p'    , action='store_true'  , help = 'Create the files but not send the jobs')
parser.add_argument('--test','-t'       , action='store_true'  , help = 'Sends only one or two jobs, as a test')
parser.add_argument('--dataset','-d'    , default=''           , help = 'Check this dataset')
parser.add_argument('--prodName','-n'   , default=''           , help = 'Name of your production')
parser.add_argument('--options','-o'    , default=''           , help = 'Options to pass to your producer')
parser.add_argument('--path'    , default='./' , help = 'path to files')
parser.add_argument('file'         , default=''           , nargs='?', help = 'txt file with datasets')

  
args = parser.parse_args()
  
verbose     = args.verbose
doPretend   = args.pretend
dotest      = args.test
datasetName = args.dataset
prodName    = args.prodName
options     = args.options
path        = args.path
fname       = args.file

doDataset   = False if datasetName == '' else True

dataset = ReadLines(fname) if datasetName == '' else datasetName

print 'Getting info from DAS...'
dic = GetEntriesDAS(dataset, verbose, doPretend)
# {dataset : [nfiles, nev]} or [nfiles, nev]
datasets = dic.keys()


print 'Searching files of prod ', prodName, ' in ', path
dicfiles = SearchFiles(path, prodName)
# {samplename : path}

samples = dicfiles.keys()
samples.sort()

for s in samples:
  if verbose: print 'Getting count for sample ', s
  trees = GetFiles(dicfiles[s], s) if prodName == "" else GetAllTrees(dicfiles[s])
  count = GetOnlyCount(trees)
  for d in datasets:
    dname = '%s'%d
    dname = dname.replace('/', '_')
    dname = dname.replace('-', '_')
    if not s in dname: continue
    nfiles, nev = dic[d]
    fr = float(count)/nev*100
    print '[%i] [%i] %s : %1.2f %s'%(nev, count, FixStringLength(s), fr, '%')
