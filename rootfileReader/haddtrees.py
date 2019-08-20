'''
 [haddtrees.py] by Xuan (jrgonzal@cern.ch) 
 Description: Execute this program to merge your nanoAOD production
 You need to have 'rootfilesReader.py' and 'haddnano.py'
 Usage:
   python haddtrees.py input_directory/ --prodName productionTag --maxSize 2000 # merge files in chunks of about 2 Gb (input size)
   python haddtrees.py nanoAODcrab/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/jun10MC/ -o TTTo2L2Nu -d out/'
   python haddtrees.py nanoAODcrab/TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/jun12_TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/ -o test.root'
   python haddtrees.py nanoAODcrab -t jun10 -s 2000'
'''

import os, sys
import argparse
from rootfileReader import *

def rmProd(dirname, prodname):
  dirnames, samplenames = haddProduction(dirname, prodname, verbose = 1)

def haddForAllProd(dirname, prodname, pretend = False, outdir = './', maxSize = 5000, verbose = 1):
  dirnames, samplenames = haddProduction(dirname, prodname, verbose)
  if not pretend:
    if verbose >= 1: print pcol.red + ' STARTING...' + pcol.end
  else:
    if verbose >= 1: print pcol.red + ' PRETENDING...' + pcol.end
  for i in range(len(dirnames)): haddtrees(dirnames[i], samplenames[i], outdir, maxSize, pretend, verbose)

def  haddSampleInProd(dirname, prodname, sample, pretend = False, outdir = './', maxSize = 5000, verbose = 1):
  dirnames, samplenames = haddProduction(dirname, prodname, verbose)
  if verbose >= 1: print '>> Looking for sample: ', sample
  for i in range(len(dirnames)): 
    if sample == samplenames[i]: haddtrees(dirnames[i], samplenames[i], outdir, maxSize, pretend, verbose)

parser = argparse.ArgumentParser(description='Check trees')
parser.add_argument('--verbose', '-v'    , action='store_true'  , help = 'Activate the verbosing')
parser.add_argument('--pretend', '-p'   , action='store_true',    help = 'Pretend')
parser.add_argument('--prodName', '-t'  , default = '',          help = 'Tag of the production')
parser.add_argument('--outname', '-o'    , default = '',          help = 'Output name')
parser.add_argument('--outdir', '-d'    , default = './',          help = 'Output directory')
parser.add_argument('--maxSize', '-s'   , default = 2000,    help = 'Maximum input size of the chunks to merge')
parser.add_argument('--sample', '-a'   , default = '',    help = 'Execute only for sample "sample" in production')
parser.add_argument('path'         , default = './' , help = 'Name of the directory')

args = parser.parse_args()

verbose    = args.verbose
pretend    = args.pretend
dirname    = args.path
prodname   = args.prodName
outdir     = args.outdir
maxSize    = float(args.maxSize)
outname    = args.outname
sample     = args.sample

if prodname == '': haddtrees(dirname, outname, outdir, maxsize = maxSize, pretend = pretend, verbose = verbose)
else: 
  if sample == '': haddForAllProd(dirname, prodname, pretend, outdir, maxSize, verbose)
  else:            haddSampleInProd(dirname, prodname, sample, pretend, outdir, maxSize, verbose)
   
