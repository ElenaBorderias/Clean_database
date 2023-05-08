# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:55:10 2023

@author: borderiasvil
"""
from connect import *
from Patients import Patient
import json
import os
import pydicom

def log_warning(error):
    """ Example on how to read the JSON error string."""

    try:
        json_errors = json.loads(str(error))
        # If the json.loads() works then the script was stopped due to
        # a non-blocking warning.
        print('WARNING! Export Aborted!')
        print('Comment:')
        print(json_errors['Comment'])
        print('Warnings:')

        # Here the user can handle the warnings. Continue on known warnings,
        # stop on unknown warnings.
        for warning in json_errors['Warnings']:
            print(warning)
    except ValueError:
        # The error was likely due to a blocking warning, and the details should be stated in the execution log. 
        print('Error occurred. Could not export.')

def log_completed(result):
    """ This prints the successful result log in an ordered way. """

    try:
        json_result = json.loads(result)
        print('Completed!')
        print('Comment:')
        print(json_result['Comment'])
        print('Warnings:')
        for warning in json_result['Warnings']:
            print(warning)
        print('Export notifications:')
        # Export notifications is a list of notifications that the user should read.
        for notification in json_result['Notifications']:
            print(notification)
    except ValueError:
        print('Error reading completion messages.')

patient_list = []
#index_list = [42,43,44,45,46,47,48,49,50,51,53,54,55,59,60,63,65,52]
index_list = [43,44,45,46,47,48,49,50,51,53,54,55,59,60,63,65,52]
print(index_list)

for i in index_list:
    patient_list.append("0" + str(i) + "_Esophagus_AI_KUL")
print(patient_list)

for patient_name in patient_list:
    pat = Patient(patient_name)
    RS_Patient = pat.loadPatient()
    RS_Patient.Cases["Case 1"].SetCurrent() 

    patient = get_current("Patient")
    case = get_current("Case")
    clinic_db = get_current('ClinicDB')
    patient_path = os.path.join("C:\\Repeated_cts_eso",patient.Name)

    # Import CT 
    # get the first slice
    first_ct_slice = os.listdir(os.path.join(patient_path,"Average CT new"))[0]
    print(first_ct_slice)
    dcm = pydicom.read_file(os.path.join(patient_path,"Average CT new",first_ct_slice))
    print(dcm.PatientID)
    #print(dcm.StudyInstanceUID.dtpye)
    print(dcm.StudyInstanceUID)
    #print(dcm.SeriesInstanceUID.dtype)
    print(dcm.SeriesInstanceUID)
    info_ct = {'PatientID': dcm.PatientID, 'StudyInstanceUID': str(dcm.StudyInstanceUID), 'SeriesInstanceUID': str(dcm.SeriesInstanceUID)}
    patient.ImportDataFromPath(Path=os.path.join(patient_path,"Average CT new"), CaseName=case.CaseName,SeriesOrInstances=[info_ct])

    #Import RTSTRUCT
    # list all the files in the directory
    files = os.listdir(os.path.join(patient_path,"Average CT new"))

    # iterate through the files and find the file starting with "RS"
    for file in files:
        if file.startswith("RS"):
            print(f"The RTSTRUCT file starting with 'RS' is: {file}")
            rt_structut_file = file
            break
    else:
        print("No file starting with 'RS' found.")
    
    rt_struct_path = os.path.join(patient_path,"Average CT new",rt_structut_file)
    RT_dcm = pydicom.read_file(rt_struct_path)
    info_rtstruct = {'PatientID': RT_dcm.PatientID, 'StudyInstanceUID': str(RT_dcm.StudyInstanceUID), 'SeriesInstanceUID': str(RT_dcm.SeriesInstanceUID)}
    patient.ImportDataFromPath(Path=os.path.join(patient_path,"Average CT new"), CaseName=case.CaseName,SeriesOrInstances=[info_rtstruct])

    #Rename CT
    examination_index = case.Examinations.Count - 1
    ct_name = "Repeated Avg CT"
    case.Examinations[examination_index].Name = ct_name
    case.Examinations[ct_name].EquipmentInfo.SetImagingSystemReference(ImagingSystemName="UCL Toshiba")

    #Copy structures
    roi_names = [x.Name for x in case.PatientModel.RegionsOfInterest]
    for roi in roi_names:
        if '(1)' in roi:
            real_roi = roi[:-4]
            roi_to_copy = roi
            print(real_roi)
            print(roi_to_copy)

            if not case.PatientModel.StructureSets[ct_name].RoiGeometries[real_roi].HasContours():
                case.PatientModel.StructureSets[ct_name].CopyRoiGeometryToAnotherRoi(FromRoi=roi_to_copy,ToRoi=real_roi)
                case.PatientModel.RegionsOfInterest[roi_to_copy].DeleteRoi()
            else:
                print('This roi already exists in your CT')

    patient.Save()
