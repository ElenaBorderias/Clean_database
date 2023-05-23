# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:55:10 2023

@author: borderiasvil
"""
from connect import *
import math


def create_MidV_EndInHale_EndExHale(list_exam_full, struct_to_analyze, index):
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
    # Initialize the variable chosen_ct as being the CT allowing the initialization of the minimum variable
    #rms = min(rms_list[6:])
    rms = min(rms_list)
    print("rms : ", rms)
    print(rms_list)

    chosen_scan_id = rms_list.index(rms)

    chosen_ct = list_exam_full[chosen_scan_id]
    print("The determined real midV CT phase is:" + chosen_ct)
    print("coord. mid. V: x = ", center_roi_x[chosen_scan_id], " ,y = ", center_roi_y[chosen_scan_id], " ,z = ",
          center_roi_z[chosen_scan_id])

    # # Initialize 3 lists
    # distance_x = []
    # distance_y = []
    # distance_z = []
    # # Iterate over the CTs of the 4D CT group
    # for i in range(0, len(list_exam_full)):
    #     # Add to each list the distance between the CTV center of the mid vent CT and the considered CT
    #     distance_x.append(center_roi_x[chosen_scan_id] - center_roi_x[i])
    #     distance_y.append(center_roi_y[chosen_scan_id] - center_roi_y[i])
    #     distance_z.append(center_roi_z[chosen_scan_id] - center_roi_z[i])
    # # Calculate the maximum CTV center displacement amplitude relative to the mid-vent CT
    # amplitude_x = abs(max(distance_x) - min(distance_x))
    # amplitude_y = abs(max(distance_y) - min(distance_y))
    # amplitude_z = abs(max(distance_z) - min(distance_z))

    print(center_roi_z)

    end_inhale = max(center_roi_z)
    end_exhale = min(center_roi_z)

    inhale_scan_id = center_roi_z.index(end_inhale)
    exhale_scan_id = center_roi_z.index(end_exhale)

    inhale_ct = list_exam_full[inhale_scan_id]
    exhale_ct = list_exam_full[exhale_scan_id]

    if chosen_ct == exhale_ct or chosen_ct == inhale_ct:
        rms = min(rms_list)
        print("rms : ", rms)
        print(rms_list)

        chosen_scan_id = rms_list.index(rms)
        chosen_ct = list_exam_full[chosen_scan_id]

    case.Examinations[chosen_ct].Name = 'MidV CT' + index
    case.Examinations[exhale_ct].Name = 'End_InH' + index
    case.Examinations[inhale_ct].Name = 'End_ExH' + index

    return 'MidV CT' + index, 'End_InH' + index, 'End_ExH' + index

################################################## MAIN ##############################################################


case = get_current("Case")
ctv_name = "CTV_T_LN"
#case.PatientModel.RegionsOfInterest['CTV(T+LN)'].Name = ctv_name
phases_groups = ["Phases2"]


for ct_group in phases_groups:
    index = ct_group[-1]
    ct_ref = "MidP CT "+index
    ct_phases_raw = [x.Examination.Name for x in case.ExaminationGroups[ct_group].Items]
    """
    case.PatientModel.CreateHybridDeformableRegistrationGroup(RegistrationGroupName="HybridDefReg_CT" + index,
                                                              ReferenceExaminationName=ct_ref,
                                                              TargetExaminationNames=ct_phases_raw,
                                                              ControllingRoiNames=[], ControllingPoiNames=[],
                                                              FocusRoiNames=[],
                                                              AlgorithmSettings={'NumberOfResolutionLevels': 3, 'InitialResolution': {'x': 0.5, 'y': 0.5, 'z': 0.5}, 'FinalResolution': {'x': 0.25, 'y': 0.25, 'z': 0.25}, 'InitialGaussianSmoothingSigma': 2, 'FinalGaussianSmoothingSigma': 0.333333333333333, 'InitialGridRegularizationWeight': 400, 'FinalGridRegularizationWeight': 400, 'ControllingRoiWeight': 0.5, 'ControllingPoiWeight': 0.1, 'MaxNumberOfIterationsPerResolutionLevel': 1000, 'ImageSimilarityMeasure': "CorrelationCoefficient", 'DeformationStrategy': "Default", 'ConvergenceTolerance': 1E-05})
    """
    case.MapRoiGeometriesDeformably(RoiGeometryNames=[ctv_name],
                                    CreateNewRois=False,
                                    StructureRegistrationGroupNames=[
                                        "HybridDefReg_CT" + index]*len(ct_phases_raw),
                                    ReferenceExaminationNames=[
                                        ct_ref]*len(ct_phases_raw),
                                    TargetExaminationNames=ct_phases_raw,
                                    ReverseMapping=False,
                                    AbortWhenBadDisplacementField=False)

    MidV, EndInH, EndExH = create_MidV_EndInHale_EndExHale(
        ct_phases_raw, ctv_name, index)
    print('I renamed the cts to: ', MidV, EndInH, EndExH)

    ct_phases_renamed = [
        x.Examination.Name for x in case.ExaminationGroups[ct_group].Items]
    all_rois = [
        x.OfRoi.Name for x in case.PatientModel.StructureSets[ct_ref].RoiGeometries]
    if 'CTV(T+LN)_ref' in all_rois:
        all_rois.remove('CTV(T+LN)_ref')
    if 'BODY' in all_rois:
        all_rois.remove('BODY')
    case.MapRoiGeometriesDeformably(RoiGeometryNames=all_rois,
                                    CreateNewRois=False,
                                    StructureRegistrationGroupNames=[
                                        "HybridDefReg_CT" + index]*len(ct_phases_raw),
                                    ReferenceExaminationNames=[
                                        ct_ref]*len(ct_phases_raw),
                                    TargetExaminationNames=ct_phases_renamed,
                                    ReverseMapping=False,
                                    AbortWhenBadDisplacementField=False)

    for ct in ct_phases_renamed:
        if not case.PatientModel.StructureSets[ct].RoiGeometries["BODY"].HasContours():
            case.PatientModel.RegionsOfInterest['BODY'].CreateExternalGeometry(
                Examination=case.Examinations[ct], ThresholdLevel=-250)
