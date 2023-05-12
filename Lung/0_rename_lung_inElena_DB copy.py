# Script recorded 28 Feb 2023, 13:13:29

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *

case = get_current("Case")
patient = get_current("Patient")

ct_name_to_rename = 'MidP CT 2'

standard_rois = []
roi_names = [x.OfRoi.Name for x in case.PatientModel.StructureSets[ct_name_to_rename].RoiGeometries]
exam_names = [exam.Name for exam in case.Examinations]

rois_to_change = [{'standard': 'GTV T', 'current': 'gtv t', 'type': 'Target'},
                  {'standard': 'GTV LN', 'current': 'gtv ln','type': 'Target'},
                  {'standard': 'T', 'current': 'ctv t', 'type': 'Target'},
                  {'standard': 'LN', 'current': 'ctv ln','type': 'Target'},
                  {'standard': 'LUNG_L', 'current': 'L lung','type': 'Organ at risk'},
                  {'standard': 'LUNG_R', 'current': 'R lung','type': 'Organ at risk'},
                  {'standard': 'HEART', 'current': 'Heart','type': 'Organ at risk'},
                  {'standard': 'ESOPHAGUS', 'current': 'Esophagus','type': 'Organ at risk'},
                  {'standard': 'SC', 'current': 'SC','type': 'Organ at risk'},
                  {'standard': 'SC_PRV', 'current': 'PRV SC','type': 'Organ at risk'},
                  {'standard': 'BODY', 'current': 'Body','type': 'External'},
                  {'standard': 'LUNGS-GTV', 'current': 'Lungs-GTV','type': 'Organ at risk'},
                  {'standard': 'BRONCHUS', 'current': 'Bronchus','type': 'Organ at risk'},
                  {'standard': 'THYROID', 'current': 'Thyroid','type': 'Organ at risk'}]

for roi in rois_to_change:
  standard_rois.append(roi['standard'])

  if roi['current'] in roi_names:
    case.PatientModel.RegionsOfInterest[roi['current']].Name = roi['standard']
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

patient.Save()

standard_rois.append(['CTV_T_LN','LUNGS-GTV'])
for roi in roi_names:
  if '_ref' in roi or 'Control' in roi or 'isodose' in roi or '->' in roi or '_dose' in roi or 'def ctv' in roi or 'def gtv' in roi or 'def GTV' in roi:
    try:
        case.PatientModel.RegionsOfInterest[roi].DeleteRoi()
    except:
       print('I could not delete this ROI ', roi)