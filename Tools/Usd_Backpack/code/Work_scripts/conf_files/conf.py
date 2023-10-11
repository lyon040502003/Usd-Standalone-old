import os 

class op_conf():
    
    def __init__(self) -> None:

        self.geo_file_types = usd_file_types = [line.rstrip() for line in open("code/Work_scripts/conf_files/3d_geo_files_formats.txt")]
        self.image_file_types = usd_file_types = [line.rstrip() for line in open("code/Work_scripts/conf_files/Image_file_types.txt")]
        self.usd_file_types = usd_file_types = [line.rstrip() for line in open("code/Work_scripts/conf_files/usd_file_formats.txt")]


current_conf = op_conf()