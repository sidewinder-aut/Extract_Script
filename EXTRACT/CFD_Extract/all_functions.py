#!/usr/bin/python

"""
Subfunctions for the Extract_Caller.py file - The routines below DO NOT DO THE ACTUAL EXTRACTION. They just copy the necessary
input and setup files and then call the actual extraction files. This folder structure has been chosen on purpose to provide 
separate toolboxes for each extract procedure and a more modular coding structure.

[ date:     13. 12. 2016    ]
[ author:     L. Eder    ] 
"""

#--- LIBRARY IMPORT  --------------------------------------------------------------------------------------------
import string,sys
import time, os.path
import shutil
from sys import argv

#--- STEERING Parameters  ----------------------------------------------------------------------------------------
# debug flag for coding development only - to avoid debug output set the parameter to False
global debug_flag 
debug_flag = False

#--- MAIN FUNCTIONS ----------------------------------------------------------------------------------------------    
def create_output_folder(extract_folder, activation_switches):
    """
    Creation of output folder - It is checked whether the "Full Analysis" option is chosen, which currently only I use. According to the other
    activation switches the necessary folders are created.

    [ date:     13. 12. 2016    ]
    [ author:     L. Eder    ] 
    """
    
    # --- determination of activation switches
    full_analysis = activation_switches["full_analysis"]
    fl2_active = activation_switches["fl2_active"]
    fla_active = activation_switches["fla_active"]
    images_active = activation_switches["images_active"]
    copy_fla_active = activation_switches["copy_fla"]
    copy_ssf_active = activation_switches["copy_ssf"]
    copy_simcheck_active = activation_switches["copy_simcheck"]
    
    
    print"--- OUTPUT FOLDER GENERATION ------------------------------------------"
    
    # --- Procedure for "Full Analysis" type
    if full_analysis:        
        print "    *** Full Analysis type chosen - Copying the ex_ana folder from 00_Input"
        
        # Provision of necessary folder paths
        sourcefolder = extract_folder + "/CFD_Extract/ppe_toolbox/Full_Analysis"
        destifolder = extract_folder + "/Analysis_"
        
        if debug_flag:
            print "---debug--- Source of copytree: {a}".format(a = sourcefolder)
            print "---debug--- Destination of copytree: {a}".format(a = destifolder)
        
        # Check for already existing file - It is deleted, if there is one
        if os.path.isdir(destifolder):
            print "    *** Old Analysis directory removed"
            shutil.rmtree(destifolder)
            
        # Copy the template
        shutil.copytree(sourcefolder, destifolder)
    
    # --- Procedure for "Standard Analysis" type
    else:
        print "    *** Standard analysis chosen - Creating a Results_extract folder"
        
        # Provision of necessary folder paths
        destifolder = extract_folder + "/Results_extract"
        
        # Check for already existing file - It is deleted, if there is one
        if os.path.isdir(destifolder):
            print "    *** Old Results_Extract directory removed"
            shutil.rmtree(destifolder)
        
        # Check activation switches and create necessary files  
        os.mkdir(destifolder)
        
        # Create extract log file
        commandline = "touch " + destifolder + "/extract.log"
        os.system(commandline)
        print "    *** Logfile created"
        
        if fl2_active: os.mkdir(destifolder + "/2D_fl2_results") 
        if fla_active: os.mkdir(destifolder + "/2D_fla_results") 
        if images_active: os.mkdir(destifolder + "/Figures")
        if (copy_fla_active or copy_ssf_active or copy_simcheck_active): 
            os.mkdir(destifolder + "/Additional_files") 
            if copy_fla_active: os.mkdir(destifolder + "/Additional_files/fla_files")
            if copy_ssf_active: os.mkdir(destifolder + "/Additional_files/ssf_files")
            if copy_simcheck_active: os.mkdir(destifolder + "/Additional_files/SimCheck")
    print"-----------------------------------------------------------------------"
    print''
    
    return destifolder    


