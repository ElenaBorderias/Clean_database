# Script recorded 28 Feb 2023, 13:13:29

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *

case = get_current("Case")
patient = get_current("Patient")


ct_list = ['pCT_tomo']
roi_names = [x.Name for x in case.PatientModel.RegionsOfInterest]
exam_names = [exam.Name for exam in case.Examinations]


for ct_name in ct_list:
    if ct_name in exam_names:
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
        




""" for ct_name in ct_list:
    if ct_name in exam_names:
        if 'CTV_T_LN' not in roi_names:
            retval_0 = case.PatientModel.CreateRoi(Name="CTV_T_LN", Color="SaddleBrown", Type="Ctv", TissueName=None, RbeCellTypeName=None, RoiMaterial=None)
            retval_0.CreateAlgebraGeometry(Examination=case.Examinations[ct_name], Algorithm="Auto", ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ["T"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ["LN"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })

        elif not case.PatientModel.StructureSets[ct_name].RoiGeometries['CTV_T_LN'].HasContours():
            case.PatientModel.RegionsOfInterest['CTV_T_LN'].CreateAlgebraGeometry(Examination=case.Examinations[ct_name], Algorithm="Auto", ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ["T"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ["LN"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })

        if 'LUNGS-GTV' not in roi_names: 
            retval_0 = case.PatientModel.CreateRoi(Name="LUNGS-GTV", Color="Orange", Type="Organ", TissueName=None, RbeCellTypeName=None, RoiMaterial=None)
            retval_0.CreateAlgebraGeometry(Examination=case.Examinations[ct_name], Algorithm="Auto", ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ["LUNG_L", "LUNG_R"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ["GTV T", "GTV LN"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
        
        elif not case.PatientModel.StructureSets[ct_name].RoiGeometries['LUNGS-GTV'].HasContours():
            case.PatientModel.RegionsOfInterest['LUNGS-GTV'].CreateAlgebraGeometry(Examination=case.Examinations[ct_name], Algorithm="Auto", ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ["LUNG_L", "LUNG_R"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ["GTV T", "GTV LN"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
 """