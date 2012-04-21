#!/usr/bin/env python

import sys
import os
import shutil

from util import *

if DOCS_HTML_PATH_EXISTS():
    try:
        shutil.rmtree(DOCS_HTML_PATH)
    except OSError:
        print 'Warning: Could not delete old Doxygen HTML docs'
    

os.chdir(BASE_PATH)

doxygenCmd  = 'doxygen '
doxygenCmd += wrapInQuotes(DOXYFILE_PATH)

os.system(doxygenCmd)

