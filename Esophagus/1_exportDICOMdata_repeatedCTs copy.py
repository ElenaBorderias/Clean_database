# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:55:10 2023

@author: borderiasvil
"""
from connect import *
from Patients import Patient
import json
import os

def log_warning(error):
    """ Example on how to read the JSON error string."""

    try:
        json_errors = json.loads(str(error))
        # If the json.loads() works then the script was stopped due to
        # a non-blocking warning.
        print('WARNING! Export Aborted!')
        print('Comment:')
        print(json_errors['Comment'])
        print('Warnings:')

        # Here the user can handle the warnings. Continue on known warnings,
        # stop on unknown warnings.
        for warning in json_errors['Warnings']:
            print(warning)
    except ValueError:
        # The error was likely due to a blocking warning, and the details should be stated in the execution log. 
        print('Error occurred. Could not export.')

def log_completed(result):
    """ This prints the successful result log in an ordered way. """

    try:
        json_result = json.loads(result)
        print('Completed!')
        print('Comment:')
        print(json_result['Comment'])
        print('Warnings:')
        for warning in json_result['Warnings']:
            print(warning)
        print('Export notifications:')
        # Export notifications is a list of notifications that the user should read.
        for notification in json_result['Notifications']:
            print(notification)
    except ValueError:
        print('Error reading completion messages.')

patient_list = []
index_list = [42,43,44,45,46,47,48,49,50,51,53,54,55,59,60,63,65,52]
print(index_list)

for i in index_list:
    patient_list.append("0" + str(i) + "_Esophagus_AI_KUL")
print(patient_list)

for patient_name in patient_list:
    pat = Patient(patient_name)
    RS_Patient = pat.loadPatient()
    patient = get_current("Patient")

    if patient_name == "052_Esophagus_AI_KUL":
      case_name = "Repeated CT PT"
    else:
      case_name = "Repeated CT"

    RS_Patient.Cases[case_name].SetCurrent() 

    case = get_current("Case")
    clinic_db = get_current('ClinicDB')

    default_anonymization_options = clinic_db.GetSiteSettings().DicomSettings.DefaultAnonymizationOptions
    anonymization_settings = {'Anonymize': False,
                                'AnonymizedName': 'anonymizedName',
                                'AnonymizedID': 'anonymizedID',
                                'RetainDates': default_anonymization_options.RetainLongitudinalTemporalInformationFullDatesOption,
                                'RetainDeviceIdentity': default_anonymization_options.RetainDeviceIdentityOption,
                                'RetainInstitutionIdentity': default_anonymization_options.RetainInstitutionIdentityOption,
                                'RetainUIDs': default_anonymization_options.RetainUIDs,
                                'RetainSafePrivateAttributes': default_anonymization_options.RetainSafePrivateOption}
    ct = "Average CT new"

    path = os.path.join("Y:\\Elena\\Repeated_cts_eso",patient.Name,ct)
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        result = case.ScriptableDicomExport(ExportFolderPath = path,
                                            AnonymizationSettings = anonymization_settings,
                                            Examinations = [ct],
                                            RtStructureSetsForExaminations = [ct],
                                            DicomFilter = '',
                                            IgnorePreConditionWarnings = True)
        log_completed(result)
    except Exception as error:
        log_warning(error)
        raise error



