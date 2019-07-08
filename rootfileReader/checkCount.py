'''
 [checkCount.py] by Xuan (jrgonzal@cern.ch) 
 Description: Execute this program to check the number of initial events of your production
 You need to have 'rootfilesReader.py' 
 Usage:
   python checkCount.py input_directory/ 
'''

import os, sys
import argparse
from rootfilesReader import *

def haddForAllProd(dirname, prodname, pretend = False, outdir = './', maxSize = 5000, verbose = 1):
  dirnames, samplenames = haddProduction(dirname, prodname, verbose)
  if not pretend:
    if verbose >= 1: print pcol.red + ' STARTING...' + pcol.end
  else:
    if verbose >= 1: print pcol.red + ' PRETENDING...' + pcol.end
  for i in range(len(dirnames)): haddtrees(dirnames[i], samplenames[i], outdir, maxSize, pretend, verbose)

def  haddSampleInProd(dirname, prodname, sample, pretend = False, outdir = './', maxSize = 5000, verbose = 1):
  if verbose >= 1: print '>> Looking for sample: ', sample
  for i in range(len(dirnames)): 
    if sample == samplenames[i]: haddtrees(dirnames[i], samplenames[i], outdir, maxSize, pretend, verbose)

parser = argparse.ArgumentParser(description='Check trees')
parser.add_argument('--verbose', '-v'    , action='store_true'  , help = 'Activate the verbosing')
parser.add_argument('--pretend', '-p'   , action='store_true',    help = 'Pretend')
parser.add_argument('--prodName', '-t'  , default = '',          help = 'Tag of the production')
parser.add_argument('--outname', '-o'    , default = '',          help = 'Output name')
parser.add_argument('--outdir', '-d'    , default = './',          help = 'Output directory')
parser.add_argument('--sample', '-s'   , default = '',    help = 'Execute only for sample "sample" in production')
parser.add_argument('path'         , default = './' , help = 'Name of the directory')

args = parser.parse_args()

verbose    = args.verbose
pretend    = args.pretend
dirname    = args.path
prodname   = args.prodName
outdir     = args.outdir
maxSize    = args.maxSize
outname    = args.outname
sample     = args.sample


  dirnames, samplenames = haddProduction(dirname, prodname, verbose)

if prodname == '': haddtrees(dirname, outname, outdir, maxsize = maxSize, pretend = pretend, verbose = verbose)
else: 
  if sample == '': haddForAllProd(dirname, prodname, pretend, outdir, maxSize, verbose)
  else:            haddSampleInProd(dirname, prodname, sample, pretend, outdir,maxSize, verbose)
   
