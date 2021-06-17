# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Toolbox: Tree Belt Gap Detection tools
# Analysis: automatic tool allowing to spatial diagnosis of TB expressed through distributions of TB gaps between, under and inside trees and shrubs, enabling further windbreak efficiency assessment
# Citation:
# Description:
# Author script: Pedziwiatr K., Nowak M."
# Version__="20210610_1264"
# ---------------------------------------------------------------------------

import os
import arcpy
from arcpy.sa import *

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("3D")

in_las_file = arcpy.GetParameterAsText(0)
out_folder = arcpy.GetParameterAsText(1)
clip = arcpy.GetParameterAsText(2)
h2= arcpy.GetParameterAsText(3)
h3= arcpy.GetParameterAsText(4)
classes_= arcpy.GetParameterAsText(5) #"3;4;5"
first_return=arcpy.GetParameter(6)#False

arcpy.AddMessage(first_return)
arcpy.AddMessage(type(first_return))

arcpy.env.workspace = out_folder
extract_name= "extract.lasd"
new_class=21
new_class2=22
new_class3=23

h1=[h2,h3]
classes=[]
arcpy.AddMessage(".........start............ ")
for c in classes_.split(';'):
    classes.append(int(c))

try:
    #extract shape, choise class 345, classification to firrt return and all returns
    arcpy.AddMessage("Extract LAS file..")
    arcpy.ExtractLas_3d(in_las_file,out_folder,"",clip,"","", "","REARRANGE_POINTS","",extract_name)
    Out_path_extract = os.path.join(out_folder, extract_name)

    #wszytskie punkty
    if first_return==False:
        arcpy.AddMessage("Choice all cloud points..")
        ldl_all=arcpy.MakeLasDatasetLayer_management(extract_name, "sl_all",classes)
        s="_"
        text=("density_range", "_ALL_P.tif")
        name_all= s.join(text)
        path_slice=os.path.join(out_folder, name_all)
        st_all=arcpy.LasPointStatsAsRaster_management("sl_all", path_slice, "POINT_COUNT", "CELLSIZE", 1)
        #change classes 345 to 0
        for j in classes:
            change_cl_all=arcpy.ChangeLasClassCodes_3d("sl_all",[[j,0]],"COMPUTE_STATS")  # zmiana klas na 0
        # change class by height
        classH=arcpy.ClassifyLasByHeight_3d("sl_all", "GROUND",[[new_class,h1[0]],[new_class2,h1[1]],[new_class3,100]])

        Out_path_all_points= os.path.join(out_folder, path_slice)
        arcpy.env.snapRaster = Out_path_all_points
        # choise the interval - class 22
        s="_"
        text=("vertical_range_", str(h1[0]), str(h1[1]), "_ALL_P")
        name22= s.join(text)
        outExtension=".tif"
        path_slice22=os.path.join(out_folder, name22+outExtension)
        
        ldl_all_22=arcpy.MakeLasDatasetLayer_management(classH, name22,new_class2)
        #statistics for class 22
        h_all_22=arcpy.LasPointStatsAsRaster_management(name22, path_slice22, "POINT_COUNT", "CELLSIZE", 1)
        arcpy.AddMessage("1/2")


    # max count points cloud in px in slices
    if first_return==False:
        pp=arcpy.RasterToNumPyArray(path_slice22)
        max_all=pp.max()
        print("max count cloud points in pixel in all return ", type(max_all))
        print("max count cloud points in pixel in all return ",max_all)
        
        #% count px to max value px
        result_22=(Raster(path_slice22)*100)/float(max_all)
        print("result to ", result_22)
        
        fc_out=os.path.join(out_folder, "PER_MAX_"+name22+outExtension)
        print("fc_out to " , fc_out )
        result_22.save(fc_out)
        arcpy.AddMessage("2/2")


    #first return
    if first_return==True:
        arcpy.AddMessage("Choice first return cloud points..")
        ldl_1r=arcpy.MakeLasDatasetLayer_management(extract_name, "sl_1r",classes,"1") #1 this is first return (1r)
        path_slice1=os.path.join(out_folder, "return_1.tif")
        s="_"
        text=("density_range",  "_1R.tif")
        name_all= s.join(text)
        path_slice1=os.path.join(out_folder, name_all)
        st_1r=arcpy.LasPointStatsAsRaster_management("sl_1r", path_slice1, "POINT_COUNT", "CELLSIZE", 1)
        #change classes 345 to 0
        for j in classes:
            change_cl_1r=arcpy.ChangeLasClassCodes_3d("sl_1r",[[j,0]],"COMPUTE_STATS") # change classes 345 to 0
        # change class by height
        classH1=arcpy.ClassifyLasByHeight_3d("sl_1r", "GROUND",[[new_class,h1[0]],[new_class2,h1[1]],[new_class3,100]])

        Out_path_all_points= os.path.join(out_folder, path_slice1)
        arcpy.env.snapRaster = Out_path_all_points
        
        Out_path_all_points= os.path.join(out_folder, "sl_1r")
        arcpy.env.snapRaster =Out_path_all_points
        
        # choise the interval - class 22
        s="_"
        text=("vertical_range", str(h1[0]), str(h1[1]), "r_1")
        name22_1= s.join(text)
        outExtension=".tif"
        path_slice22_1=os.path.join(out_folder, name22_1+outExtension)
        
        ldl_1_22=arcpy.MakeLasDatasetLayer_management(classH1, name22_1,new_class2,1)
        #statistics for class 22
        h_1_22=arcpy.LasPointStatsAsRaster_management(name22_1, path_slice22_1, "POINT_COUNT", "CELLSIZE", "1")
        arcpy.AddMessage("1/2")

    # max count points cloud in px in slices
    if first_return==True:
        pp=arcpy.RasterToNumPyArray(path_slice22_1)
        max_1=pp.max()
        print("max count cloud points in pixel in first return ", type(max_1))
        print("max count cloud points in pixel in first return ",max_1)
        
        #% count px to max value px
        result_22_1=(Raster(path_slice22_1)*100)/float(max_1)
        print("result to ", result_22_1)
        
        fc_out1=os.path.join(out_folder, "PER_MAX_"+name22_1+outExtension)
        print("fc_out to " , fc_out1 )
        result_22_1.save(fc_out1)
        arcpy.AddMessage("2/2")

    arcpy.CheckInExtension("Spatial")
    arcpy.CheckInExtension("3D")
    arcpy.AddMessage("Ok... finish")
    arcpy.AddMessage(classes)
    arcpy.AddMessage(h1)


except Exception as err:
    print ("Error "+str(err))
    arcpy.AddError("Error..")
    arcpy.AddMessage(arcpy.GetMessages())