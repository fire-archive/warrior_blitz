#!/usr/bin/env python

import os

from util import *

out_file_path = os.path.abspath(os.path.dirname(__file__))
out_file_path = os.path.join(out_file_path,'scraps_py.py')

out_file = None

if __name__.lower() == '__main__':
    out_file = open(out_file_path,'w')
    
    out_file.write('\n')
    
    out_file.close()
    

