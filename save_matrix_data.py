"""
supplementary_methods.py, Geoffrey Weal, 4/8/23

This script contains all the methods needed for the get_matrix_elements.py program to run.
"""

import csv
import numpy as np
from supplementary_methods import make_new_matrix, check_matrix, labelnames

def save_matrix_data(data, foldername):
	"""
	This method is designed to take the data from the data dictionary and convert it into a matrix form.

	Parameters
	----------
	data : dict.
		This dioctionary contains all the data needed for creating a matrix.
	"""

	# First, check if a Label has been given for this matrix data
	if 'Label' not in data.keys():
		raise Exception('Error. No Label found.')

	# Second, grad the label for this matrix data, and convert white spaces to underscores
	label = data['Label'].replace(' ','_').replace('/','_')

	# Third, determine if there is an array or intergers or floats that contains information for making a matrix with. 
	if 'IArr' in data.keys():
		array = data['IArr']
	elif 'RArr' in data.keys():
		array = data['RArr']

	# Fourth, obtain the information needed to convert IArr/RArr into a matrix/matrices. 
	if 'N' in data.keys():
		matrix_information = data['N']

	# Fifth, if you have the necessary information, create and save the matrix
	if (('IArr' in data.keys()) or ('RArr' in data.keys())) and ('N' in data.keys()):

		# 5.1: Make the matrices from your array and the matrix information. 
		matrices = convert_into_matrix(array, matrix_information, label)

		# 5.2: If matrices is a NoneType, ignore this data dictionary and move on, we dont want to record this matrix data.
		if matrices is None:
			return

		# 5.3: Save the data in an excel spreadsheet using pandas.
		if len(matrices) == 1:

			# 5.3.1: Save the matrix as a csv file.
			save_matrix_as_csv(matrices[0], label, foldername)

		else:

			# 5.3.2: Obtain the names to name each of the matrices
			if label in labelnames:
				if not (len(labelnames[label]) == len(matrices)):
					print('Error: Number of matrices for '+str(label)+' does not match expected from labelnames.\nNo of matrices: '+str(len(matrices))+'\nNumber of matrices expected (from labelnames): '+str(len(labelnames[label]))+'\nExpected matrices (from labelnames): '+str(labelnames[label]))
					import pdb; pdb.set_trace()
				matrice_subnames = [label+'_'+str(sublabel) for sublabel in labelnames[label]]
			else:
				matrice_subnames = [label+'_'+str(number) for number in range(1,len(matrices)+1)]

			# 5.3.3: Save the matrix as a csv file.
			for filename, matrix in zip(matrice_subnames, matrices):
				save_matrix_as_csv(matrix, filename, foldername)

# ===============================================================================================================================================

