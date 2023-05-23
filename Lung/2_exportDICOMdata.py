# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:55:10 2023

@author: borderiasvil
"""
from connect import *
import json

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

case = get_current("Case")
patient = get_current("Patient")
ctv_name = "CTV_T_LN"
phases_groups = ["Phases 2","Phases 3"]

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

for ct_group in phases_groups:
    index = ct_group[-1]
    ct_ref = "MidP CT "+index
    ct_phases_renamed = [x.Examination.Name for x in case.ExaminationGroups[ct_group].Items]

    cts_to_export = ct_phases_renamed

    for ct in cts_to_export:
        path = os.path.join("Y:\\Elena\\Clean_data_Dario",patient.Name,index,ct)
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



