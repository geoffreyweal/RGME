"""
supplementary_methods.py, Geoffrey Weal, 4/8/23

This script contains all the methods needed for the get_matrix_elements.py program to run.
"""

# ===============================================================================================================================================

# The types of variables that could be recorded and their datatypes.
datatypes = {} 
datatypes['Label']   = 'string'
datatypes['IVers']   = 'integer'
datatypes['NLab']    = 'integer'
datatypes['Version'] = 'string'
datatypes['Title']   = 'string'
datatypes['NAtoms']  = 'integer'
datatypes['NBasis']  = 'integer'
datatypes['NBsUse']  = 'integer'
datatypes['ICharg']  = 'integer'
datatypes['Multip']  = 'integer'
datatypes['NE']      = 'integer'
datatypes['Len12L']  = 'integer'
datatypes['Len4L']   = 'integer'
datatypes['IOpCl']   = 'integer'
datatypes['ICGU']    = 'integer'
datatypes['IAn']     = 'integer list'
datatypes['IAtTyp']  = 'integer list'
datatypes['AtmChg']  = 'float list'
datatypes['C']       = 'float list'
datatypes['IBfAtm']  = 'integer list'
datatypes['IBfTyp']  = 'integer list'
datatypes['AtmWgt']  = 'float list'
datatypes['NFC']     = 'integer'
datatypes['NFV']     = 'integer'
datatypes['ITran']   = 'integer'
datatypes['IDum9']   = 'integer'
datatypes['NShlAO']  = 'integer'
datatypes['NPrmAO']  = 'integer'
datatypes['NShlDB']  = 'integer'
datatypes['NPrmDB']  = 'integer'
datatypes['NBTot']   = 'integer'
datatypes['IOpCl']   = 'integer'
datatypes['IArr']    = 'integer list'
datatypes['RArr']    = 'float list'
datatypes['NI']      = 'integer'
datatypes['NR']      = 'integer'
datatypes['NRI']     = 'integer'
datatypes['NTot']    = 'integer'
datatypes['LenBuf']  = 'integer'
datatypes['N']       = 'integer list'
datatypes['ASym']    = 'string'

def get_infotypes():
	"""
	This method will return all the information types that can be obtained in the matrix_element_output.txt file
	"""
	return datatypes.keys()

def get_datatype(variable):
	"""
	This method will return the data type for the input variable

	Parameters
	----------
	variable: str.
		This is the variable you want to obtain
	datatypes : str.
		This is the datatype for this variable
	"""
	if variable is None:
		raise Exception('Error: No Datatype given. This may be caused by readmat8 not running correcting.\nCheck your input file and newly created MatrixElementsFiles/matrix_element_output.txt file to see if they are empty or not, or if they specify errors in the file. Report any issues to Github Issues.\nThis program will finish unsucessfully.')
	return datatypes[variable]

labelnames = {}
labelnames['DIPOLE_INTEGRALS'] = ['X', 'Y', 'Z']
labelnames['QUADRUPOLE_INTEGRALS'] = ['XX', 'YY', 'ZZ', 'XY', 'XZ', 'YZ']

entrylengths = {}
entrylengths['IAn']    = 4
entrylengths['IAtTyp'] = 12
entrylengths['AtmChg'] = 12
entrylengths['C']      = 12
entrylengths['IBfAtm'] = 8
entrylengths['IBfTyp'] = 8
entrylengths['AtmWgt'] = 12
entrylengths['IArr'] = 12
entrylengths['RArr'] = 12

# ===============================================================================================================================================

def get_filename(dataname):
	"""
	This method will update the label name that will be saved as a filename.
	"""
	return dataname.replace(' ','_').replace('/','_').replace('(','_').replace(')','_')

