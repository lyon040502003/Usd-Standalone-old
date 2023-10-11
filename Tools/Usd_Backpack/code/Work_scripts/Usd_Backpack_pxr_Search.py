import os
from pxr import Usd
from pxr import Vt
import pprint
import shutil

from code.Work_scripts.conf_files.conf import current_conf


#usdcat C:\Users\lyonh\cube.usd --out C:\Users\lyonh\cube.usd --usdFormat usda # converts to usda but dosnt rename to usda


def find_usd_objects_and_files(stage):
    
    stage = Usd.Stage

    for prim in stage.Traverse():
        print (prim.GetPath())
        print("info", stage.GetPrimAtPath(prim.GetPath()).GetTypeName())
        for child in prim.GetChildren():
            print("child", child.GetPath(),"\n")
            print("all Atts")
            pprint.pprint(child.GetAttributes())

            for atts in child.GetAttributes():
                if "file" in str(atts):
                    print("\n","Found File at", child.GetPath())
                    print(child.GetAttribute(str(atts).split(".")[-1].split("'")[-2]).Get())
                    print("Paren_File",str(child.GetPrimStack()[-1]).split(",")[-2].split("'")[-2])
            print("-"*80)
            print("")''
