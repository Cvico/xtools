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
from rootfileReader.rootfileReader import SearchFiles, GetAllTrees

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

dataset = ReadLines(path) if datasetName != '' else datasetName

dic = GetEntriesDAS(dataset, verbose, doPretend)
# {dataset : [nfiles, nev]} or [nfiles, nev]
datasets = dic.keys()


dicfiles = SearchFiles(path, prodname)
# {samplename : path}

samples = dicfiles.keys()

for s in samples:
  entries, count, sow = GetCount(GetAllTrees(dicfiles[s]))
  for d in datasets:
    if not s in d: continue
    nfiles, nev = dic[d]
    fr = float(count)/nev*100
    print '%s : %1.2f %s'%(FixStringLength(s), fr, '%')
