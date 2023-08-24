# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:55:10 2023

@author: borderiasvil
"""
from connect import *
import math

patient = get_current("Patient")
case = get_current("Case")

struct_to_analyze = "CTV"
ct_group_name = "Phases" 

center_roi_x = []
center_roi_y = []
center_roi_z = []

# # Iterate over the CTs of the 4D CT group
list_exam_full = [x.Examination.Name for x in case.ExaminationGroups[ct_group_name].Items]

for phase_name in list_exam_full:
    # Calculate difference in CTV center based on each axis relative to the selected CT(exam_name)
    center_roi_x.append(case.PatientModel.StructureSets[phase_name].RoiGeometries[struct_to_analyze].GetCenterOfRoi().x)
    center_roi_y.append(case.PatientModel.StructureSets[phase_name].RoiGeometries[struct_to_analyze].GetCenterOfRoi().y)
    center_roi_z.append(case.PatientModel.StructureSets[phase_name].RoiGeometries[struct_to_analyze].GetCenterOfRoi().z)

# Calculate the maximum CTV center displacement amplitude relative to the mid-vent CT
amplitude_x = abs(max(center_roi_x) - min(center_roi_x))
amplitude_y = abs(max(center_roi_y) - min(center_roi_y))
amplitude_z = abs(max(center_roi_z) - min(center_roi_z))

print("Amplitude X: ", amplitude_x)
print("Amplitude Y: ", amplitude_y)
print("Amplitude Z: ", amplitude_z)