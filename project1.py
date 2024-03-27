# project1.py

from pathlib import Path
from typing import List
import shutil

def make_path (string: str) -> Path:
    'Takes a string as an argument and returns it as a path.' 
    string = string [2:]
    return Path (string)

def print_files (a_list: List [Path]) -> None:
    'Prints the elements of a list.' 
    for element in a_list:
        print (element) 

def iterate_files (a_list: List [Path]) -> List [Path]:
    'Returns a list of all the files in a path found recursively.'  
    b_list = []
    for element in a_list:
        if element.is_file ():
            b_list.append (element)
        elif element.is_dir ():
            try: 
                b_list.extend (iterate_files (list(element.iterdir ())))
            except OSError:
                continue
    b_list.sort ()
    return b_list
    
def return_all (b_list: List [Path]) -> List [Path]:
    'Returns the list it takes as a parameter.' 
    return b_list

def name_search (search: str, b_list: List [Path]) -> List [Path]:
    'Returns a list of paths whose file names match or contain the string input.'
    c_list = []
    for element in b_list: 
        if search [2:] in str (element):
            c_list.append (element) 
    return c_list
        
def text_search (search: str, b_list: List [Path]):
    'Returns a list of paths whose files contain the string input in its contents.'
    c_list = []
    for element in b_list:
        the_file = open (element)
        try:
            for line in the_file.readlines ():
                line = line.rstrip ()
                if line == search [2:]:
                    c_list.append (element)
                    the_file.close ()
        except ValueError: 
            continue
    return c_list
    
def extension_search (search: str, b_list: List [Path]) -> List [Path]:
    'Returns a list of paths whose extensions match the string input.'
    c_list = []
    for element in b_list: 
        if element.suffix == search [1:] or element.suffix [1:] == search [2:]:
            c_list.append (element)
    return c_list
        
def less_than_search (search: str, b_list: List [Path]) -> List [Path]:
    'Returns a list of paths whose files are less than the integer input representing byte size.'
    c_list = []
    for element in b_list: 
        if element.stat().st_size < int (search [2:]):
            c_list.append (element) 
    return c_list
        
def greater_than_search (search: str, b_list: List [Path]) -> List [Path]:
    'Returns a list of paths whose files are greater than the integer input representing byte size.'
    c_list = []
    for element in b_list: 
        if element.stat ().st_size > int (search [2:]):
            c_list.append (element) 
    return c_list

def read_first_line (c_list: List [Path]) -> List [str]:
    'Returns the first line of each text file in the list. Returns NOT TEXT if the file is not a text file.'
    d_list = []
    for element in c_list:
        the_file = open (element)
        try: 
            text = the_file.readline ().strip()
        except ValueError: 
            text = 'NOT TEXT'
        d_list.append (text) 
        the_file.close ()
    return d_list
    
def duplicate_files (c_list: List [Path]) -> List [Path]:
    'Returns a duplicate files of all the files in the list, with the extension .dup'
    d_list = []
    for element in c_list:
        new_file = shutil.copy2 (element.name, element.name + '.dup')
        d_list.append (Path (new_file)) 
    return d_list
        
def touch_files (c_list = [Path]) -> List [None]:
    'Modifies the last modified timestamp of each file in the list to be the current date/time.'
    d_list = []
    for element in c_list:
        element.touch ()
    return d_list

def main (): 
    while True: 
        path: str = input ()
        if path [0:2] == 'D ' or path [0:2] == 'R ':
            one_path = make_path (path)
            contents = []
            
            for element in list (one_path.iterdir ()) :
                if element.is_file ():
                    contents.append (element)
            contents.sort () 

            if path [0:2] == 'R ':
                for element in list (one_path.iterdir ()):
                    if element.is_dir ():
                        try: 
                            subcontents = iterate_files (list (element.iterdir ()))
                            contents.extend (subcontents)
                        except OSError:
                            continue
      
            print_files (contents) 

            while True:  
                search: str = input ()
                if search [0:1] == 'A':
                    contents = return_all (contents)
                    break
                elif search [0:1] == 'N' and search [1:] != '':
                    contents = name_search (search, contents)
                    break
                elif search [0:1] == 'T':
                    contents = text_search (search, contents)
                    break
                elif search [0:1] == 'E':
                    contents = extension_search (search, contents)
                    break
                elif search [0:1] == '<':
                    contents = less_than_search (search, contents)
                    break
                elif search [0:1] == '>':
                    contents = greater_than_search (search, contents)
                    break
                else: 
                    print ('ERROR')
                
            print_files (contents)

            while True:
                action: str = input ()
                if action == 'F':
                    contents = read_first_line (contents)
                    break
                elif action == 'D':
                    contents = duplicate_files (contents)
                    break
                elif action == 'T':
                    contents = touch_files (contents)
                    break
                else:
                    print ('ERROR')

            print_files (contents)
            break

        else:
            print ('ERROR') 

if __name__ == '__main__':
    main () 
