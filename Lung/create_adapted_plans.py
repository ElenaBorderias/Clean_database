# Script recorded 24 May 2023, 09:58:43

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *

case = get_current("Case")
plan = get_current("Plan")
beam_set = get_current("BeamSet")
examination = get_current("Examination")


# Unscriptable Action 'Save' Completed : SaveAction(...)

# Unscriptable Action 'Create alternative plan' Completed : CopyPlanToNewExaminationAction(...)

# Unscriptable Action 'Save' Completed : SaveAction(...)

plan.PlanOptimizations[0].OptimizationParameters.SaveRobustnessParameters(PositionUncertaintyAnterior=0.5, PositionUncertaintyPosterior=0.5, PositionUncertaintySuperior=0.5, PositionUncertaintyInferior=0.5, PositionUncertaintyLeft=0.5, PositionUncertaintyRight=0.5, DensityUncertainty=0.03, PositionUncertaintySetting="Universal", IndependentLeftRight=True, IndependentAnteriorPosterior=True, IndependentSuperiorInferior=True, ComputeExactScenarioDoses=False, NamesOfNonPlanningExaminations=["End_ExH2", "End_InH2", "MidV CT2"], PatientGeometryUncertaintyType="PerTreatmentCourse", PositionUncertaintyType="PerTreatmentCourse", TreatmentCourseScenariosFactor=1000, PositionUncertaintyList=None, PositionUncertaintyFormation="Automatic", RobustMethodPerTreatmentCourse="WeightedPowerMean")

plan.PlanOptimizations[0].ResetOptimization()

plan.PlanOptimizations[0].RunOptimization(ScalingOfSoftMachineConstraints=None)

with CompositeAction('Update derived geometries (ring-1cm, Image set: CT 12 - PET, End_InH, CT 2, CT 3, CT 4, CT 5, CT 6, CT 7, End_ExH, CT 9, MidV CT, CT 13 - Average, CT 11 - MidP, pCT_tomo, MidP CT2, MidP CT3, CT 1, CT 8, CT 10, CT 11, CT 12, CT 13, CT 14, End_ExH2, End_InH2, MidV CT2, CT 15, CT 16, CT 17, CT 18, CT 19, CT 20, End_ExH3, End_InH3, MidV CT3)'):

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 12 - PET'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['End_InH'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 2'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 3'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 4'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 5'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 6'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 7'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['End_ExH'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 9'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['MidV CT'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 13 - Average'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 11 - MidP'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['pCT_tomo'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=examination, Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['MidP CT3'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 1'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 8'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 10'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 11'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 12'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 13'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 14'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['End_ExH2'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['End_InH2'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['MidV CT2'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 15'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 16'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 17'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 18'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 19'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['CT 20'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['End_ExH3'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['End_InH3'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  case.PatientModel.UpdateDerivedGeometries(RoiNames=["ring-1cm"], Examination=case.Examinations['MidV CT3'], Algorithm="Auto", AreEmptyDependenciesAllowed=False)

  # CompositeAction ends 


plan.PlanOptimizations[0].RunOptimization(ScalingOfSoftMachineConstraints=None)

with CompositeAction('Edit plan'):

  with CompositeAction('Add new beam set'):

    # CompositeAction ends 


  with CompositeAction('Set beam set dependencies'):

    # CompositeAction ends 


  with CompositeAction('Set prescription'):

    # CompositeAction ends 


  # Unscriptable Action 'Edit plan' Completed : SaveEditedPlanAndTreatmentSetupCompositeAction(...)

  # CompositeAction ends 


beam_set.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="IonMonteCarlo", ForceRecompute=False, RunEntryValidation=True)

beam_set.SetAutoScaleToPrimaryPrescription(AutoScale=True)

# Unscriptable Action 'Save' Completed : SaveAction(...)
