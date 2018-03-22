#!/usr/bin/python

"""
Read in for AVL-FIRE *_fl2.gid file, that is stored in the 2D_Resuls folder of each calculation

[ date:     10. 11. 2016    ]
[ author:     L. Eder    ]

    [ output ]
        textfile = output.txt
    
        
"""


#--- LIBRARY IMPORT  ---------------------------------------------------------------------------------------
import string,sys
import time, os.path
from sys import argv

#--- CHECK FOR VALID INPUT ---------------------------------------------------------------------------------


# argument check - the user has to specify four input arguments (what to execute on which fl2 file with which input file and where to write it to)
check = len(argv)
if check != 4:
    print("Error: ")
    print("you have to enter a command line like:")
    print("./mext.py <filename.gid> <inputfile.txt> <outputfile.txt>")
    sys.exit()
fl2_name = argv[1]
in_name = argv[2]
out_name = argv[3]


# Check, if the specified fl2 file exits in the specified folder 
if not os.path.isfile(fl2_name):
    print "Did not find any fl2 file with name: {a}".format(a = fl2_name)
    print "Exiting Script"
    sys.exit()

# Check, if the specified fl2 file exits in the specified folder     
if not os.path.isfile(in_name):
    print "Did not find any input file with name: {a}".format(a = fl2_name)
    print "Exiting Script"
    sys.exit()    
    

# debug flag - switch to true, if you want an extended output
debug_flag = False



#--- MAIN PROGRAM ---------------------------------------------------------------------------------------
#print '*** FL2 Extract script started at: {a}'.format(a = os.getcwd())

#--- Search for significant lines ------------------------------------------------
# define checkstrings and create a header
checkstring_channel = "CHANNELNAME"
checkstring_unit = "UNIT"
checkstring_end = "END"

# set initial counters and list
line_counter = 0
checklist = []

# open fl2 file and find the row number of the three significant checkstrings
fl2_file = open(fl2_name, 'r')
for line in fl2_file:
    if checkstring_channel in line:
	    checklist.append(line_counter)
    if checkstring_unit in line:
	    checklist.append(line_counter)
    if checkstring_end in line:
	    checklist.append(line_counter)	
    line_counter += 1 
fl2_file.close()

if debug_flag:
	print "---debug--- Line number of CHANNELNAME: {a}".format(a = checklist[0])
	print "---debug--- Line number of UNIT:        {a}".format(a = checklist[1])
	print "---debug--- Line number of END:         {a}".format(a = checklist[2])
	

   
#--- Read the input file ---------------------------------------------------   
# open input file and create output_header list
# output header contains the srings of the variables, specified in the input file
input_file = open(in_name, 'r')
output_headers = []

# loop through input file and save the stripped strings to the output_headers list
for line in input_file:
	stripped_line = line.strip()
	stripped_line = stripped_line.strip(",")
	#stripped_line = stripped_line.strip("'")
	#stripped_line = stripped_line.strip(":")
	output_headers.append(stripped_line)
input_file.close()



column_index = []

# Look for the row index of each output header
# If it is not found, the script is ended
# If it is found, the row index is saved to the column_index list (the according row is the later on column of the data values)
for header_counter in range(len(output_headers)):
	does_not_contain_header = True
	line_counter = 0
	fl2_file = open(fl2_name, 'r')	   

	for line in fl2_file:		
		if output_headers[header_counter] in line:
			column_index.append(line_counter-1)
			does_not_contain_header = False
			break
		else:
			line_counter += 1           
	
        
	if does_not_contain_header:
		print "Could not find {a} in the fl2 file - aborting script!".format(a = output_headers[header_counter])
		fl2_file.close()
		sys.exit()	
	fl2_file.close()
fl2_file.close()


if debug_flag:
    print "---debug--- Column Index: \t {a}".format(a = column_index)	
 
#--- Process unit columns ------------------------------------------------------------------------------------------ 
line_counter = 0
start_row = checklist[1]
unit_list = []

fl2_file = open(fl2_name, 'r')
fl2_lines = fl2_file.readlines()
for i in range(len(column_index)):
    stripped_line = fl2_lines[start_row + column_index[i]].strip()
    stripped_line = stripped_line.strip(",")
    stripped_line = stripped_line.strip("&")
    stripped_line = stripped_line.strip(",")
    stripped_line = stripped_line.strip("UNIT = [")
    stripped_line = stripped_line.strip("'")    
    unit_list.append(stripped_line)
    #unit_list.append(fl2_lines[start_row + column_index[i]])

if debug_flag:
    print "---debug--- Unit namings: \t {a}".format(a = unit_list)
    
#--- Process the data columns ------------------------------------------------------------------------------------  
# define initial check parameters
line_counter = 0
start_row = checklist[2]
temp_list = []
data_lists = []

# Create a list of lists (array) that works like:
#         columns:     each column conatins one data set, that was specified in the input file
#         rows:        each row contains the time step- or crank angle resolved data sets that were specified in the input file
for i in range(len(column_index)):
    data_lists.append([])


if debug_flag:
    print "---debug--- Empty data list of lists: \t {a}".format(a = data_lists)


# Loop through the fl2 file, split the tab separated strings and then write accordingly to the list of lists (data_lists)
fl2_file = open(fl2_name, 'r')
for line in fl2_file:
    # Start after row that has the "END" string in it - this is where the actual data starts
    if line_counter > start_row:
        temp_list = line.split('\t')
        for i in range(len(column_index)):
            if debug_flag:
                print "---debug--- i: {a}".format(a = i)
                print "---debug--- column index: {a}".format(a = column_index[i]) 
            data_lists[i].append(temp_list[column_index[i]])
    line_counter += 1            
fl2_file.close()


if debug_flag:        
    for i in range(len(column_index)):    
        print "---debug--- Full data list of lists of {b}: \t {a}".format(a = data_lists[i], b = output_headers[i]) 

# Check for consistency - All columns have to have the same length        
for data_column in data_lists:
    if len(data_column) != len(data_lists[0]):
        print "Column lengths do not match, exiting script"
        sys.exit()
 
# Add the header and unit to the according data list
for i in range(len(column_index)):
    data_lists[i].insert(0,output_headers[i])
    data_lists[i].insert(1,unit_list[i])

if debug_flag:        
    for i in range(len(column_index)):    
        print "---debug--- Complete list of lists of {b}: \t {a}".format(a = data_lists[i], b = output_headers[i])         



#--- Write to one output file  -----------------------------------------------------------------------------------------
if debug_flag:
    print "---debug--- Lenght of one data set: {a}".format(a = len(data_lists[0]))
    print "---debug--- Number of columns in the data set: {a}".format(a = len(column_index))


out_file = open(out_name, 'w')


# Write the list of lists to an ouput
for row_ndx in range(len(data_lists[0])):
    for col_ndx in range(len(column_index)):
        if debug_flag:
            print"---debug--- row: {a} / column: {b}".format(a = row_ndx, b = col_ndx)
        #bugfix - if your want to read out ALL data, you have to remove the newline character from the last column
        out_file.write((data_lists[col_ndx][row_ndx] + '\t').replace("\n",""))
    out_file.write('\n')
out_file.close()


