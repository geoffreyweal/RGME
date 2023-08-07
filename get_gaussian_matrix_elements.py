#!/usr/bin/env python3

"""
get_matrix_elements.py, Geoffrey Weal, 4/8/23

This program is designed to convert the data from "output=(MatrixElement)" gjf input from Gaussian into csv files.
"""

# First, import required modules.
import os, sys
from shutil import rmtree
from subprocess import run
from extract_matrix_data import extract_data

# Second, establish file and program paths. 
filepath = sys.argv[1]
program_path = os.path.dirname(__file__)

# Third, create the folder to save csv and other files to created during the running of this program.
matrix_elements_foldername = 'MatrixElementsFiles'
if os.path.exists(matrix_elements_foldername):
	rmtree(matrix_elements_foldername)
os.makedirs(matrix_elements_foldername)

# Fourth, make sure that you have the gauopen_v2 program. 
gauopen_v2_filepath = 'gauopen_v2'
readmat8_name = 'readmat8'
path_to_readmat8 = program_path+'/'+gauopen_v2_filepath+'/'+readmat8_name
if not os.path.exists(path_to_readmat8):
	raise Exception('Error, you need to run the "setup_GauOpen.sh" file before running this program.\nExpected program path: '+str(path_to_readmat8))

# Fifth, run the readmat8 program in gauopen_v2 to get the output from it. 
data_filename = 'matrix_element_output.txt'
print('Running readmat8 program on: '+str(filepath))
print('Saving raw data into '+str(matrix_elements_foldername+'/'+data_filename))
with open(matrix_elements_foldername+'/'+data_filename, "w") as outfile:
	result = run([path_to_readmat8, str(filepath)], stdout=outfile)
if not result.returncode == 0:
	print('ERROR: There was a problem when running the readmat8 program on '+str(filepath))
	print('Go to '+matrix_elements_foldername+'/'+data_filename+' To read what the error was.')
	exit('This program will finish UNSUCCESSFULLY.')
print('Finished running readmat8 program')

# Sixth, extract the data from matrix_element_output.txt and save the matrices as csv files.
print('Extracting data into CSV files')
extract_data(data_filename, matrix_elements_foldername)
print('\nFinished extracting data into CSV files')

