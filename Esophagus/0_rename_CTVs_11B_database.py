# Script recorded 28 Feb 2023, 13:13:29

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *
from Patients import Patient

def main():

  patient_list = []
  index_list = [42,43,44,45,46,47,48,49,50,51,53,54,55,59,60,63,65,52]
  print(index_list)

  for i in index_list:
    patient_list.append("0" + str(i) + "_Esophagus_AI_KUL")
  print(patient_list)

  for patient_name in patient_list:
    pat = Patient(patient_name)
    RS_Patient = pat.loadPatient()
    RS_Patient.Cases['Case 1'].SetCurrent() 

    patient = get_current("Patient")
    case_pCT = patient.Cases["Case 1"]

    if patient_name == "052_Esophagus_AI_KUL":
      case_rCT = patient.Cases["Repeated CT PT"]
    else:
      case_rCT = patient.Cases["Repeated CT"]

    pCT_name = "Average CT"
    rCT_name = "Average CT new"

    roi_names_pct = [x.OfRoi.Name for x in case_pCT.PatientModel.StructureSets[pCT_name].RoiGeometries]
    roi_names_rct = [x.OfRoi.Name for x in case_rCT.PatientModel.StructureSets[rCT_name].RoiGeometries]

    print("#############################################################################################################")
    print("Patient: ", patient.Name)
    #print("Roi names pCT:", roi_names_pct)
    #print("Roi names rCT:", roi_names_rct)

    if "MT_iCTV_5040" in roi_names_pct and "MT_iPTV_07_5040" in roi_names_pct and "MT_CTVt_5040" in roi_names_pct:
      print("All CTVs are good in planning CT")
    if "MT_iCTV_5040" not in roi_names_pct:
      print("MT_iCTV_5040 is missing in pCT")
    if "MT_iPTV_07_5040" not in roi_names_pct and "MT_iPTVt_07_4500" in roi_names_pct:
      case_pCT.PatientModel.RegionsOfInterest["MT_iPTVt_07_4500"].Name = "MT_iPTV_07_5040"
    if "MT_CTVt_5040" not in roi_names_pct:
      print("MT_CTVt_5040 is missing in pCT")

    if "MT_iCTV_5040" in roi_names_rct and "MT_iPTV_07_5040" in roi_names_rct and "MT_CTVt_5040" in roi_names_rct:
      print("All CTVs are good in repeated CT")
    if "MT_iCTV_5040" not in roi_names_rct:
      print("MT_iCTV_5040 is missing in repeated CT")
    if "MT_iPTV_07_5040" not in roi_names_rct:
      print("MT_iPTV_07_5040 is missing in repeated CT")
    if "MT_CTVt_5040" not in roi_names_rct:
      print("MT_CTVt_5040 is missing in repeated CT")

    rois_to_keep = ['MT_iCTV_5040', 'MT_iPTV_07_5040', 'MT_CTVt_5040',
                    "BODY", "MT_Fundus", "MT_LeftVentricle","MT_SpinalCan_03","MT_SpinalCanal",
                    "MT_Kidney_R","MT_Kidney_L","MT_Heart","MT_Lungs","MT_Liver"]
    
    if all(elem in rois_to_keep for elem in roi_names_pct):
      print("All rois are available in pCT")
    else:
      print("Some ROIS are missing, let's check")
      for roi in rois_to_keep:
        if roi not in roi_names_pct:
          print(roi, " is missing in the planning CT")

    if all(elem in rois_to_keep for elem in roi_names_rct):
      print("All rois are available in rCT")
    else: 
      print("Some ROIS are missing, let's check")
      for roi in rois_to_keep:
        if roi not in roi_names_rct:
          print(roi, " is missing in repeated CT")


    Im_keeping = []
    Im_deleting = []
    for roi in case_rCT.PatientModel.RegionsOfInterest:
      if roi.Name not in rois_to_keep:
        print("I will delete :", roi.Name)
        Im_deleting.append(roi.Name)
        roi.DeleteRoi()
      else:
        print("We keep ", roi.Name)
        Im_keeping.append(roi.Name)

    print("Number of items to keep: ", len(Im_keeping))
    print("Number of items to delete: ", len(Im_deleting))
    print("#############################################################################################################")
    #case.PatientModel.ToggleExcludeFromExport(ExcludeFromExport=True, RegionOfInterests=["CTVn_4500"], PointsOfInterests=[])
    patient.Save()

  
main()

# rois_to_change = [{'standard': 'GTV T', 'current': 'gtv t', 'type': 'Target'},
#                   {'standard': 'GTV LN', 'current': 'gtv ln','type': 'Target'},
#                   {'standard': 'T', 'current': 'ctv t', 'type': 'Target'},
#                   {'standard': 'LN', 'current': 'ctv ln','type': 'Target'},
#                   {'standard': 'LUNG_L', 'current': 'L lung','type': 'Organ at risk'},
#                   {'standard': 'LUNG_R', 'current': 'R lung','type': 'Organ at risk'},
#                   {'standard': 'HEART', 'current': 'Heart','type': 'Organ at risk'},
#                   {'standard': 'ESOPHAGUS', 'current': 'Esophagus','type': 'Organ at risk'},
#                   {'standard': 'SC', 'current': 'SC','type': 'Organ at risk'},
#                   {'standard': 'SC_PRV', 'current': 'PRV SC','type': 'Organ at risk'},
#                   {'standard': 'BODY', 'current': 'Body','type': 'External'},
#                   {'standard': 'LUNGS-GTV', 'current': 'Lungs-GTV','type': 'Organ at risk'},
#                   {'standard': 'BRONCHUS', 'current': 'Bronchus','type': 'Organ at risk'},
#                   {'standard': 'THYROID', 'current': 'Thyroid','type': 'Organ at risk'}]

# for roi in rois_to_change:
#   standard_rois.append(roi['standard'])

#   if roi['current'] in roi_names:
#     case.PatientModel.RegionsOfInterest[roi['current']].Name = roi['standard']
#     if roi['type'] == 'Organ at risk':
#       case.PatientModel.RegionsOfInterest[roi['standard']].OrganData.OrganType = "OrganAtRisk"
#     if roi['type'] == 'Target':
#       if roi['standard'].startswith('CTV') or roi['standard'] == 'T' or roi['standard'] == 'LN' :
#         case.PatientModel.RegionsOfInterest[roi['standard']].Type = "Ctv"
#         case.PatientModel.RegionsOfInterest[roi['standard']].OrganData.OrganType = "Target"

#       elif roi['standard'].startswith('GTV'):
#         case.PatientModel.RegionsOfInterest[roi['standard']].Type = "Gtv"
#         case.PatientModel.RegionsOfInterest[roi['standard']].OrganData.OrganType = "Target"

#       else:
#         print('Wrong target type')

# rois_to_delete = []     
# for roi_to_delete in rois_to_delete:

#   case.PatientModel.RegionsOfInterest[roi_to_delete].DeleteRoi()

# patient.Save()