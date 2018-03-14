#!/usr/bin/python

"""
Read in for AVL-FIRE *.fla file - You have to exectue the extract_fla.py first and before that create an XMGR folder. Otherwise this won't work

[ date:     15. 11. 2016    ]
[ author:     L. Eder    ]

    [ output ]
        textfile = output.txt
    
        
"""

#--- LIBRARY IMPORT  ---------------------------------------------------------------------------------------
import string,sys
import time, os.path
from sys import argv

debug_flag = False

#--- MAIN PROGRAM ---------------------------------------------------------------------------------------
#print 'FLA Extract script started at: {a}'.format(a = os.getcwd())


#--- CHECK FOR VALID INPUT ---------------------------------------------------------------------------------

# Check if XMGR folder exists 
xmgr_folder_path = os.getcwd()+ "/XMGR"
if not os.path.isdir(xmgr_folder_path):
    print "No XMGR folder found in: {a}".format(a = os.getcwd())
    print "Exiting script"
    sys.exit()


# Check if XMGR folder contains *.res files  
for fname in os.listdir('./XMGR'):
    if fname.endswith('.res'):
        contains_res_files = True
        break

if not contains_res_files:   
    print "No *.res files found in: {a}".format(a = xmgr_folder_path)
    print "Exiting script"
    sys.exit()

    
#--- Collect names for lateron output ---------------------------------------------------------------------------------    

output_headers = []
output_headers.append('Time or CA')

# Write the data header to a separate list
for fname in os.listdir(xmgr_folder_path):
    if fname.endswith('.res'):
        output_headers.append(fname.split(".")[0])

if debug_flag:        
    print "---debug--- Output headers: {a}".format(a = output_headers)

complete_lists = []
number_of_columns = len(output_headers)

for i in range(number_of_columns):
    complete_lists.append([])

if debug_flag:
    print "---debug--- Empty list of lists: {a}".format(a = complete_lists)


col_counter = 1   

for fname in os.listdir(xmgr_folder_path):
    complete_lists[col_counter].append(output_headers[col_counter])
    complete_lists[col_counter].append('unit')
    if col_counter == 1:
        complete_lists[0].append(output_headers[0])
        complete_lists[0].append('unit')
    input_file = open('./XMGR/' + fname, 'r')
    for line in input_file: 
        complete_lists[col_counter].append(line.split('\t')[1].split("\n")[0])
        if col_counter == 1:
            complete_lists[0].append(line.split('\t')[0].split("\n")[0])
    input_file.close()
    col_counter += 1 

if debug_flag:
    for i in range(len(output_headers)):
        print "---debug--- Entries for {b}: {a}".format(a = complete_lists[i], b = output_headers[i])

for column in complete_lists:
    if len(column) != len(complete_lists[0]):
        print "Length of current column = {a}, length of reference column = {b}".format(a = len(column), b = len(complete_lists[0]))
        print "Column lengths do not match, exiting script"
        sys.exit()
    
# Write the list of lists to an ouput

out_file = open("complete.txt", 'w')
for row_ndx in range(len(complete_lists[0])):
    for col_ndx in range(number_of_columns):
        if debug_flag:
            print"---debug--- row: {a} / column: {b}".format(a = row_ndx, b = col_ndx)
        out_file.write(complete_lists[col_ndx][row_ndx] + '\t')
    out_file.write('\n')
out_file.close()    

        