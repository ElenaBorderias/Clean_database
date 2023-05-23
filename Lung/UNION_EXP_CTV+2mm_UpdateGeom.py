# Script recorded 23 May 2023, 13:17:45

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *

case = get_current("Case")
examination = get_current("Examination")


with CompositeAction('Expand (UNION_EXP, Image set: MidP CT2)'):

  retval_0 = case.PatientModel.RegionsOfInterest['UNION_EXP'].SetMarginExpression(SourceRoiName="CTV_T_LN", MarginSettings={ 'Type': "Expand", 'Superior': 0.47, 'Inferior': 0.47, 'Anterior': 0.32, 'Posterior': 0.32, 'Right': 0.29, 'Left': 0.29 })

  retval_0.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

  # CompositeAction ends 


with CompositeAction('Update derived geometry (UNION_EXP, Image set: MidP CT3)'):

  retval_0.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

  # CompositeAction ends 

