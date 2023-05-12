# Script recorded 28 Feb 2023, 13:13:29

#   RayStation version: 13.10.0.7342
#   Selected patient: ...

from connect import *

case = get_current("Case")
patient = get_current("Patient")

ct_name= 'CT 1'

roi_names = [x.OfRoi.Name for x in case.PatientModel.StructureSets[ct_name].RoiGeometries]

for roi in roi_names:
  if 'isodose' in roi or 'iso_np' in roi or 'iso_p_np' in roi:
    try:
        case.PatientModel.RegionsOfInterest[roi].DeleteRoi()
    except:
       print('I could not delete this ROI ', roi)

patient.Save()