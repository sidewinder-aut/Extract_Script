#!/usr/bin/python

"""
Caller file for all extract procedures. fl2 files, fla files can be extracted for certain variables - Please see the specific 
toolbox subfolder for further information on how to use the fl2 extract and fla extract file. 
Images can be extracted with the AVL FIRE Macro provided by AVL/AST. 
For all the above mentioned, the necessary input files have to be provided in the specific *_toolbox folder. Furthermore the 
activation switches have to be set to "True" (see steering parameters from line 28 to 42)
*.ssf files, *.fla files and SimCheck folders can be saved to the output folder as well.

[ date:     13. 12. 2016    ]
[ author:     L. Eder    ]
"""


#--- LIBRARY IMPORT  ---------------------------------------------------------------------------------------
import string,sys
import time, os.path
import CFD_Extract

# Abbreviation for the later module calls
ext = CFD_Extract


#--- STEERING Parameters  ---------------------------------------------------------------------------------------
# debug flag for coding development only - to avoid debug output set the parameter to False
global debug_flag 
debug_flag = False

# Activation switches for the single extract and copy procedures - See documentation for further information
# True - Activated procedure
# False - Procedure shut off

activation_switches = {
    "fl2_active":       True, 
    "fla_active":       False, 
    "images_active":    True, 
    "full_analysis":    False,
    "copy_fla":         True,
    "copy_ssf":         True,
    "copy_simcheck":    True    
}

case_folder_specific = True
searchstring = ""

#--- CHECK FOR VALID INPUT ---------------------------------------------------------------------------------
print '\n---------------------------------- Extract script started at: {a} ---------------------------------- \n'.format(a = time.strftime('%d. %B %Y %H:%M'))

# Get current folder and the calculation directory path --> CAUTION - The script assumes that the EXTRACT folder is in the project directory
extract_folder = os.getcwd()
calculation_folder = os.getcwd() + "/../Calculation"

if debug_flag:
    print "---debug--- Extract folder: {a}".format(a = extract_folder)
    print "---debug--- Calculation folder: {a}".format(a = calculation_folder)
    
# get a list of the case folders in the calculation directories    
case_names = [] 
for foldername in os.listdir(calculation_folder):
    if case_folder_specific:
        if foldername.find(searchstring) != -1:
            case_names.append(foldername)  
    else:
        case_names.append(foldername)
    
if debug_flag:
    print "---debug--- Case folders in calculation directories: {a}".format(a = case_names)

# creation of output folder path
output_folder = ext.create_output_folder(extract_folder, activation_switches)

# Get shell caller file if there is one

print"--- EXTRACT OPERATIONS  -----------------------------------------------"

if debug_flag:
    print "---debug--- Output folder: {a}".format(a = output_folder)

#--- FOLDER LOOP ------------------------------------------------------------------------------------------------    
for i in range(len(case_names)):
    # Get current case folder
    case_folder = calculation_folder + "/" + case_names[i] 
    print'--- {a}:'.format(a = os.path.basename(case_folder))
    
    # Call all the extract procedures
    ext.fl2_extract(extract_folder, case_folder, output_folder, activation_switches)    
    ext.fla_extract(extract_folder, case_folder, output_folder, activation_switches) 
    ext.images_extract(extract_folder, case_folder, output_folder, activation_switches)
    ext.get_additional_files(extract_folder, case_folder, output_folder, activation_switches)
    
print"-----------------------------------------------------------------------"
print''
print '---------------------------------- Extract script ended at: {a} ---------------------------------- \n'.format(a = time.strftime('%d. %B %Y %H:%M'))



