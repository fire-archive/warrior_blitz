import os

def indentFile(out_file,indent_depth):
    indent_depth = int(indent_depth)
    
    if indent_depth > 0:
        indent_str  = ' '*4
        indent_str *= indent_depth
        
        out_file.write(indent_str)
        
    

def writeLine(out_file,line_text,indent_depth=0):
    line_text = str(line_text)
    
    indentFile(out_file,indent_depth)
    
    out_file.write(line_text)
    out_file.write('\n')
    

def blankLine(out_file,indent_depth=0):
    writeLine(out_file,'',indent_depth)
    

def wrapInQuotes(string,strip_inside_quotes=True):
    strip_inside_quotes = bool(strip_inside_quotes)
    
    string = str(string)
    
    
    if strip_inside_quotes:
        string = string.replace('"','')
        string = string.replace("'","")
        
    
    return '"' + string + '"'
    

def copyFiles(from_path,to_path):
    if not (isinstance(from_path,list) or isinstance(from_path,tuple)):
        from_path = [from_path]
        
    
    from_path = [str(name) for name in from_path]
    from_path = [os.path.abspath(name) for name in from_path]
    
    from_path = list(set(from_path))
    from_path.sort()
    
    if not isinstance(to_path,str):
        raise TypeError('Given to_path is not a string (to_path given was '+str(to_path)+')')
        
    
    to_path = os.path.abspath(to_path)
    
    cp_cmd = 'cp -rf '
    
    cp_cmd += ' '.join([('"'+name+'"') for name in from_path])
    
    cp_cmd += ' "'+to_path+'"'
    
    result = os.system(cp_cmd)
    
    if result != 0:
        raise 'Error during call to copyFiles(). os.system(cp_cmd) returned error code '+str(result)
        
    


BASE_PATH       = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))

DATA_PATH       = os.path.join(BASE_PATH,'data')
DEVDATA_PATH    = os.path.join(BASE_PATH,'dev-data')
LIB_PATH        = os.path.join(BASE_PATH,'lib')
CONFIG_PATH     = os.path.join(BASE_PATH,'config')
DOCS_PATH       = os.path.join(BASE_PATH,'docs')

DOXYFILE_PATH   = os.path.join(DOCS_PATH,'Doxyfile')
DOCS_HTML_PATH  = os.path.join(DOCS_PATH,'html')

DOCS_HTML_PATH_EXISTS = lambda: os.path.exists(DOCS_HTML_PATH)

EDITOR_PATH         = os.path.join(BASE_PATH,'editor')
EDITOR_LIB_PATH     = os.path.join(EDITOR_PATH,'lib')
EDITOR_DATA_PATH    = os.path.join(EDITOR_PATH,'data')

EDITOR_PATH_EXISTS  = lambda: os.path.exists(EDITOR_PATH)


if __name__.lower() == '__main__':
    # Do tests here!
    pass
    

