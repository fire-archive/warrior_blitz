#!/usr/bin/env python

import shutil
import os

from util import *

COPY_TYPES = [
    # File types to copy
    
    # Images
    '.png',
    
    # Sounds
    '.wav','.ogg',
    
    # XML Files
    '.xml'
    
]

# Whether to exclude Unix-style hidden files and folders.
# (That is, those with a name that begins with a dot)
EXCLUDE_UNIX_HIDDEN = True

def doCopy():
    os.chdir(DEVDATA_PATH)
    
    if os.path.exists(DATA_PATH):
        for name in os.listdir(DATA_PATH):
            name_path = os.path.join(DATA_PATH,name)
            
            if os.path.isdir(name_path):
                shutil.rmtree(name_path)
                
            else:
                os.remove(name_path)
                
            
        
    else:
        os.makedirs(DATA_PATH)
        
    
    for dirpath,dirnames,filenames in os.walk('.'):
        
        for name in dirnames:
            if EXCLUDE_UNIX_HIDDEN and name.startswith('.'):
                # We're excluding UNIX hidden folders and this
                # is one of them. We don't want to recurse into it.
                dirnames.remove(name)
                
            
            # Path within dev-data/
            devdata_dir_path = os.path.relpath(os.path.join(dirpath,name))
            # Join that to DATA_PATH to get the path within data/
            data_dir_path = os.path.join(DATA_PATH,devdata_dir_path)
            
            if not os.path.exists(data_dir_path):
                print 'Making folder at '+data_dir_path
                
                os.makedirs(data_dir_path)
                
            
        
        for name in filenames:
            if EXCLUDE_UNIX_HIDDEN and name.startswith('.'):
                # We're excluding UNIX hidden files and this
                # is one of them. We'll skip it.
                continue
                
            
            copy_type_matches = [name.endswith(ext) for ext in COPY_TYPES]
            
            if any(copy_type_matches):
                # Path within dev-data/
                devdata_file_path = os.path.relpath(os.path.join(dirpath,name))
                # Join that to DATA_PATH to get the path within data/
                data_file_path = os.path.join(DATA_PATH,devdata_file_path)
                
                print 'Copying file at '+devdata_file_path+' to '+data_file_path
                
                shutil.copy2(devdata_file_path,data_file_path)
                
            
        
    

if __name__.lower() == '__main__':
    doCopy()
    

