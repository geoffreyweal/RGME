#!/usr/bin/env python3

"""
get_matrix_elements.py, Geoffrey Weal, 4/8/23

This program is designed to convert the data from "output=(MatrixElement)" gjf input from Gaussian into csv files.
"""

# First, import required modules.
import os, sys
from shutil import rmtree
from subprocess import run
from extract_matrix_data   import extract_data
from supplementary_methods import get_filename

# Second, establish file and program paths. 
filepath = sys.argv[1]
program_path = os.path.dirname(__file__)

# Third, create the folder to save csv and other files to created during the running of this program.
matrix_elements_foldername = 'MatrixElementsFiles'
#''' # add back later
if os.path.exists(matrix_elements_foldername):
	rmtree(matrix_elements_foldername)
os.makedirs(matrix_elements_foldername)
#'''

# Fourth, make sure that you have the gauopen_v2 program. 
gauopen_v2_filepath = 'gauopen_v2'
readmat8_name = 'readmat8'
path_to_readmat8 = program_path+'/'+gauopen_v2_filepath+'/'+readmat8_name
#''' # add back later
if not os.path.exists(path_to_readmat8):
	toString = 'Error, you need to run the "setup_GauOpen.sh" file before running this program.\n\nSee the RGME Github page for more information on setting up the RGME program (https://github.com/geoffreyweal/RGME).\n\nExpected program path: '+str(path_to_readmat8)
	raise Exception(toString)
#'''
# Fifth, run the readmat8 program in gauopen_v2 to get the output from it. 
data_filename = 'matrix_element_output.txt'
#''' # add back later
print('Running readmat8 program on: '+str(filepath))
print('Saving raw data into '+str(matrix_elements_foldername+'/'+data_filename))
with open(matrix_elements_foldername+'/'+data_filename, "w") as outfile:
	result = run([path_to_readmat8, str(filepath)], stdout=outfile)
if not result.returncode == 0:
	print()
	print('================================================================================')
	print('ERROR: There was a problem when running the readmat8 program on '+str(filepath))
	print('Go to '+matrix_elements_foldername+'/'+data_filename+' to read what the error was.')
	print('Will print what matrics has been obtained and that are confidently completed')
	#exit('This program will finish UNSUCCESSFULLY.')
	print('================================================================================')
	print()
print('Finished running readmat8 program')
#'''

# Sixth, extract the data from matrix_element_output.txt and save the matrices as csv files.
print('Extracting data into CSV files')
labels, all_filepaths = extract_data(data_filename, matrix_elements_foldername)
print('\nFinished extracting data into CSV files')

# Seventh, if the last matrix name does not end with End, remove it because it may not be complete
if len(labels) > 0:
	last_label = labels[-1]
	if not last_label == 'END':
		filepath_to_remove = all_filepaths[-1]
		if os.path.exists(filepath_to_remove):
			print('WARNING!!!: '+str(filepath_to_remove)+' may not be complete. Specifically, the later matrix rows may be missing. Caution should be applied when read and using this matrix data.')
			#os.remove(filepath_to_remove)
		else:
			print('WARNING!!!: Could not find error file: '+str(filepath_to_remove))