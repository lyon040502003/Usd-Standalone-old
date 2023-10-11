import os
import pprint
import shutil

from code.Work_scripts.conf_files.conf import current_conf



class packed_usd_file_struckt:
    """
    This Class will hoste the variables for the foulder struckture
    and this class will hoste a construcktor to build the foulder struckture
    it will also include some cecks to decide how the foulder struckture schould look
    """

    def __init__(self, usd_exp_path) -> None:

        # Check if the user wants to create a usd file or a foulder
        # and if the user wants to create a usd file check if the location is empty
        # and if it is empty then create all the foulder there if not create a foulder in the pace
        if any(ext in usd_exp_path for ext in current_conf.usd_file_types):
            print("User Wants To Export Usd file, did not specifie Foulder")
            if len(os.listdir(os.path.dirname(usd_exp_path))) == 0: # Checking if the foulder is empty or not in order to determen if the user create the foulder for the export or not
                print("Directory is empty, will Create Foulder Struckture Hear")
                self.parent_foulder = os.path.dirname(os.path.abspath(usd_exp_path))
            else:
                print("Directory is not empty, will create subfoulder for foulder struckture and move export usd file into")
                self.parent_foulder = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(usd_exp_path)),os.path.abspath(usd_exp_path).split("\\")[-1].split(".")[0]))
            print("Foulder path will be set:", self.parent_foulder)


        self.usd_hoste_foulder = os.path.abspath(self.parent_foulder + "/usd") # TODO work with os.join 
        self.IO_hoste_foulder = os.path.abspath(self.parent_foulder + "/IO_foulders")

    def generate_foulder_struckt(self):
        """This Function build the Foulder Struckture that was defined at the inint funciton
        This Function will runn thre all attrubutes that have "foulder" in ther name and then use the Str defined in this attribute to generate the Foulder path
        """
        print("")
        #Generate Parent Foulder
        try:
            os.makedirs(self.parent_foulder)
        except:
            if len(os.listdir(self.parent_foulder)) != 0:
                print("Parend Foulder exists and is not empty")
                raise Exception("Pxr Search Error, will not attemt to Empty foulder do to no information about it's Curent use")
            else:
                print("Parent Dir Dose Allredy Exist, but is empty. will now continue with the foulder creation")
        # Create The Subfoulders
        try:
            os.mkdir(self.usd_hoste_foulder)
            os.mkdir(self.IO_hoste_foulder)
        except:
            shutil.rmtree(self.usd_hoste_foulder)
            shutil.rmtree(self.IO_hoste_foulder)

            os.mkdir(self.usd_hoste_foulder)
            os.mkdir(self.IO_hoste_foulder)


    def delet_foulder_struckt(self, must_empty : bool=True, del_zip: bool=False, error_when_dir_missing: bool=False):

        print("")

        if must_empty:
            if len(os.listdir(self.parent_foulder)) != 0:
                shutil.rmtree(self.parent_foulder)
            else:
                print("Foulder not empty, Will not delet")
        elif not must_empty: # TODO was dass den hier ?
            if error_when_dir_missing:
                print("force deleted foulder struckture :",self.parent_foulder)
                shutil.rmtree(self.parent_foulder)
            else:
                print("Foulder {} Donst exists, Will Continue on error".format(self.parent_foulder))
        if del_zip:
            shutil.rmtree(self.parent_foulder+".zip")


    def zip_foulder_struckture(self, remove_original: bool=False):
        shutil.make_archive(self.parent_foulder, 'zip', self.parent_foulder)
        print("Creaded : ", self.parent_foulder+".zip")

        if remove_original:
            self.delet_foulder_struckt(must_empty=False)
            print("Zip Function will Delet Orignial Foulder Struckt")

