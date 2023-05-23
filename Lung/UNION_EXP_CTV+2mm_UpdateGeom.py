# Script recorded 23 May 2023, 13:17:45

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *

case = get_current("Case")
patient = get_current("Patient")

cts_to_update = ["MidP CT2","End_InH2","End_ExH2", "MidV CT2","MidP CT3","End_InH3","End_ExH3", "MidV CT3"]

with CompositeAction('Expand (UNION_EXP, Image set: MidP CT2)'):

  retval_0 = case.PatientModel.RegionsOfInterest['UNION_EXP'].SetMarginExpression(SourceRoiName="CTV_T_LN", 
                                                                                  MarginSettings={ 'Type': "Expand", 'Superior': 0.47, 'Inferior': 0.47, 'Anterior': 0.32, 'Posterior': 0.32, 'Right': 0.29, 'Left': 0.29 })

  for ct_name in cts_to_update:
    retval_0.UpdateDerivedGeometry(Examination=case.Examinations[ct_name], Algorithm="Auto")
    case.PatientModel.UpdateDerivedGeometries(RoiNames=["CTV+2mm"], Examination=case.Examinations[ct_name], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

patient.Save()
