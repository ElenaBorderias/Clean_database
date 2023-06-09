import json
from multiprocessing.sharedctypes import Value

from connect import get_current


class Patient:
    def __init__(self, name):
        self.name = name
        self.patientInfo = ''

    def __repr__(self):
        return "Patient("+str(self.name)+")="

    def __str__(self):
        return "Patient("+str(self.name)+")="

    def getPatientInfo(self):
        if self.patientInfo == '':
            patient_db = get_current("PatientDB")
            patientInfos = patient_db.QueryPatientInfo(Filter={'LastName': '^'+self.name+'$'})
            # Check that info contains exactly one item.
            if len(patientInfos) == 1:
                self.patientInfo = patientInfos[0]
            else:
                # No patient, with last name 'p' found.
                # Raise an exception.
                raise Exception(
                    "No patient or more than one patient with last \   name '{0}' in the database".format(self.name))
        return self.patientInfo

    def loadPatient(self):
        """Sets the patient as the current patient"""
        print("Loading patient: " + self.name)
        patient_db = get_current("PatientDB")
        try: 
            patient = patient_db.LoadPatient(PatientInfo=self.getPatientInfo())
            return patient
        except ValueError as e:
            print(e)
            return 'Patient could not be open'

def loadPatients(path):
    _f = open(path)
    properties = json.load(_f)
    _f.close()
    return [Patient(data, name) for name, data in properties.items()]