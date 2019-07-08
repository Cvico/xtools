import os, sys
import argparse
from ROOT import TFile, TTree

parser = argparse.ArgumentParser(description='Check trees')
parser.add_argument('--verbose'    , action='store_true'  , help = 'Activate the verbosing')
parser.add_argument('--startswith'  , default = '',          help = 'Starting name of files')
parser.add_argument('--endswith'   , default = '.root',          help = 'Ending name of files, ".root" by default')
parser.add_argument('--treename'   , default = 'Events',    help = 'Name of the tree, "Events" by default')
parser.add_argument('path'         , default = './' , help = 'Name of the file or of the directory')

args = parser.parse_args()

verbose = args.verbose
startswith = args.startswith
endswith = args.endswith
treename = args.treename
path     = args.path

def CheckNevents(filename, treename = 'Events', verbose = 0):
  if not os.path.isfile(filename):
    print 'ERROR: file "%s" does not exist!!' %filename
  f = TFile.Open(filename)
  if not hasattr(f, treename):
    print 'ERROR: file "%s" has not a tree named "%s"'%(filename, treename)
  else:
    nEvents = getattr(f,treename).GetEntries()
    if verbose: print '%s: %i'%(filename, nEvents)
  f.Close()

def CheckNeventsInDir(dirname, treename = 'Events', startswith = '', endswith = '.root', verbose = 0):
  if not os.path.isdir(dirname):
    if dirname.startswith(startswith) and dirname.endswith(endswith):
      CheckNevents(dirname, treename, startswith, endswith, verbose)
    else:
      print 'ERROR: file "%s" is not a file nor a directory...'%dirname
  else:
    dirname += '/' if not dirname.endswith('/') else ''
    for f in os.listdir(dirname):
      if not f.endswith(endswith): continue
      if not f.startswith(startswith): continue
      CheckNevents(dirname + f, treename, verbose)

CheckNeventsInDir(path , treename, startswith, endswith, verbose)
