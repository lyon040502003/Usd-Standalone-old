import os
import shutil
import re
import fnmatch
import fileinput
from pathlib import Path

# define master file paths
file_path = "E:/Tools/USDA_backpack/test_cases/usd_backpack_test_cases/Simple_tester/Sceene/main_sccene_render.usda"
new_file_path = "E:/Tools/USDA_backpack/test_cases/usd_backpack_test_cases/test_out/simple_test_exp_test.usda"




# define default file vars
file_dir = os.path.split(file_path)[0]
file_name = file_path.split("/")[-1]
file_drive = file_path.split("/")[-0]


# deine paths for the new files to go to 
sublayer_files = os.path.split(new_file_path)[0].replace('/','\\') + "\\usd_tex\\IO_files"
sublayer_usda_files = os.path.split(new_file_path)[0].replace('/','\\') + "\\usd_tex\\usda\\"

# dic off all files that need to be copied and the destination where ther have to go to 
IO_file_sorce_dic = dict()
IO_file_copy_dic = dict()

# list off all usda files that need checking
master_layer_usda_sorce = []
master_layer_usda_destination = []

all_written_usda_files = []

texture_file_types = [line.rstrip() for line in open('USDA_Backpack_scripts/Work_scripts/conf_files/Image_file_types.txt')]
usd_file_types = [line.rstrip() for line in open('USDA_Backpack_scripts/Work_scripts/conf_files/usd_file_formats.txt')]
usd_file_types.remove(".usda")
Geo_file_types = [line.rstrip() for line in open('USDA_Backpack_scripts/Work_scripts/conf_files/Image_file_types.txt')]


Hou_dir = "C:/Program Files/Side Effects Software/Houdini 19.5.435/bin/"
iconver_exe = "iconvert.exe"





#         /// FUNCTIONS ////  

def refactor_copy_dic(copy_dic):

    udim_work_dic = dict()
    udim_files = []
    udim_files_destination = []
    for sorce in copy_dic:
        if "<UDIM>" in sorce:
            udim_files.append(sorce)  
            udim_files_destination.append(copy_dic[sorce])
            udim_work_dic[sorce]=copy_dic[sorce]  
        else:
            IO_file_copy_dic[sorce]=copy_dic[sorce]  
    for files in udim_work_dic:
        print("files in the work dic", files)
        print(os.listdir(os.path.dirname(os.path.abspath(files))))
        filenames = fnmatch.filter(os.listdir(os.path.dirname(files)), '*')
        target_file_dir = os.path.dirname(udim_work_dic[files])
        file_front = files.split("\\")[-1].replace("<UDIM>", "/").split("/")[0]
        file_back = files.split("\\")[-1].replace("<UDIM>", "/").split("/")[1]
        for tex in filenames:
            if re.search(f'{file_front}1[0-9][0-9][0-9]{file_back}', tex):
                IO_file_copy_dic[os.path.join(os.path.dirname(files),tex)] = os.path.join(target_file_dir,tex)

class file_manager():
        
    def copy_files(IO_dic):
        
        for sorce in IO_dic:
            print("file to copy  ",IO_dic[sorce])
            if  os.path.exists(IO_dic[sorce]): 
                os.remove(IO_dic[sorce])
                print("file existed, remove file ",IO_dic[sorce])
                shutil.copy(sorce, IO_dic[sorce])
            else:
                Path(os.path.abspath(os.path.dirname(IO_dic[sorce]))).mkdir(parents=True, exist_ok=True)
                print("dir_created", os.path.abspath(os.path.dirname(IO_dic[sorce])))
                shutil.copy(sorce, IO_dic[sorce])
            print(" file copyied f/t", sorce, "  //  ", IO_dic[sorce],".\n")
                
    
    def convert_to_rat(IO_dic,usd_dic):
        for sorce_file in IO_dic: 
            in_file = os.path.abspath(IO_dic[sorce_file])
            if in_file.endswith(".hdr"):
                print("hdr_files_will_not_be_converted", in_file)
            else:
                print("rat conf files:",in_file)
                cmd_iconvert_command = "-g off  -d float  " + in_file +"  " + in_file.replace(in_file.split("/")[-1].split(".")[-1],'rat')
                cmd_command = '"'+Hou_dir+iconver_exe+'" '+ cmd_iconvert_command
                os.system(cmd_command)
                os.remove(in_file)
            
        for file in usd_dic:
            work_file = os.path.abspath(file)
            print("recursive files ", work_file)
            with fileinput.input(inplace=True,files=(work_file)) as f:
                for line in f:
                    if any(ext in line for ext in texture_file_types) and ":file" in line and not line.split("@")[-2].endswith(".hdr"):      
                        print(line.replace(line.split("@")[-2].split(".")[-1], "rat"))

                    else:
                        print(line)