def fl2_extract(extract_folder, case_folder, output_folder, activation_switches):
    """
    fl2 extract caller - The necessary files are copied, the fl2 extract is called and then the resulting
    output files are copied back again.

    [ date:     13. 12. 2016    ]
    [ author:     L. Eder    ] 
    """    
    # --- determination of activation switches    
    # --- Provision of necessary folder paths
    is_active = activation_switches["fl2_active"]
    output_folder = output_folder + "/2D_fl2_results/"      
    fl2_destifolder = case_folder + "/2D_Results/"  
    
    # --- Check if fl2 is active
    if not is_active or not os.path.isdir(fl2_destifolder):
        if not is_active: print "    xxx FL2 Extraction inactive - skipping the fl2 extract procedure"
        if not os.path.isdir(fl2_destifolder): print "    xxx No 2D_results folder found in {a} - skipping fl2 extract procedure".format(a = case_folder)
        return
    
    else:
        # Provision of necessary folder paths
        fl2_sourcefolder = extract_folder + "/CFD_Extract/fl2_toolbox/"
        fl2_destifolder = case_folder + "/2D_Results/"
        extract_file = "fl2_multiextract.py"
        input_file = "input.txt"
        if debug_flag:
            print "---debug--- Source folder: {a}".format(a = fl2_sourcefolder)
            print "---debug--- Destination folder: {a}".format(a = fl2_destifolder)    
            
        # Check, if there is an input file for the extract procedure to work with
        if not os.path.isdir(fl2_sourcefolder):
            print "    !!! Could not find fl2 input folder - It should be: {a}".format(a = fl2_sourcefolder)
            sys.exit()        
        else:    
            # Copy the necessary files to the current case folder and change into the directory
            shutil.copyfile(fl2_sourcefolder + extract_file, fl2_destifolder + extract_file)
            shutil.copyfile(fl2_sourcefolder + input_file, fl2_destifolder + input_file)
            os.chdir(fl2_destifolder)
            
            # Make files executable 
            commandline = "chmod +x " + extract_file
            os.system(commandline)
            print '    *** FL2 Extract script started'
            
            # Start fl2 extract script
            commandline = "./" + extract_file + " " + os.path.split(case_folder)[1] + "_fl2.gid input.txt output.txt" 
            if debug_flag:
                print "---debug--- Current working directory: {a}".format(a = os.getcwd())
                print "---debug--- os.system command: {a}".format(a=commandline)
            os.system(commandline)
            
            # Provision of necessary folder paths
            old_output_name = "output.txt"
            new_output_name = os.path.split(case_folder)[1] + "_fl2.txt"
            os.rename(old_output_name, new_output_name)
            
            # Remove the stuff that is not needed any more from the case folder
            os.remove(extract_file)
            os.remove(input_file)
            
            # Move back the result file
            shutil.move(fl2_destifolder + "/" + new_output_name, output_folder + "/")
            
        return
    
def fla_extract(extract_folder, case_folder, output_folder, activation_switches):
    """
    fla extract caller - The necessary files are copied, the fla extract is called and then the resulting
    output files are copied back again.

    [ date:     13. 12. 2016    ]
    [ author:     L. Eder    ] 
    """    
    # --- determination of activation switches    
    # --- Provision of necessary folder paths
        
    is_active = activation_switches["fla_active"]
    log_file = output_folder + "/extract.log"
    output_folder = output_folder + "/2D_fla_results/"        
    
    # --- Check if fla is active
    if not is_active:
        print "    xxx FLA Extraction inactive - skipping the fla extract procedure"
        return
    else:
        # Provision of necessary folder paths
        fla_sourcefolder = extract_folder + "/CFD_Extract/fla_toolbox/"
        fla_destifolder = case_folder + "/"
        extract_file = "fla_extract.py"
        input_file = "extract_log.input"
        join_file = "fla_joinfiles.py"


        if debug_flag:
            print "---debug--- Source folder: {a}".format(a = fla_sourcefolder)
            print "---debug--- Destination folder: {a}".format(a = fla_destifolder)    
            print "---debug--- Logfile location: {a}".format(a = log_file)
        # Check, if there is an input file for the extract procedure to work with    
        if not os.path.isdir(fla_sourcefolder):
            print "    !!! Could not find fla input folder - It should be: {a}".format(a = fla_sourcefolder)
            sys.exit()        
        else:
            # Copy the necessary files to the current case folder and change into the directory    
            shutil.copyfile(fla_sourcefolder + extract_file, fla_destifolder + extract_file)
            shutil.copyfile(fla_sourcefolder + input_file, fla_destifolder + input_file)
            shutil.copyfile(fla_sourcefolder + join_file, fla_destifolder + join_file)
            
            os.chdir(fla_destifolder)
            
            # Check if there is already an XMGR folder in the case directory - If not, make one
            if not os.path.isdir(case_folder + "/XMGR"):
                os.mkdir("XMGR")
            
            
            # Make files executable     
            commandline = "chmod +x " + extract_file
            os.system(commandline)
            commandline = "chmod +x " + join_file
            os.system(commandline)
            
            # Start the fla extract script
            print '    *** FLA Extract script started at: {a}'.format(a = os.getcwd())
            commandline = "./" + extract_file + " " + os.path.split(case_folder)[1] + ".fla " + input_file + ">> " + log_file
            os.system(commandline)
            if debug_flag:
                print "---debug--- Current working directory: {a}".format(a = os.getcwd())
                print "---debug--- os.system command: {a}".format(a=commandline)
            
            # Start the joining of the fla extract files 
            print '*** Joining files in XMGR folder'
            commandline = "./" + join_file
            os.system(commandline)
            if debug_flag:
                print "---debug--- Current working directory: {a}".format(a = os.getcwd())
                print "---debug--- os.system command: {a}".format(a=commandline)
            
            # Rename some stuff and provide new folder path destinations
            old_output_name = "complete.txt"
            new_output_name = os.path.split(case_folder)[1] + "_fla.txt"
            os.rename(old_output_name, new_output_name)
            
            # Remove unnecessary stuff that is not needed any more in the case directory
            os.remove(extract_file)
            os.remove(input_file)
            os.remove(join_file)
            
            # Copy back the results file 
            shutil.move(fla_destifolder + "/" + new_output_name, output_folder + "/")
            
        return
    
