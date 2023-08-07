"""
extract_matrix_data.py, Geoffrey Weal, 5/8/23

This script contains methods for extracting the matrix data from the output from readmat8 that can be saved into csv files.
"""

from supplementary_methods import save_data, append_data, save_matrix_data, get_type, entrylengths

def extract_data(data_filename, matrix_elements_foldername):
	"""
	This method is designed to extract the matrix data from the output from readmat8 that can be saved into csv files.

	Parameters
	----------
	data_filename : str.
		This is the filename that contains the matrix data obtained from readmat8.
	matrix_elements_foldername : int
		This is the foldername to save the matrix csv data into, and where data_filename is stored.
	"""

	data = {}
	with open(matrix_elements_foldername+'/'+data_filename, "r") as outfile:
		for line in outfile:

			# First, split the line up into a list of strings
			split_line = line.rstrip().split()

			# Second, if the line begins with:
			#    * "File": Do not record this and move on, or
			#    * "Label": Found new matrix. Save this data and initialise new data dictionary. 
			if   split_line[0] == 'File':
				continue
			elif split_line[0] == 'Label':
				if not (data == {}):
					save_matrix_data(data, matrix_elements_foldername)
				data = {}

			# Third, obtain the data from the line and import it into the data dictionary. 
			is_matrix_data, character_datatype = determine_matrix_data(line)
			if is_matrix_data:
				extract_matrix_data(line, character_datatype, data)
			else:
				extract_non_matrix_data(split_line, data)

			#if 'Label' in data:
			#	if data['Label'] == 'REAL ZEFFECTIVE':
			#		import pdb; pdb.set_trace()

	# Fourth, save the final compoent in data if this has not already been saved. 
	if not (data == {}):
		save_matrix_data(data, matrix_elements_foldername)

# ============================================================================================================

def extract_matrix_data(line, character_datatype, data):
	"""
	This method is designed to gather matrix information from the Gaussian datafile.

	Parameters
	----------
	line : str.
		This is the line from the Gaussian datafile to process.
	character_datatype : str.
		This is the datatype that is being processed. 
	data : dict.
		This dictionary stores all the data that has been extracted from the Gaussian datafile.
	"""

	# First, obtain the variable to save the data into the data dictionary. 
	saving_variable = character_datatype.replace('=','')

	# Second, remove the saving_variable from the line. 
	new_line = line.rstrip().split(character_datatype)[1]

	# Third, obtain the entry length as based on the datatype given by saving_variable
	entrylength = entrylengths[saving_variable]

	# Fourth, obtain the total number of indices to scan over, as well as the modulus 
	total_index, mod_index = divmod(len(new_line), entrylength)

	# Fifth, check that the length of the line is divisable by the length of the expected entry for this datatype.
	if not (mod_index == 0):
		raise Exception('Error: len(new_line) = '+str(len(new_line))+'; entrylength = '+str(entrylength)+'\nnew_line='+str(new_line))

	# Sixth, obtain each of the entries from new_line and add them to the data dictionary. 
	for index in range(total_index):

		# 6.1: Obtain the indices of the parts of new_line to extract.  
		start_index = index*entrylength
		end_index   = index*entrylength + entrylength

		# 6.2: Obtain the entry from new_line between start_index and end_index
		value = new_line[start_index:end_index]

		# 6.3: Save the entry into the data dictionary. 
		if saving_variable not in data:
			data[saving_variable]  = save_data(value, datatypes[saving_variable])
		else:
			data[saving_variable] += append_data(value,  datatypes[saving_variable])

# ============================================================================================================

def extract_non_matrix_data(split_line, data):
	"""
	This method is designed to gather non-matrix information from the Gaussian datafile.

	Parameters
	----------
	split_line : list of str.
		This is a list of all the entries in the line. 
	data : dict.
		This dictionary stores all the data that has been extracted from the Gaussian datafile.
	"""

	# First, initialise the saving_variable to None. The line will contain the information about what this is as we move through the split_line list.
	saving_variable = None
	found_label = False

	# Second, for each entry in split_line list.
	for values in split_line:

		# 2.1: If values == 'Label', indicate we are recording the Label for this matrix data.
		if   values == 'Label':
			found_label = True
			saving_variable = 'Label'
			continue
		else:
			initial_valuename = values.split('=')[0]
			if found_label and (initial_valuename in datatypes.keys()):
				print(data['Label'])
				found_label = False

		# 2.2: If values == 'Title', indicate we are recording the Title for this matrix data.
		if values == 'Title':
			saving_variable = 'Title'

		elif '=' in values:
			# 2.3: If values contains a = is it. this probably means we are dealling with a datatype to record. 
			#        Information to record for this datatype may also be included (included after the = sign). 

			# 2.3.1: Save this as a label name
			if found_label and ('(' in values) or (')' in values):
				values = [values]
				
			else:

				# 2.3.1.2.1: obtain the value type 
				values = values.split('=')
				value0 = values.pop(0)

				# 2.3.1.2.2: Determine what to do with the first instance in values, being value0.
				if value0 in datatypes.keys():

					# Record value0 as the saving_variable to save into data
					saving_variable = value0

				elif get_type(saving_variable) == 'string':

					# value0 is matrix information. Record it. 
					if saving_variable not in data:
						data[saving_variable]  = save_data(value, get_type(saving_variable))
					else:
						data[saving_variable] += append_data(value, get_type(saving_variable))

				else:

					# Problem has arisen. 
					raise Exception('huh? Report this in Github : '+str(value0))

			# 2.3: Record the other value in the values dictionary. 
			for value in values:
				if value == '':
					continue
				if saving_variable not in data:
					data[saving_variable]  = save_data(value, get_type(saving_variable))
				else:
					data[saving_variable] += append_data(value, get_type(saving_variable))

		else:

			# 2.4: Save the matrix data into the data dictionary. 
			if saving_variable not in data:
				data[saving_variable]  = save_data(values, get_type(saving_variable))
			else:
				data[saving_variable] += append_data(values, get_type(saving_variable))

# ============================================================================================================

def determine_matrix_data(line):
	"""
	This method will determine if matrix data is being processed or not, and also what datatype is being processed

	Parameters
	----------
	line : str.
		This is the line in the Gaussian datafile that is under analysis.

	Returns
	-------
	is_matrix_data : bool.
		True is the line contains matrix data. False if the line does not contain matrix data.
	character_datatype : str.
		If the line contains matrix data, this indicates the datatype that will be extracted from line.
	"""

	for datatype_character in entrylengths.keys():

		# First, if 'C=' is in the line, but not 'NFC=', the datatype if cartesian, which is stored as a matrix.
		if datatype_character == 'C': 
			if ('C=' in line) and ('NFC=' not in line):
				return True, 'C='
			continue

		# Second, add an equals sign to the end of datatype_character
		datatype_character_equals = datatype_character+'='

		# Third, if datatype_character_equals is in line, return True as this is a matrix datatype.
		if datatype_character_equals in line:
			return True, datatype_character_equals

	# If at this point, we are not dealing with matrix based data.
	return False, None

# ============================================================================================================
