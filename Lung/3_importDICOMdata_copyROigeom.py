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
#index_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
index_list = [3]
print(index_list)

for i in index_list:

    patient_name = "LUNG_UCL" + str(i)
    pat = Patient(patient_name)
    RS_Patient = pat.loadPatient()
    RS_Patient.Cases["Case 1"].SetCurrent() 

    patient = get_current("Patient")
    case = get_current("Case")
    clinic_db = get_current('ClinicDB')
    patient_name_folder = "FDG^Lung"+str(i)+"_1"
    patient_path = os.path.join("Y:\Elena\Clean_data_Dario",patient_name_folder)
    rcts = ["2","3"]
    for rct in rcts:
        phases = os.listdir(os.path.join(patient_path,rct))
        phases_ct_names = []

        for phase in phases:
            phase_path = os.path.join(patient_path,phase)

            #I will import all phases except for the MidP

            if not phase.startswith("MidP"):
                # Import CT 
                # get the first slice
                first_ct_slice = os.listdir(phase_path)[0]
                print(first_ct_slice)
                dcm = pydicom.read_file(os.path.join(phase_path,first_ct_slice))
                print(dcm.PatientID)
                #print(dcm.StudyInstanceUID.dtpye)
                print(dcm.StudyInstanceUID)
                #print(dcm.SeriesInstanceUID.dtype)
                print(dcm.SeriesInstanceUID)
                info_ct = {'PatientID': dcm.PatientID, 'StudyInstanceUID': str(dcm.StudyInstanceUID), 'SeriesInstanceUID': str(dcm.SeriesInstanceUID)}
                patient.ImportDataFromPath(Path=phase_path, CaseName=case.CaseName,SeriesOrInstances=[info_ct])

                #Import RTSTRUCT
                # list all the files in the directory
                files = os.listdir(phase_path)

                # iterate through the files and find the file starting with "RS"
                for file in files:
                    if file.startswith("RS"):
                        print(f"The RTSTRUCT file starting with 'RS' is: {file}")
                        rt_structut_file = file
                        break
                else:
                    print("No file starting with 'RS' found.")
                
                rt_struct_path = os.path.join(phase_path,rt_structut_file)
                RT_dcm = pydicom.read_file(rt_struct_path)
                info_rtstruct = {'PatientID': RT_dcm.PatientID, 'StudyInstanceUID': str(RT_dcm.StudyInstanceUID), 'SeriesInstanceUID': str(RT_dcm.SeriesInstanceUID)}
                patient.ImportDataFromPath(Path=phase_path, CaseName=case.CaseName,SeriesOrInstances=[info_rtstruct])

                #Get CT name
                examination_index = case.Examinations.Count - 1
                imported_phase_name = case.Examinations[examination_index].Name
                phases_ct_names.append(imported_phase_name)
                case.Examinations[imported_phase_name].EquipmentInfo.SetImagingSystemReference(ImagingSystemName="UCL Toshiba")

                #Copy structures
                roi_names = [x.Name for x in case.PatientModel.RegionsOfInterest]
                for roi in roi_names:
                    if '(1)' in roi:
                        real_roi = roi[:-4]
                        roi_to_copy = roi
                        print(real_roi)
                        print(roi_to_copy)

                        if not case.PatientModel.StructureSets[imported_phase_name].RoiGeometries[real_roi].HasContours():
                            case.PatientModel.StructureSets[imported_phase_name].CopyRoiGeometryToAnotherRoi(FromRoi=roi_to_copy,ToRoi=real_roi)
                            case.PatientModel.RegionsOfInterest[roi_to_copy].DeleteRoi()
                        else:
                            print('This roi already exists in your CT')

        #Once we have all phases (CT and contours) - we create a CT group
        patient.Save()