def images_extract(extract_folder, case_folder, output_folder, activation_switches):
    """
    Image extract caller - The necessary files are copied, the image extract macro is called and then the resulting
    output files are copied back again.

    [ date:     13. 12. 2016    ]
    [ author:     L. Eder    ] 
    """   
    # --- determination of activation switches    
    # --- Provision of necessary folder paths     
    is_active = activation_switches["images_active"]
    log_file = output_folder + "/extract.log"    
    output_folder = output_folder + "/Figures/"        
        
    # --- Check if image extraction is active
    if not is_active or not os.path.isdir(case_folder+"/3D_Results"):
        if not is_active: print "    xxx Image Extraction inactive - skipping the image extract procedure"
        if not os.path.isdir(case_folder+"/3D_Results"): print "    xxx No 3D_Results folder foudn in case directory - skipping the image extract procedure"
        return
    else:
        images_sourcefolder = extract_folder + "/CFD_Extract/img_toolbox/Macro/"
        images_destifolder = case_folder + "/Macro"
        #macro_folder = "Macro"

        if debug_flag:
            print "---debug--- Macro folder: {a}".format(a = images_destifolder)
    
        # Check, if there is an input file for the extract procedure to work with       
        if not os.path.isdir(images_sourcefolder):
            print "    !!! Could not find Macro input folder - It should be: {a}".format(a = images_sourcefolder)
            sys.exit()        
        else:    
            
            # Copy the necessary stuff to the folder
            if os.path.isdir(images_destifolder):
                shutil.rmtree(images_destifolder)
            shutil.copytree(images_sourcefolder,images_destifolder)
            
            os.chdir(images_destifolder)
                            
            commandline = "chmod +x fire_post_case.macro start_fire_post_case.py" 
            os.system(commandline)
            
            # Start image extraction
            print '    *** Images Extract script started'
            commandline = "./start_fire_post_case.py  >> " + log_file
            os.system(commandline)
            if debug_flag:
                print "---debug--- Current working directory: {a}".format(a = os.getcwd())
                print "---debug--- os.system command: {a}".format(a=commandline)
            
            # Copy the created folder back to the extract destination folder
            os.chdir("../")    
            shutil.rmtree("Macro")
            os.rename("Figures_3D", case_folder + "_fl3")
            shutil.move(case_folder + "_fl3", output_folder)
            
        return
    
 
def get_additional_files(extract_folder, case_folder, output_folder, activation_switches):    
    """
    Function fetches additonal files to the output folder - Currently *.fla, *.ssf files and SimCheck folders can be fetched
    Please consider the activation switches.

    [ date:     13. 12. 2016    ]
    [ author:     L. Eder    ] 
    """       
    # --- determination of activation switches
    copy_fla_active = activation_switches["copy_fla"]
    copy_ssf_active = activation_switches["copy_ssf"]
    copy_simcheck_active = activation_switches["copy_simcheck"]
    
    # --- Check if any copy check is activated    
    if (not copy_fla_active and not copy_ssf_active and not copy_simcheck_active):
        print "    xxx No additional files fetched"
        return
    else:
        # Copy fla files
        if copy_fla_active:
            dest_folder = output_folder + "/Additional_files/fla_files" 
            filename = os.path.basename(case_folder) + ".fla"
            fla_destifolder = case_folder + "/"            
            shutil.copyfile(fla_destifolder + filename , dest_folder + "/" + filename)
            print "    *** fla files fetched"
            
        # Copy ssf files    
        if copy_ssf_active:
            dest_folder = output_folder + "/Additional_files/ssf_files" 
            filename = os.path.basename(case_folder) + ".ssf"
            fla_destifolder = case_folder + "/"            
            shutil.copyfile(fla_destifolder + filename , dest_folder + "/" + filename)
            print "    *** ssf files fetched"
            
        # Copy SimCheck folders    
        if copy_simcheck_active:
            dest_folder = output_folder + "/Additional_files/SimCheck" 
            check_sourcefolder = case_folder + "/SimCheck"
            shutil.copytree(check_sourcefolder,dest_folder + "/" + os.path.basename(case_folder))   
            print "    *** SimCheck folder fetched"
    return