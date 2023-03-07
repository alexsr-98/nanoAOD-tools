import os, sys, ast

def GetEvDic(l):
  for d2 in l:
    for d in d2['dataset']:
      if 'nevents' in d.keys(): 
        return d
  return {}



args = sys.argv

if len(args[1:]) == 0: 
  print 'Usage: \n>> python CheckDatasets.py datasets/mc2018.txt'
  exit()
fname = args[1]

mode = ''
command = 'dasgoclient --query="dataset dataset=%s"'

if len(args[1:]) > 1:
  mode = args[2]
  if mode == 'file': command = 'dasgoclient --query="file dataset=%s"'
  else: command += ' -json'


datasets = []
if os.path.isfile(fname):
  f = open(fname)
  print 'Opening file: %s'%fname
  for l in f.readlines():
    if l.startswith('#'): continue
    if '#' in l: l = l.split('#')[0]
    l = l.replace(' ', '').replace('\n', '')
    if l == '': continue
    datasets.append(l)
else: datasets = [fname]

print 'Found %i datasets...'%len(datasets)
totalFiles = 0
totalEvents = 0
totalSize = 0
for d in datasets:
  #print 'Checking dataset %s...'%d
  match = os.popen(command%d).read()
  if mode == '':
    match = match.replace('\n', '')
    warn = '\033[0;32mOK       \033[0m' if match == d else '\033[0;31mNOT FOUND\033[0m'
    print '[%s] %s'%(warn, d)
  elif mode == 'file':
    if match.endswith('\n'): match=match[:-1]
    match = match.replace(' ', '').split('\n')
    for m in match: print m
  else:
    match = match.replace('\n', '').replace('null', '""')
    #l = ast.literal_eval(match)
    l = eval(match)
    dic = GetEvDic(l)
    if dic == {}: 
      print '\nWARNING: not found categories of dataset ', d
      exit()
    nevents = dic['nevents']
    nfiles  = dic['nfiles']
    size    = dic['size']/1e6
    print 'nevets = %i, nfiles = %i, size = %1.2f MB'%(nevents, nfiles, size)
    totalFiles+=nfiles; totalEvents+=nevents; totalSize+=size

if mode!='' and mode!='file': print '\nTOTAL: nevets = %i, nfiles = %i, size = %1.2f MB'%(totalEvents, totalFiles, totalSize)
