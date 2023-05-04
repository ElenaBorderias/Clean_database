# Script recorded 28 Feb 2023, 13:13:29

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *

case = get_current("Case")
patient = get_current("Patient")


ct_group_list = ['Phases 1','Phases 2','Phases 3']
roi_names = [x.Name for x in case.PatientModel.RegionsOfInterest]


for ct_group in ct_group_list:
    phases = [item.Examination.Name for item in case.ExaminationGroups[ct_group].Items]
    for ct_name in phases:
        for roi in case.PatientModel.StructureSets[ct_name].RoiGeometries:
            current_roi = roi.OfRoi.Name

            if 'def ctv ln' in roi.OfRoi.Name and roi.HasContours():
                roi_to_copy_to = 'LN'
                #make sure we do not override existing structures
                if not case.PatientModel.StructureSets[ct_name].RoiGeometries[roi_to_copy_to].HasContours():
                    case.PatientModel.StructureSets[ct_name].CopyRoiGeometryToAnotherRoi(FromRoi=current_roi,ToRoi=roi_to_copy_to)

            elif 'def ctv t' in roi.OfRoi.Name and roi.HasContours():
                roi_to_copy_to = 'T'
                #make sure we do not override existing structures
                if not case.PatientModel.StructureSets[ct_name].RoiGeometries[roi_to_copy_to].HasContours():
                    case.PatientModel.StructureSets[ct_name].CopyRoiGeometryToAnotherRoi(FromRoi=current_roi,ToRoi=roi_to_copy_to)

            elif 'def GTVp' in roi.OfRoi.Name and roi.HasContours():
                roi_to_copy_to = 'GTV T'
                #make sure we do not override existing structures
                if not case.PatientModel.StructureSets[ct_name].RoiGeometries[roi_to_copy_to].HasContours():
                    case.PatientModel.StructureSets[ct_name].CopyRoiGeometryToAnotherRoi(FromRoi=current_roi,ToRoi=roi_to_copy_to)

            elif 'def GTVn' in roi.OfRoi.Name and roi.HasContours():
                roi_to_copy_to = 'GTV LN'
                #make sure we do not override existing structures
                if not case.PatientModel.StructureSets[ct_name].RoiGeometries[roi_to_copy_to].HasContours():
                    case.PatientModel.StructureSets[ct_name].CopyRoiGeometryToAnotherRoi(FromRoi=current_roi,ToRoi=roi_to_copy_to)
            
            else:
                print('This roi is not in phases', current_roi)
        