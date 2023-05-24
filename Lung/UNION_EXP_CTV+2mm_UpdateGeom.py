# Script recorded 23 May 2023, 13:17:45

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *

case = get_current("Case")
patient = get_current("Patient")

cts_to_update = ["MidP CT2","End_InH2","End_ExH2", "MidV CT2","MidP CT3","End_InH3","End_ExH3", "MidV CT3"]

roi_names = [x.OfRoi.Name for x in case.PatientModel.StructureSets["CT 11 - MidP"].RoiGeometries]

if "CTV_T_LN" in roi_names and "CTV" not in roi_names:
  with CompositeAction('Expand (UNION_EXP, Image set: MidP CT2)'):

    retval_0 = case.PatientModel.RegionsOfInterest['UNION_EXP'].SetMarginExpression(SourceRoiName="CTV_T_LN", 
                                                                                    MarginSettings={ 'Type': "Expand", 'Superior': 0.47, 'Inferior': 0.47, 'Anterior': 0.32, 'Posterior': 0.32, 'Right': 0.29, 'Left': 0.29 })

    for ct_name in cts_to_update:
      retval_0.UpdateDerivedGeometry(Examination=case.Examinations[ct_name], Algorithm="Auto")
      case.PatientModel.UpdateDerivedGeometries(RoiNames=["CTV+2mm"], Examination=case.Examinations[ct_name], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  patient.Save()

if "CTV" in roi_names and "CTV_T_LN" not in roi_names:
  with CompositeAction('Expand (UNION_EXP, Image set: MidP CT2)'):

    retval_0 = case.PatientModel.RegionsOfInterest['EXP'].SetMarginExpression(SourceRoiName="CTV", 
                                                                                    MarginSettings={ 'Type': "Expand", 'Superior': 0.47, 'Inferior': 0.47, 'Anterior': 0.32, 'Posterior': 0.32, 'Right': 0.27, 'Left': 0.27 })

    for ct_name in cts_to_update:
      retval_0.UpdateDerivedGeometry(Examination=case.Examinations[ct_name], Algorithm="Auto")
      case.PatientModel.UpdateDerivedGeometries(RoiNames=["CTV+2mm"], Examination=case.Examinations[ct_name], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  patient.Save()