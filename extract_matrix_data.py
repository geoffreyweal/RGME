"""
extract_matrix_data.py, Geoffrey Weal, 5/8/23

This script contains methods for extracting the matrix data from the output from readmat8 that can be saved into csv files.
"""

from save_matrix_data      import save_matrix_data
from supplementary_methods import save_data, append_data, get_infotypes, get_datatype, entrylengths

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

	labels = []; all_filepaths = []; data = {}
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
					label, filepaths = save_matrix_data(data, matrix_elements_foldername)
					if label is not None:
						labels.append(label)
					if filepaths is not None:
						all_filepaths += filepaths
				data = {}

			# Third, obtain the data from the line and import it into the data dictionary. 
			is_matrix_data, infotype = determine_matrix_data(line)
			if is_matrix_data:
				extract_matrix_data(line, infotype, data)
			else:
				extract_non_matrix_data(split_line, data)

	# Fourth, save the final compoent in data if this has not already been saved. 
	if not (data == {}):
		label, filepaths = save_matrix_data(data, matrix_elements_foldername)
		if label is not None:
			labels.append(label)
		if filepaths is not None:
			all_filepaths += filepaths

	# Fifth, return all the labels
	return labels, all_filepaths

# ============================================================================================================

def extract_matrix_data(line, infotype_with_equals, data):
	"""
	This method is designed to gather matrix information from the Gaussian datafile.

	Parameters
	----------
	line : str.
		This is the line from the Gaussian datafile to process.
	infotype_with_equals : str.
		This is the information type that is being processed. This will end with a = sign
	data : dict.
		This dictionary stores all the data that has been extracted from the Gaussian datafile.
	"""

	# First, obtain the variable to save the data into the data dictionary. 
	infotype = infotype_with_equals.replace('=','')

	# Second, remove the infotype from the line. 
	new_line = line.rstrip().split(infotype_with_equals)[1]

	# Third, obtain the entry length as based on the datatype given by infotype
	entrylength = entrylengths[infotype]

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
		if infotype not in data:
			data[infotype]  = save_data(value, get_datatype(infotype))
		else:
			data[infotype] += append_data(value, get_datatype(infotype))

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

	# First, initialise working_infotype to None. The line will contain the information about what this is as we move through the split_line list.
	working_infotype = None
	found_label = False

	# Second, for each entry in split_line list.
	for values in split_line:

		# 2.1: If values == 'Label', indicate we are recording the Label for this matrix data.
		if   values == 'Label':
			found_label = True
			working_infotype = 'Label'
			continue
		else:
			initial_valuename = values.split('=')[0]
			if found_label and (initial_valuename in get_infotypes()):
				print(data['Label'])
				found_label = False

		# 2.2: If values == 'Title', indicate we are recording the Title for this matrix data.
		if values == 'Title':
			working_infotype = 'Title'

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
				if value0 in get_infotypes():

					# Record value0 as the working_infotype to save into data
					working_infotype = value0

				elif get_datatype(working_infotype) == 'string':

					# value0 is matrix information. Record it. 
					if working_infotype not in data:
						data[working_infotype]  = save_data(value, get_datatype(working_infotype))
					else:
						data[working_infotype] += append_data(value, get_datatype(working_infotype))

				else:

					# Problem has arisen. 
					raise Exception('huh? Report this in Github : '+str(value0))

			# 2.3: Record the other value in the values dictionary. 
			for value in values:
				if value == '':
					continue
				if working_infotype not in data:
					data[working_infotype]  = save_data(value, get_datatype(working_infotype))
				else:
					data[working_infotype] += append_data(value, get_datatype(working_infotype))

		else:

			# 2.4: Save the matrix data into the data dictionary. 
			if working_infotype not in data:
				data[working_infotype]  = save_data(values, get_datatype(working_infotype))
			else:
				data[working_infotype] += append_data(values, get_datatype(working_infotype))

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