ignore_labels = ['GAUSSIAN_SCALARS']
def convert_into_matrix(array, matrix_information, label):
	"""
	This method is designed to convert your input array into the appropriate number of 1D or 2D matrices as given by matrix_information

	Parameters
	----------
	array : list of Any
		This is all the data you want to convert into a number of 1D or 2D matrices, as given by matrix_information. Array is given as a massive 1D list holding all the information. 
	matrix_information : list of ints
		This list contains all the information about the number of 1D or 2D matrices to create from array. 
	label : str.
		This is the name of the matrix data being obtained.

	Returns
	-------
	A list of all the matrices given in this dataset. 
	"""

	# Preamble, if label is to be ignored, return None
	if label in ignore_labels:
		return None

	# First, obtain the number of rows and columns in each matrix. 
	matrix_row_size = matrix_information[0]
	matrix_col_size = matrix_information[1]

	# Second, determine if the matrices are lower triangular matrices 
	# If matrix_row_size is negative, matrices are lower triangular. 
	is_lower_triangle = (matrix_row_size < 0)
	matrix_row_size = abs(matrix_row_size)

	# Third, collect all the matrices in array, based on the matrix format given by matrix_information
	matrices = []
	matrix = make_new_matrix(matrix_row_size, matrix_col_size)
	if matrix_col_size == 1:
		# ------------------------------------------------------
		# 3.1: IF THE matrix_col_size IS 1, YOU HAVE A 1D MATRIX
		# ------------------------------------------------------

		# 3.1.1: Add values to matrix until you have reached matrix_row_size.
		row_index = 0
		for value in array:
			matrix[row_index] = value
			row_index += 1

			# 3.2.1: If row_index == matrix_row_size, save the matrix and initialise the next matrix. 
			if row_index == matrix_row_size:
				check_matrix(matrix, matrix_col_size)
				matrices.append(np.array(matrix))
				matrix = make_new_matrix(matrix_row_size, matrix_col_size)
				row_index = 0

	else:
		# -------------------------------------------------------------------
		# 3.2: IF THE matrix_col_size IS greater than 1, YOU HAVE A 2D MATRIX
		# -------------------------------------------------------------------

		if is_lower_triangle:

			# 3.2.1: If your matrix is a lower triangular, do the following:
			row_index = 0; col_index = 0
			for value in array:
				try:
					matrix[col_index][row_index] = value
					matrix[row_index][col_index] = value
				except:
					raise Exception('Issue: matrix_information: '+str(matrix_information)+'; row_index: '+str(row_index)+'; col_index: '+str(col_index))
				row_index += 1
				if row_index == col_index+1:
					# 3.2.1.1: If row_index == col_index, move onto the next column index.
					row_index =  0; col_index += 1
					if col_index == matrix_col_size:
						# 3.2.1.2: If col_index == matrix_col_size, matrix has been filled.
						#          Move onto the matrix.
						check_matrix(matrix, matrix_col_size)
						matrices.append(np.array(matrix))
						matrix = make_new_matrix(matrix_row_size, matrix_col_size)
						row_index = 0; col_index = 0
					elif col_index > matrix_col_size:
						raise Exception('Issue: matrix_information: '+str(matrix_information)+'; row_index: '+str(row_index)+'; col_index: '+str(col_index))
				elif row_index > col_index:
					raise Exception('Issue: matrix_information: '+str(matrix_information)+'; row_index: '+str(row_index)+'; col_index: '+str(col_index))

		else:

			# 3.2.2: If your matrix is an ordinary triangular, do the following:
			row_index = 0; col_index = 0
			for value in array:
				try:
					matrix[col_index][row_index] = value
				except:
					raise Exception('Issue: matrix_information: '+str(matrix_information)+'; row_index: '+str(row_index)+'; col_index: '+str(col_index))
				row_index += 1
				if row_index == matrix_row_size:
					# 3.2.1.1: If row_index == matrix_row_size, move onto the next column index.
					row_index =  0; col_index += 1
					if col_index == matrix_col_size:
						# 3.2.1.2: If col_index == matrix_col_size, matrix has been filled.
						#          Move onto the matrix.
						check_matrix(matrix, matrix_col_size)
						matrices.append(np.array(matrix))
						matrix = make_new_matrix(matrix_row_size, matrix_col_size)
						row_index = 0; col_index = 0
					elif col_index > matrix_col_size:
						raise Exception('Issue: matrix_information: '+str(matrix_information)+'; row_index: '+str(row_index)+'; col_index: '+str(col_index))
				elif row_index > matrix_row_size:
					raise Exception('Issue: matrix_information: '+str(matrix_information)+'; row_index: '+str(row_index)+'; col_index: '+str(col_index))

	# Fourth, check if the number of matrices obtained is as expected from matrix_information
	no_of_matrices = matrix_information[2] * matrix_information[3] * matrix_information[4]
	if not (len(matrices) == no_of_matrices):
		print('Error: Number of matrices for '+str(label)+' does not match expected.\nNo of matrices: '+str(len(matrices))+'\nNumber of matrices expected: '+str(no_of_matrices)+'\nmatrix_information: '+str(matrix_information))
		import pdb; pdb.set_trace()

	# Fifth, return matrices.
	return matrices

# ===============================================================================================================================================

def save_matrix_as_csv(matrix, filename, dirpath):
	"""
	This method is designed to save the data from matrix into a csv file.

	Parameters
	----------
	matrix : list of Any, or list of list of Any
		This is the matrix you want to check. 
	filename : str.
		This is the name of the file (without .csv in the name).
	dirpath : str.
		This is the path that you want to save filename.csv in. 
	"""
	with open(dirpath+'/'+filename+'.csv', 'w', newline='') as csvfile:
		csv_writer = csv.writer(csvfile)
		if   matrix.ndim == 1:
			csv_writer.writerow(matrix)
		elif matrix.ndim == 2:
			for row in matrix:
				csv_writer.writerow(row)
		else:
			raise Exception('Error: Matrix is not 1D or 2D.\nMatrix dimensions: '+str(matrix.ndim))

# ===============================================================================================================================================

