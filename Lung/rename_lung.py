# Script recorded 28 Feb 2023, 13:13:29

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *

case = get_current("Case")
patient = get_current("Patient")


roi_names = [x.OfRoi.Name for x in case.PatientModel.StructureSets['CT 1'].RoiGeometries]
rois_to_change = [{'standard': 'GTV T', 'current': 'GTV T', 'type': 'Target'},
                  {'standard': 'GTV LN', 'current': 'GTV LN','type': 'Target'},
                  {'standard': 'T', 'current': 'CTV T 5mm', 'type': 'Target'},
                  {'standard': 'LN', 'current': 'CTV LN 5mm','type': 'Target'},
                  {'standard': 'LUNG_L', 'current': 'L lung','type': 'Organ at risk'},
                  {'standard': 'LUNG_R', 'current': 'R lung','type': 'Organ at risk'},
                  {'standard': 'HEART', 'current': 'Heart','type': 'Organ at risk'},
                  {'standard': 'ESOPHAGUS', 'current': 'Esophagus','type': 'Organ at risk'},
                  {'standard': 'SC', 'current': 'spinal cord','type': 'Organ at risk'},
                  {'standard': 'SC_PRV', 'current': 'PRV SC','type': 'Organ at risk'},
                  {'standard': 'BODY', 'current': 'Body','type': 'External'},
                  {'standard': 'LUNGS-GTV', 'current': 'Lungs-GTV','type': 'Organ at risk'},
                  {'standard': 'BRONCHUS', 'current': 'Bronchus','type': 'Organ at risk'},
                  {'standard': 'THYROID', 'current': 'Thyroid','type': 'Organ at risk'}]

for roi in rois_to_change:

  if roi['current'] in roi_names:
    case.PatientModel.RegionsOfInterest[roi['current']].Name = roi['standard']
    patient.Save()
    if roi['type'] == 'Organ at risk':
      case.PatientModel.RegionsOfInterest[roi['standard']].OrganData.OrganType = "OrganAtRisk"
    if roi['type'] == 'Target':
      if roi['standard'].startswith('CTV') or roi['standard'] == 'T' or roi['standard'] == 'LN' :
        case.PatientModel.RegionsOfInterest[roi['standard']].Type = "Ctv"
        case.PatientModel.RegionsOfInterest[roi['standard']].OrganData.OrganType = "Target"

      elif roi['standard'].startswith('GTV'):
        case.PatientModel.RegionsOfInterest[roi['standard']].Type = "Gtv"
        case.PatientModel.RegionsOfInterest[roi['standard']].OrganData.OrganType = "Target"

      else:
        print('Wrong target type')

rois_to_delete = []     
for roi_to_delete in rois_to_delete:

  case.PatientModel.RegionsOfInterest[roi_to_delete].DeleteRoi()

  # CompositeAction ends 
ct_list = ['CT 1', 'CT 2']
for ct_name in ct_list:

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


