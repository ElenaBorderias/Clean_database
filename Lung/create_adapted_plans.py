# Script recorded 24 May 2023, 09:58:43

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *

case = get_current("Case")
patient = get_current("Patient")

reference_plans_names = ["IMPT","IMPT_4mm3%","IMPT_2mm3%"]
cts_to_adapt = ["MidP CT2","MidP CT3"]

all_plan_names = [x.Name for x in case.TreatmentPlans]

#Create alternative plan
for plan_name in reference_plans_names:
  for ct_name in cts_to_adapt:
    new_plan_name = plan_name+"_"+ct_name[-3:]
    
    if new_plan_name not in all_plan_names:
      print("######### Generating new adapted plan : ", new_plan_name, "############")
      case.TreatmentPlans[plan_name].CreateAlternativePlan(PlanName=new_plan_name, ExaminationName=ct_name)

      #read reference robust optimization parameters
      if plan_name == "IMPT":
        setup_error = 0.5
      else:
        setup_error = 0.2

      index = ct_name[-1]

      adapted_plan = case.TreatmentPlans[new_plan_name]
      adapted_plan.PlanOptimizations[0].OptimizationParameters.SaveRobustnessParameters(PositionUncertaintyAnterior=setup_error, 
                                                                                PositionUncertaintyPosterior=setup_error, 
                                                                                PositionUncertaintySuperior=setup_error, 
                                                                                PositionUncertaintyInferior=setup_error,
                                                                                PositionUncertaintyLeft=setup_error, 
                                                                                PositionUncertaintyRight=setup_error, 
                                                                                DensityUncertainty=0.03, 
                                                                                PositionUncertaintySetting="Universal", 
                                                                                IndependentLeftRight=True, 
                                                                                IndependentAnteriorPosterior=True, 
                                                                                IndependentSuperiorInferior=True, 
                                                                                ComputeExactScenarioDoses=False, 
                                                                                NamesOfNonPlanningExaminations=["End_ExH"+index, "End_InH"+index, "MidV CT"+index], 
                                                                                PatientGeometryUncertaintyType="PerTreatmentCourse", 
                                                                                PositionUncertaintyType="PerTreatmentCourse", 
                                                                                TreatmentCourseScenariosFactor=1000, 
                                                                                PositionUncertaintyList=None, 
                                                                                PositionUncertaintyFormation="Automatic", 
                                                                                RobustMethodPerTreatmentCourse="WeightedPowerMean")

      adapted_plan.PlanOptimizations[0].ResetOptimization()
      adapted_plan.PlanOptimizations[0].RunOptimization(ScalingOfSoftMachineConstraints=None)
      adapted_plan.BeamSets[0].DicomPlanLabel = new_plan_name

      adapted_plan.BeamSets[0].ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="IonMonteCarlo", ForceRecompute=False, RunEntryValidation=True)

      adapted_plan.BeamSets[0].SetAutoScaleToPrimaryPrescription(AutoScale=True)
      patient.Save()
