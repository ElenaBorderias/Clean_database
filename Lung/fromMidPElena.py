# Script recorded 28 Feb 2023, 13:13:29

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *

case = get_current("Case")
patient = get_current("Patient")

pairs = [{'midpreal': 'MidPCT3 real', 'midpElena': 'MidPCT3 Elena'},{'midpreal': 'MidPCT2 real', 'midpElena': 'MidPCT2 Elena'} ]
rois_to_map = ["LUNG_R", "LUNG_L", "SC", "SC_PRV", "GTV T", "GTV LN", "ESOPHAGUS", "HEART", "T", "LN"]
roi_names = [x.Name for x in case.PatientModel.RegionsOfInterest]
if "GTV LN" not in roi_names:
  rois_to_map = ["LUNG_R", "LUNG_L", "BRONCHUS", "SC", "SC_PRV", "GTV T", "THYROID", "ESOPHAGUS", "HEART", "T"]

index = 1
for p in pairs:
  print()
  registration_group_name = "HybridDefReg_" + str(index)
  case.PatientModel.CreateHybridDeformableRegistrationGroup(RegistrationGroupName=registration_group_name, ReferenceExaminationName= p['midpElena'], TargetExaminationNames=[p['midpreal']], ControllingRoiNames=[], ControllingPoiNames=[], FocusRoiNames=[], AlgorithmSettings={ 'NumberOfResolutionLevels': 3, 'InitialResolution': { 'x': 0.5, 'y': 0.5, 'z': 0.5 }, 'FinalResolution': { 'x': 0.25, 'y': 0.25, 'z': 0.25 }, 'InitialGaussianSmoothingSigma': 2, 'FinalGaussianSmoothingSigma': 0.333333333333333, 'InitialGridRegularizationWeight': 400, 'FinalGridRegularizationWeight': 400, 'ControllingRoiWeight': 0.5, 'ControllingPoiWeight': 0.1, 'MaxNumberOfIterationsPerResolutionLevel': 1000, 'ImageSimilarityMeasure': "CorrelationCoefficient", 'DeformationStrategy': "Default", 'ConvergenceTolerance': 1E-05 })
  case.MapRoiGeometriesDeformably(RoiGeometryNames=rois_to_map, 
                                  CreateNewRois=False,
                                  StructureRegistrationGroupNames = [registration_group_name],
                                  ReferenceExaminationNames = [p['midpElena']],
                                  TargetExaminationNames = [p['midpreal']])
  index = index+1