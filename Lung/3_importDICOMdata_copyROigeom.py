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

patient_list = []
#index_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
index_list = [3]
print(index_list)

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

def create_MidV_EndInHale_EndExHale(phases_group_name, struct_to_analyze, index):

    list_exam_full = [x.Examination.Name for x in case.ExaminationGroups[phases_group_name].Items]
    # We calculate the real Mid-position, the Mid-ventilation CT, the GTV movement around the Mid-ventilation CTV
    # Initialize 3 list (one per direction x, y, z) to contain CTV center of each CT from the 4D setT
    center_roi_x = []
    center_roi_y = []
    center_roi_z = []
    # Iterate over the list content
    print("Getting the center-coordinates of the CTV on all the phases")
    for i in list_exam_full:
        # Calculate difference in CTV center based on each axis relative to the selected CT(exam_name)
        center_roi_x.append(case.PatientModel.StructureSets[str(
            i)].RoiGeometries[struct_to_analyze].GetCenterOfRoi().x)
        center_roi_y.append(case.PatientModel.StructureSets[str(
            i)].RoiGeometries[struct_to_analyze].GetCenterOfRoi().y)
        center_roi_z.append(case.PatientModel.StructureSets[str(
            i)].RoiGeometries[struct_to_analyze].GetCenterOfRoi().z)
    # Calculate the average of CTV center displacement according to each axis
    mean_x = sum(center_roi_x) / len(center_roi_x)
    mean_y = sum(center_roi_y) / len(center_roi_y)
    mean_z = sum(center_roi_z) / len(center_roi_z)
    print("coord. mid. P: x = ", mean_x, " ,y = ", mean_y, " ,z = ", mean_z)
    # Calculate the root mean square of the CTV in the selected CT(exam_name) relative the mean calculate over each axis
    # Use the minimum value as starting point to find the smallest value in CTV center displacement from the mid-position
    rms_list = []
    for center_idx in range(0, len(center_roi_x)):
        rms_list.append(math.sqrt(
            ((center_roi_x[center_idx] - mean_x) ** 2) + ((center_roi_y[center_idx] - mean_y) ** 2) + (
                (center_roi_z[center_idx] - mean_z) ** 2)))
    # Initialize the variable midV_ct as being the CT allowing the initialization of the minimum variable
    rms = min(rms_list[6:])
    print("rms : ", rms)
    print(rms_list)

    midV_scan_id = rms_list.index(rms)

    midV_ct = list_exam_full[midV_scan_id]
    print("The determined real midV CT phase is:" + midV_ct)
    print("coord. mid. V: x = ", center_roi_x[midV_scan_id], " ,y = ", center_roi_y[midV_scan_id], " ,z = ",
          center_roi_z[midV_scan_id])

    print(center_roi_z)

    end_inhale = max(center_roi_z)
    end_exhale = min(center_roi_z)

    inhale_scan_id = center_roi_z.index(end_inhale)
    exhale_scan_id = center_roi_z.index(end_exhale)

    inhale_ct = list_exam_full[inhale_scan_id]
    exhale_ct = list_exam_full[exhale_scan_id]

    if midV_ct == exhale_ct or midV_ct == inhale_ct:
        rms = min(rms_list)
        print("rms : ", rms)
        print(rms_list)

        midV_scan_id = rms_list.index(rms)
        midV_ct = list_exam_full[midV_scan_id]

    case.Examinations[midV_ct].Name = 'MidV CT' + index
    case.Examinations[exhale_ct].Name = 'End_InH' + index
    case.Examinations[inhale_ct].Name = 'End_ExH' + index

    return 'MidV CT' + index, 'End_InH' + index, 'End_ExH' + index

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
        print("Here are the phases: ", phases)
        phases_ct_names = []

        for phase in phases:
            phase_path = os.path.join(patient_path,rct,phase)

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
                patient.ImportDataFromPath(Path=phase_path, CaseName=case.CaseName,SeriesOrInstances=[info_ct],AllowMismatchingPatientID=True)
                patient.Save()

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
                patient.ImportDataFromPath(Path=phase_path, CaseName=case.CaseName,SeriesOrInstances=[info_rtstruct],AllowMismatchingPatientID=True)

                #Get CT name
                examination_index = case.Examinations.Count - 1
                imported_phase_name = case.Examinations[examination_index].Name
                phases_ct_names.append(imported_phase_name)
                case.Examinations[imported_phase_name].EquipmentInfo.SetImagingSystemReference(ImagingSystemName="UCL Toshiba")
                patient.Save()

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
                patient.Save()

            case.CreateExaminationGroup(ExaminationGroupName="Phases "+str(rct), 
                                        ExaminationGroupType="Collection4dct", 
                                        ExaminationNames=[phases_ct_names])
            
            struct_to_analyze = "CTV_T_LN"
            phases_group_name = "Phases "+str(rct)
            create_MidV_EndInHale_EndExHale(phases_group_name, struct_to_analyze, rct)

        #Once we have all phases (CT and contours) - we create a CT group
        patient.Save()