def split_string_into_substrings(input_string, substring_length=1):
	"""
	This method will take the input string and convert it into substrings of size given by substring_length.

	Parameters
	----------
	input_string : str.
		This is the input string you want to split into substrings.
	substring_length : int
		This is the length of the substrings to divide input_string into. 

	Returns
		list of substrings of size up to substring_length
	"""

	return input_string

	# First, initialise a list to record data into, and a working_string.
	data = []
	working_string = ''

	# Second, analyse each character in the string and process it.
	counter = 0
	for character in input_string:

		# 2.1: Save the current character to the working_string.
		working_string += character

		# 2.2: Increase the count only if the initial character is a negative number.
		if (counter == 0) and (character == '-'):
			pass
			#elif (character == '.'):
			#	pass
		else:
			counter += 1

		# 2.3: If the counter has reached substring_length, add the working_string to data 
		#      and prepare working_string for the next string. 
		if counter == substring_length:
			data.append(working_string)
			working_string = ''
			counter = 0
		elif counter > substring_length:
			raise Exception('Error, counter > substring_length. counter = '+str(counter)+'; substring_length = '+str(substring_length)+'; working_string = '+str(working_string)+'.')

	# Third, check to make sure that working_string is empty. 
	# If not, some of the data wasn't properly moved into data. 
	if not (working_string == ''):
		raise Exception('Error, working_string still contains data. working_string = '+str(working_string)+'; data = '+str(data))

	# Fourth, return data
	return data

def save_data(variable, datatype, line_number, label):
	"""
	This method will convert the input variable into the correct data type.

	Parameters
	----------
	variable : Any
		This is the variable you want to convert.
	datatype : str.
		This is the datatype you want to convert variable into.
	line_number : int.
		This is the line number of the line in matrix_element_output.txt.
	label : str.
		This is the name of the matrix being extracted.
	"""
	if   datatype == 'integer':
		return int(variable)
	elif datatype == 'float':
		return float(variable)
	elif datatype == 'string':
		return str(variable)
	elif datatype == 'integer list':
		return [int(variable)]
	elif datatype == 'float list':
		#variables = split_string_into_substrings(variable, substring_length=8)
		#return [float(variable) for variable in variables]
		return [float(variable)]
	raise Exception(f'Error at line {line_number} of matrix_element_output.txt (Matrix name: {label}): The following variable could not be converted to the datatype you desired: {variable}, {datatype}')

def append_data(variable, datatype, line_number, label):
	"""
	This method will convert the input variable into the correct data type. This data will be appended to the currently collected data.

	Parameters
	----------
	variable : Any
		This is the variable you want to convert.
	datatype : str.
		This is the datatype you want to convert variable into.
	line_number : int.
		This is the line number of the line in matrix_element_output.txt.
	label : str.
		This is the name of the matrix being extracted.
	"""
	if   datatype == 'string':
		return ' '+str(variable)
	elif datatype == 'integer list':
		try:
			return [int(variable)]
		except Exception as exception:
			print(f'* Warning at line {line_number} of matrix_element_output.txt (Matrix name: {label}): Integer was not given. variable: {variable}')
			return [str(variable)]
	elif datatype == 'float list':
		#variables = split_string_into_substrings(variable, substring_length=8)
		#return [float(variable) for variable in variables]
		return [float(variable)]
	raise Exception(f'Error at line {line_number} of matrix_element_output.txt (Matrix name: {label}): The following variable could not be converted to the datatype you desired: {variable}, {datatype}')

# ===============================================================================================================================================

def make_new_matrix(matrix_row_size, matrix_col_size):
	"""
	This method is designed to initialise the matrix to enter data into.

	Parameters
	----------
	matrix_row_size : int
		This is the number of rows in the matrix.
	matrix_col_size : int
		This is the number of columns in the matrix.

	Returns
	-------
	A 1D or 2D list that contains None in them. These enteries are to be replaced by values from the Gaussian file. 
	"""
	if matrix_col_size == 1:
		return [None for _ in range(matrix_row_size)]
	return [[None for _ in range(matrix_row_size)] for _ in range(matrix_col_size)]

def check_matrix(matrix, matrix_col_size):
	"""
	This method will check if any of the inputs in matrix has not been entered

	Parameters
	----------
	matrix : list of Any, or list of list of Any
		This is the matrix you want to check. 

	Returns
	-------
	A list of all the matrices given in this dataset. 
	"""
	if matrix_col_size == 1:
		# If the matrix_col_size is 1, this is a 1D matrix
		for value in matrix:
			if value is None:
				raise Exception('huh?')
	else:
		# If the matrix_col_size is greater than 1, this is a 2D matrix
		for a_list in matrix:
			for value in a_list:
				if value is None:
					raise Exception('huh?')

# ===============================================================================================================================================