class line_runner():

    def build_file_pathing(line,curent_file):
        print("line_runner_build_file_pathing_args", line, curent_file)
        
        old_rel_path = "@" + (line.strip().split("@"))[-2] + "@"
        
        
        sorce_rel_file = line.split("@")[-2]
        sorce_abs_file = os.path.abspath(curent_file.replace(curent_file.split("\\")[-1],sorce_rel_file))
        
        new_work_file_path = os.path.abspath(sublayer_usda_files+"\\"+curent_file.split("\\")[-2] + "\\" + curent_file.split("\\")[-1])
        
        new_abs_file_path = os.path.abspath(sublayer_files+"\\"+sorce_abs_file.split("\\")[-2] + "\\" + sorce_abs_file.split("\\")[-1])
        new_rel_file_path2 = os.path.relpath(new_abs_file_path, new_work_file_path).replace("\\","/")[1:]
        new_rel_path_line = "@" + new_rel_file_path2 + "@"
        print("paths",new_rel_path_line)
        
        print("")
        return new_rel_path_line, old_rel_path, new_abs_file_path, sorce_abs_file




    def run_true_line(file_to_run_true, new_file_write, function_set):
        
        """This function Truns True a file in and writes the output in to the coresponding list

        Args:
            file_to_run_true (String): this is the file that you want to be searched true
            new_file_write (String): this is the new file you are trying to write out 
            function_set (int): this is a varible that selects the functions to runn (1: all texture files types, 2: all usd files (exept usda), 3:usda files, 9:all)
        """    
        print("")
        print("line_runner file to run true   ",file_to_run_true)


        for line in file_to_run_true:
            
            if any(ext in line for ext in texture_file_types) and ":file" in line: 
                print("line_runner_run_true_line ", file_to_run_true.name)
                print(texture_file_types)
                print("tex file found ", line)
                result = line_runner.build_file_pathing(line,file_to_run_true.name)
                
                IO_file_sorce_dic[result[3]] = result[2]
                new_file_write.write(line.replace(result[1], result[0]))    

                
            elif any(ext in line for ext in usd_file_types) and not "@usda": # this function exists because it will be important to report all non usda usd files in order to show the files that might not be resolved in the ui 

                result = line_runner.build_file_pathing(line)
                IO_file_sorce_dic[result[3]] = result[2]
                new_file_write.write(line.replace(result[1], result[0])) 


            elif "usda@" in line:
                
                print("line runner usda found  ")
                print("line runner curent work file ", file_to_run_true.name)
                print("line runner file taht gets created ", new_file_write.name)
                file_to_copy = os.path.abspath(file_to_run_true.name.replace(os.path.abspath(file_to_run_true.name).split("\\")[-1], line.split("@")[-2]))
                print("original abs path test" ,file_to_copy)
                new_abs_path = os.path.abspath(sublayer_usda_files+"\\"+file_to_copy.split("\\")[-2] + "\\" + file_to_copy.split("\\")[-1])
                print("new abs path for copy",new_abs_path)
                print("work line  ", line)
                new_rel_path = os.path.relpath(new_abs_path, new_file_write.name)[1:]
                print("new_rel_path ", new_rel_path)
                new_line = line.replace(line.split("@")[-2],new_rel_path.replace("\\","/"))
                print("new line", new_line)
                new_file_write.write(new_line)
                

            else:
                new_file_write.write(line)

# function to recursivle search true all usda files 
def recurve_usda_search(file):

    usd_files = []
    opend_file = open(file, "r")
    # go true all the lines  in the usda file
    for line in opend_file:
        
        # find all the usda files in the master file
        if "usda@" in line:
            os.chdir(os.path.dirname(os.path.abspath(file)))  

            
            # build full file path for the files to copy from the relative path       
            file_to_copy = os.path.abspath((line.strip().split("@"))[-2]).replace('/','\\') 
            # appen to the sorce and target list
            master_layer_usda_sorce.append(file_to_copy.replace('/','\\'))

            
            # array to all files in the found
            usd_files.append(file_to_copy)  
            
    # recursevly search true all found usda files
    for files in usd_files:
        print("recrusive search found   ", files)
        recurve_usda_search(files)
    opend_file.close()

# function to find all files in all usda files and write new usda files 
def search_true_usda_files(usda_files): 
    for file in usda_files:
        print("text", file)
        new_file_pos = os.path.abspath(sublayer_usda_files+file.split("\\")[-2]+"\\" +file.split("\\")[-1])
        new_usda_file_dir = os.path.dirname(new_file_pos)
        if  os.path.exists(new_file_pos): 
            print("exists")
            os.remove(new_file_pos)
            print("file existed and was replaced : ",new_file_pos)
            new_file_write = open(os.path.abspath(new_file_pos),"w")
        else:
            Path(new_usda_file_dir).mkdir(parents=True, exist_ok=True)
            new_file_write = open(os.path.abspath(new_file_pos),"w")
            print("dir was missing and file was created :",new_file_pos)
        print("created usda file : ",new_file_pos)


        opend_file_old = open(file, "r")

        new_file_path = os.path.abspath(sublayer_usda_files+file.split("\\")[-2]+"\\" +file.split("\\")[-1])
        #new_file_write = open(new_file_path,"w")
        all_written_usda_files.append(new_file_path)

        line_runner.run_true_line(opend_file_old,new_file_write, 5)
        print("search_true_usda_files work file   ",opend_file_old)
        new_file_write.close()

# Function that bilds the master usda file 
def write_new_master_usda_file(old_master_usda_file, new_master_usda_file):
    
    old_file = open(old_master_usda_file)
    new_file_write = open(new_master_usda_file,"w")
    all_written_usda_files.append(new_master_usda_file)
    line_runner.run_true_line(old_file,new_file_write, 5)
    old_file.close()
    new_file_write.close()

#      /// Calls ///


def calls():
    
    recurve_usda_search(file_path)
    search_true_usda_files(master_layer_usda_sorce)

    write_new_master_usda_file(file_path,new_file_path)
    refactor_copy_dic(IO_file_sorce_dic)
    
    file_manager.copy_files(IO_file_copy_dic)
    file_manager.convert_to_rat(IO_file_copy_dic,all_written_usda_files)

    

calls()

#      /// TEST PINTS ///

