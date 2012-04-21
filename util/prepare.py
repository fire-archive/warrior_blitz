#!/usr/bin/env python

import os
import sys

from util import *

beQuiet = False

removePyc = False

filesToTouch = []
filesToRemove = []


commonFiles = {
    'Lib':[
        '__init__.py'
    ],
    'Data':{
        
    }
}

walkPaths = {
    'Lib':[
        LIB_PATH
    ],
    'Data':{
        
    }
}

if EDITOR_PATH_EXISTS():
    walkPaths['Lib'].append(EDITOR_LIB_PATH)


for lib_dir in walkPaths['Lib']:
    
    for dirpath,dirnames,filenames in os.walk(lib_dir):
        
        for name in dirnames:
            if name.startswith('.'):
                dirnames.remove(name)
                
                continue
                
            
        
        for name in commonFiles['Lib']:
            file_name = os.path.join(dirpath,name)
            
            if not os.path.exists(file_name):
                filesToTouch.append(file_name)
                
            
        
        for name in filenames:
            if name.endswith('.pyc') and removePyc:
                file_name = os.path.join(dirpath,name)
                
                filesToRemove.append(file_name)
                
            
        
    




if len(filesToTouch) > 0:
    filesToTouch = [str(name) for name in filesToTouch]
    
    filesToTouch = [os.path.relpath(name) for name in filesToTouch]
    
    filesToTouch = list(set(filesToTouch))
    
    filesToTouch.sort()
    
    if not beQuiet:
        for name in filesToTouch:
            if not os.path.exists(name):
                print 'Creating file at '+name
                
            else:
                print 'Touching file at '+name
                
            
        
    
    filesToTouch = [('"'+name+'"') for name in filesToTouch]
    
    touchCmd  = 'touch '
    touchCmd += ' '.join(filesToTouch)
    
    os.system(touchCmd)
    
else:
    if not beQuiet:
        print 'Not touching any files'
        
    

