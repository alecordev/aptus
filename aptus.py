"""
Features:

- Inserts a first line to an existent file
- Kill all processes with given name
- Merges all files from given directory
- Copy a file to all directories in a tree
- Removes a file from all directories in a tree
- Copies a file to all directories specified in a file
- Copies a tree structure to a given directory (does not include specified directories)
"""

import os
import sys
import shutil
import argparse

__version__ = '0.1'
__author__ = 'alecor'

class AlecorParser(argparse.ArgumentParser):
    """
    Handle special case and show help on invalid argument
    """
    def error(self, message):
        sys.stderr.write('\nERROR: {}\n\n'.format(message))
        self.print_help()
        sys.exit(2)

def insert_first_line(filename, string):
    """
    Given a file, it inserts a first line efficiently
    """
    try:
        import fileinput
        for line in fileinput.input([filename], inplace=True):
            if fileinput.isfirstline():
                    print string
            print line,
    except Exception as e:
        print('\nError adding specified string to file {}: {}.'.format(filename, e))

def merge_text_files(merged_filename, directory, *args, **kwargs):
    """
    Merges files from directory into merged_filename
    
    kwargs['first_line'] indicates string to find in first line to omit it
    """
    try:
        files_lst = os.listdir(directory)
        total = len(files_lst)
        print '\nFound {} files to be merged...'.format(total)
        with open(merged_filename, 'w') as f:
            for i, l in enumerate(files_lst):
                with open(os.path.join(directory, l)) as log:
                    for n, line in enumerate(log):
                        if n == 0:
                            if kwargs.get('first_line', False):
                                if line.find(kwargs['first_line']) == -1:
                                    continue
                        f.write(line)
                print '\nFile {} of {} was merged successfully.'.format(i + 1, total)
    except Exception as e:
        print '\nError merging logs {}'.format(e)

def kill_all(process):
    try:
        for i in os.popen('taskkill /im {} /f'.format(process)):
            print i,
    except Exception as e:
        print '\nError killing process {}: {}'.format(process, e)        

def copy_file_to_multiple_subfolders(src, dst, *args, **kwargs):
    """
    Copies the src file to multiple subfolders, given a directory
    as destination, the src file is copied to all subdirectories
    within that directory
    """
    print '\nSource: {}\nDestinations parent folder: {}'.format(src, dst)
    filename = os.path.basename(src)
    for folder in (d for d in os.listdir(dst) if os.path.isdir(d)):
        print '\nCopying {} to {}...'.format(filename, folder)
        try:
            shutil.copy(src, os.path.abspath(dst) + '\\' + folder)
        except Exception as e:
            print e

def remove_file_from_subfolders(filename, dst, *args, **kwargs):
    """
    Removes specified file from all subfolders of the specified destination
    """
    for folder in (d for d in os.listdir(dst) if os.path.isdir(d)):
        tgt = os.path.abspath(dst) + '\\' + folder + '\\' + filename
        if os.path.isfile(tgt):
            print '\nDeleting {} from {}...'.format(filename, folder)
            try:
                os.remove(tgt)
            except Exception as e:
                print 'Exception removing {} from {}: {}'.format(filename, folder, e)
            else:
                print '{} removed successfully from {}.'.format(filename, folder)
        else:
            print '\n{} not found in {}'.format(filename, dst)

def copy_file_to_multiple_locations_from_file(file_to_copy, locations_file):
    """
    Copy file to multiple locations specified in a text file. One location per line.
    """
    try:
        with open(locations_file) as f:
            locations = (line for line in f)
            for i, location in enumerate(locations):
                try:
                    shutil.copy(file_to_copy, location)
                    print '\n{}. {} copied to {}. {} bytes transferred.'.format(i + 1, file_to_copy, location, os.path.getsize(location + '\\' + os.path.basename(file_to_copy)))
                except Exception as e:
                    print '\nError while trying to copy {} to {}: {}'.format(file_to_copy, location, e)
    except Exception as e:
        print 'Error found: {}'.format(e)

def remove_file_to_multiple_locations_from_file(file_to_remove, locations_file):
    """
    Copy file to multiple locations specified in a text file. One location per line.
    """
    try:
        with open(locations_file) as f:
            locations = (line for line in f)
            for i, location in enumerate(locations):
                try:
                    os.remove(os.path.join(location, file_to_remove))
                    print '\n{}. {} removed from {}.'.format(i + 1, file_to_remove, location)
                except Exception as e:
                    print '\nError while trying to remove {} from {}: {}'.format(file_to_remove, location, e)
    except Exception as e:
        print 'Error found: {}'.format(e)

def copy_tree(source_directory, target_directory):
    """
    Copies all files and folders under source to target directory.
    
    Copies, duplicates the tree structure of the source folder.
    """
    try:
        shutil.copytree(source_directory, target_directory)
    except Exception as e:
        print('Error found: {}'.format(e))

if __name__ == '__main__':

    parser = AlecorParser()
    parser.add_argument('-cm', nargs=2, metavar=('FILENAME', 'LOCATIONS_FILE'), help='copy specified file to all locations specified in a text file (one path per line expected)')
    parser.add_argument('-rm', nargs=2, metavar=('FILENAME', 'LOCATIONS_FILE'), help='remove specified file from all locations specified in a text file (one path per line expected)')
    parser.add_argument('-rs', nargs=2, metavar=('FILENAME', 'FOLDERPATH'), help='remove specified file from all subfolders of given folder (delete file from tree)')
    parser.add_argument('-cs', nargs=2, metavar=('FILENAME', 'FOLDERPATH'), help='copy specified file to all subfolders of given folder (copy file to tree)')
    parser.add_argument('-m', nargs=2, metavar=('FILENAME', 'FOLDERPATH'), help='merge all files from the specified folder to a filename')
    parser.add_argument('-f', nargs=1, metavar=('TEXT'), help='specify which text identifies content of a first line that want to be avoided on merging process')
    parser.add_argument('-i', nargs=2, metavar=('FILENAME', 'TEXT'), help='specify text to insert on first line of specified filename')
    parser.add_argument('-k', nargs=1, metavar=('FILE.EXT'), help='specify process filename to terminate (all instances of the process will be terminated)')
    parser.add_argument('-ct', nargs=2, metavar=('SOURCE_DIRECTORY', 'TARGET_DIRECTORY'), help='copy all file tree from the source under the target directory')
    args = parser.parse_args()
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)
    
    if args.cm:
        copy_file_to_multiple_locations_from_file(*args.cm)
        
    if args.rs:
        remove_file_from_subfolders(*args.rs)
        
    if args.cs:
        copy_file_to_multiple_subfolders(*args.cs)

    if args.ct:
        copy_tree(*args.ct)
        
    if args.rm:
        remove_file_to_multiple_locations_from_file(*args.rm)

    if args.m:
        if args.f:
            merge_text_files(*args.m, first_line=args.f)
        else:
            merge_text_files(*args.m, first_line=args.f)
            
    if args.i:
        insert_first_line(*args.i)
        
    if args.k:
        kill_all(args.k)