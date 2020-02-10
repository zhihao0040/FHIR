###
"""
A Jupyter Notebook is not used because the amount of output slows down the 
Jupyter notebook by a lot and crashes it.

This python script should serve only as an example of querying for pages. 
The current approach is not scalable as one needs to type out all possible fields.

The current approach goes through each type of resource each page at a time to visit every single detail.
1) Patient
2) Observation
3) Immunization
4) DiagnosticReport
and so on
"""


import requests
import pandas as pd


### Base URL - The base URL used when extracting the data
BASE_URL = "http://hapi-fhir.erc.monash.edu:8080/baseDstu3/"
# BASE_URL = "http://hapi.fhir.org/baseR4/"

def checkHasNext(jsonPage):
    """
    Returns a boolean indicating whether the current jsonPage has a link to the next page.
    :param jsonPage: The current json string returned from querying a page
    :timecomplexity: O(1) since there are only 3 items in jsonPage['link'] at max
    :return: a Boolean indicating if the current jsonPage still has a next page
    """
    for i in range(len(jsonPage['link'])):
        if jsonPage['link'][i]['relation'] == "next":
            return True
    return False

# Starting off with Patient's basic details, in order to obtain Patient id
patientPage = requests.get(BASE_URL + "Patient").json()
df = pd.DataFrame(columns = ['patientId', 'birthDate'])


##########################################################################################################
# These are strings that are used as keys 
# DataFrame's columns relating to patient initialized here
hasNoNextLinkBoolean = False
currentPage = patientPage
PATIENT_MOTHER_MAIDEN_NAME = "patient-mothersMaidenName"
US_CORE_RACE = "us-core-race"
US_CORE_ETHNICITY = "us-core-ethnicity"
US_CORE_BIRTHSEX = "us-core-birthsex"
US_CORE_BIRTHPLACE = "birthPlace"
DISABILITY_ADJUSTED_LIFE_YEARS = "disability-adjusted-life-years"
QUALITY_ADJUSTED_LIFE_YEARS = "quality-adjusted-life-years"
extUrlHeader = "http://hl7.org/fhir/us/core/StructureDefinition/"
extUrlHeader2 = "http://synthetichealth.github.io/synthea/"
df[US_CORE_RACE] = ""
df[US_CORE_ETHNICITY] = ""
df[US_CORE_BIRTHSEX] = ""
df[US_CORE_BIRTHPLACE + "City"] = ""
df[US_CORE_BIRTHPLACE + "State"] = ""
df[US_CORE_BIRTHPLACE + "Country"] = ""
df[DISABILITY_ADJUSTED_LIFE_YEARS] = ""
df[QUALITY_ADJUSTED_LIFE_YEARS] = ""
df["gender"] = ""
df["birthDate"] = ""
df["maritalStatus"] = ""
df["multipleBirthBoolean"] = ""

while not (hasNoNextLinkBoolean): # while not at last page, will not skip last page as the boolean will be set to false at the bottom only
    try: # these code and access to data are obtained by looking the structure of the page as shown in https://www.hl7.org/fhir/patient.html
        for i in range(len(currentPage['entry'])): # for each entry
            currentPageRes = currentPage['entry'][i]['resource']
            patientId = currentPageRes['id']
            df.loc[len(df.index), 'patientId'] = patientId

            for j in range(len(currentPageRes['extension'])):

                ## Populating the info that is to be added into the dataframe
                extUrl = currentPageRes['extension'][j]['url']
                extUrlCore = extUrl[len(extUrlHeader):]
                extUrlCore2 = extUrl[len(extUrlHeader2):]
                if extUrlCore == US_CORE_RACE or extUrlCore == US_CORE_ETHNICITY:
                    patientInfo = currentPageRes['extension'][j]['extension'][0]['valueCoding']['display']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore] = patientInfo


                elif extUrlCore == US_CORE_BIRTHSEX:
                    patientInfo = currentPageRes['extension'][j]["valueCode"]

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore] = patientInfo

                elif extUrlCore == US_CORE_BIRTHPLACE:
                    patientInfoBirthAddress = currentPageRes['extension'][j]["valueAddress"]
                    patientInfoBirthCity = patientInfoBirthAddress['city']
                    patientInfoBirthState = patientInfoBirthAddress['state']
                    patientInfoBirthCountry = patientInfoBirthAddress['country']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore + "City"] = patientInfoBirthCity
                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore + "State"] = patientInfoBirthState
                    df.loc[(df.index[df['patientId'] == patientId])[0]][
                        extUrlCore + "Country"] = patientInfoBirthCountry

                elif extUrlCore == DISABILITY_ADJUSTED_LIFE_YEARS:
                    patientInfo = currentPageRes['extension'][j]['valueDecimal']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore] = patientInfo

                elif extUrlCore == QUALITY_ADJUSTED_LIFE_YEARS:
                    patientInfo = currentPageRes['extension'][j]['valueDecimal']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore] = patientInfo

                elif extUrlCore2 == US_CORE_RACE or extUrlCore2 == US_CORE_ETHNICITY:
                    patientInfo = currentPageRes['extension'][j]['extension'][0]['valueCoding']['display']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2] = patientInfo

                elif extUrlCore2 == US_CORE_BIRTHSEX:
                    patientInfo = currentPageRes['extension'][j]["valueCode"]

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2] = patientInfo

                elif extUrlCore2 == US_CORE_BIRTHPLACE:
                    patientInfoBirthAddress = currentPageRes['extension'][j]["valueAddress"]
                    patientInfoBirthCity = patientInfoBirthAddress['city']
                    patientInfoBirthState = patientInfoBirthAddress['state']
                    patientInfoBirthCountry = patientInfoBirthAddress['country']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2 + "City"] = patientInfoBirthCity
                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2 + "State"] = patientInfoBirthState
                    df.loc[(df.index[df['patientId'] == patientId])[0]][
                        extUrlCore2 + "Country"] = patientInfoBirthCountry

                elif extUrlCore2 == DISABILITY_ADJUSTED_LIFE_YEARS:
                    patientInfo = currentPageRes['extension'][j]['valueDecimal']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2] = patientInfo

                elif extUrlCore2 == QUALITY_ADJUSTED_LIFE_YEARS:
                    patientInfo = currentPageRes['extension'][j]['valueDecimal']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2] = patientInfo
                
                ##
            
            ## Putting the data into the dataframe based on patientId
            patientGender = currentPageRes["gender"]
            patientBirthDate = currentPageRes["birthDate"]
            patientMaritalStatus = currentPageRes["maritalStatus"]['coding'][0]['display']
            patientMultipleBirthBoolean = currentPageRes['multipleBirthBoolean']

            df.loc[(df.index[df['patientId'] == patientId])[0]]["gender"] = patientGender

            df.loc[(df.index[df['patientId'] == patientId])[0]]["birthDate"] = patientBirthDate

            df.loc[(df.index[df['patientId'] == patientId])[0]]["maritalStatus"] = patientMaritalStatus

            df.loc[(df.index[df['patientId'] == patientId])[0]]["multipleBirthBoolean"] = patientMultipleBirthBoolean
            
            ##


    except KeyError as error: ## Sometimes the page doesn't fully follow the structure as defined in https://www.hl7.org/fhir/patient.html
                              ## for e.g. when the patient doesn't have their birhdates recorded and etc.
        print(error)

    if not checkHasNext(currentPage):  ## if don't have next page, set hasNoNextLinkBoolean to true
        hasNoNextLinkBoolean = True
        currentPage = requests.get(currentPage['link'][1]['url']).json()

    else:
        currentPage = requests.get(currentPage['link'][1]['url']).json()

# print(df)

##########################################################################################################
# print(df.loc[df["patientId"] == "82821"])
# print(df.loc[df['patientId'] == 71525])

observationPage = requests.get(BASE_URL + "Observation").json()

##########################################################################################################
# I converted most units to 10^0 at the time but shouldn't do this but rather include inside the name of the field the prefix for e.g. totalCholestrol (mg)
def unitConversion(value, fromUnit="noPrefix", toUnit="noPrefix"):
    """
    Ad-hoc way of allowing conversion of units from one prefix to the other
    :param value: The value in the current unit
    :param fromUnit: The current prefix of the value
    :param toUnit: The unit to change the current value to
    :timecomplexity: O(1) 
    :return: the value with its 'value' changed to the current unit
    """
    prefix = {'y': 1e-24,  # yocto
              'z': 1e-21,  # zepto
              'a': 1e-18,  # atto
              'f': 1e-15,  # femto
              'p': 1e-12,  # pico
              'n': 1e-9,  # nano
              'u': 1e-6,  # micro
              'm': 1e-3,  # mili|
              'c': 1e-2,  # centi
              'd': 1e-1,  # deci
              'k': 1e3,  # kilo
              'M': 1e6,  # mega
              'G': 1e9,  # giga
              'T': 1e12,  # tera
              'P': 1e15,  # peta
              'E': 1e18,  # exa
              'Z': 1e21,  # zetta
              'Y': 1e24,  # yotta
              }
    if toUnit[:1] not in prefix.keys():
        if toUnit == "noPrefix":
            toUnit = 1
        else:
            return value
    else:
        if toUnit == "noPrefix":
            toUnit = 1
        else:
            toUnit = prefix[toUnit[:1]]

    if fromUnit[:1] not in prefix.keys():
        if fromUnit == "noPrefix":
            fromUnit = 1
        else:
            return value
    else:
        if fromUnit == "noPrefix":
            fromUnit = 1
        else:
            fromUnit = prefix[fromUnit[:1]]

    return value / (toUnit / fromUnit)


def getValueString(observationEntryResource): # as shown in https://www.hl7.org/fhir/patient.html, valueStrings can be in multiple formats
    """
    Based on https://www.hl7.org/fhir/patient.html, identified all possible valueStrings. Ignoring some like 'time periods' for now
    :param observationEntryResource: BASE_URL/Patient.json()['entry'][i]['resource']
    :timecomplexity: O(1) 
    :return: the type of valueString
    """  
    for key in observationEntryResource.keys(): # should only have 1 key, keys() is in []
        if key == "valueQuantity":
            return key
        elif key == "valueCodeableConcept":
            return key
        elif key == "valueString":
            return key
        elif key == "valueBoolean":
            return key
        elif key == "valueInteger":
            return key
        elif key == "valueRange":
            return key
        elif key == "valueRatio":
            return key
        elif key == "valueSampledData":
            return key
        elif key == " valueTime":
            return key
        elif key == "valueDateTime":
            return key
        elif key == "valuePeriod":
            return key
##########################################################################################################
def upadteDFWithObservationValueOfPatient(df, patientId, observationEntryResource):
    """
    Update df at the patientId's row with the info to update
    :param df: the dataframe to be updated 
    :param patientId: the row/patient info to be updated
    :param observationEntryResource: BASE_URL/Patient.json()['entry'][i]['resource']
    :timecomplexity: df[loc]'s time complexity
    """  
    for key in observationEntryResource.keys():
#         print(key)
        if key == "valueQuantity":
            df.loc[(df.index[df['patientId'] == patientId])[0]][observationEntryResource['code']['text']] = unitConversion(observationEntryResource[key]['value'], observationEntryResource[key]['unit'], "noPrefix")
        elif key == "valueCodeableConcept":
            df.loc[(df.index[df['patientId'] == patientId])[0]][observationEntryResource['code']['text']] = observationEntryResource[key]['text']
#             return observationEntryResource[key]['text']
        elif key == "valueString":
            df.loc[(df.index[df['patientId'] == patientId])[0]][observationEntryResource['code']['text']] = observationEntryResource[key]
#             return observationEntryResource[key]
        elif key == "valueBoolean":
            df.loc[(df.index[df['patientId'] == patientId])[0]][observationEntryResource['code']['text']] = observationEntryResource[key]
#             return observationEntryResource[key]
        elif key == "valueInteger":
            df.loc[(df.index[df['patientId'] == patientId])[0]][observationEntryResource['code']['text']] = observationEntryResource[key]
#             return observationEntryResource[key]
        elif key == "valueRange":
            df.loc[(df.index[df['patientId'] == patientId])[0]][observationEntryResource['code']['text']] = (observationEntryResource[key]['high'] + observationEntryResource[key]['low']) / 2
#             return (observationEntryResource[key]['high'] + observationEntryResource[key]['low']) / 2
        elif key == "valueRatio":
            df.loc[(df.index[df['patientId'] == patientId])[0]][observationEntryResource['code']['text']] = observationEntryResource[key]['numerator']/observationEntryResource[key]['denominator']
#             return observationEntryResource[key]['numerator']/observationEntryResource[key]['denominator']
        elif key == "valueSampledData":
            df.loc[(df.index[df['patientId'] == patientId])[0]][observationEntryResource['code']['text']] = observationEntryResource[key]['data']
#             return observationEntryResource[key]['data']
        elif key == " valueTime": ##
            df.loc[(df.index[df['patientId'] == patientId])[0]][observationEntryResource['code']['text']] = observationEntryResource[key]
#             return observationEntryResource[key]
        elif key == "valueDateTime":
            df.loc[(df.index[df['patientId'] == patientId])[0]][observationEntryResource['code']['text']] = observationEntryResource[key]
#             return observationEntryResource[key]
        elif key == "valuePeriod":
            df.loc[(df.index[df['patientId'] == patientId])[0]][observationEntryResource['code']['text']] = observationEntryResource[key]
#             return observationEntryResource[key]

##########################################################################################################

def upadteDFWithObservationColumnNames(df, jsonPage):
    """
    Update df with column names by going through each page 
    :param df: The dataframe to be updated
    :jsonPage: The whole json string returned when querying a page
    """  
    # counter = 0
    hasNoNextLinkBoolean = False

    while not (hasNoNextLinkBoolean): 
        # counter += len(jsonPage['entry'])
        for i in range(len(jsonPage['entry'])):
            observationEntryResource = jsonPage['entry'][i]['resource']
            #             print(str(observationEntryResource))
            if observationEntryResource['resourceType'] != "Observation":
                continue
            #         print(observationEntryResource)
            #         print("\n")
            #         print("\n")
            #         print("\n")
            #         print(observationEntryResource.keys())
            #         print(observationEntryResource['code']['text'])
            df[observationEntryResource['code']['text']] = "" # Update df with various field names

        if not checkHasNext(jsonPage):
            hasNoNextLinkBoolean = True
            jsonPage = requests.get(jsonPage['link'][1]['url']).json()

        else:
            jsonPage = requests.get(jsonPage['link'][1]['url']).json()
            # print(counter)


# print(observationPage)
upadteDFWithObservationColumnNames(df, observationPage)
print(df)

##########################################################################################################
hasNoNextLinkBoolean = False
currentPage = observationPage


while not (hasNoNextLinkBoolean): # while not at last page, will not skip last page as the boolean will be set to false at the bottom only
    try:

        for i in range(len(currentPage['entry'])): # these code and access to data are obtained by looking the structure of the page as shown in https://www.hl7.org/fhir/observation.html
            currentPageRes = currentPage['entry'][i]['resource']
            patientId = currentPageRes['subject']
            effectiveDateTime = currentPageRes["effectiveDateTime"]
            valueStringKey = getValueString(currentPageRes)

            df.loc[len(df.index), 'patientId'] = patientId

            for j in range(len(currentPageRes['extension'])):
                extUrl = currentPageRes['extension'][j]['url']
                extUrlCore = extUrl[len(extUrlHeader):]
                extUrlCore2 = extUrl[len(extUrlHeader2):]
                if extUrlCore == US_CORE_RACE or extUrlCore == US_CORE_ETHNICITY:
                    patientInfo = currentPageRes['extension'][j]['extension'][0]['valueCoding']['display']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore] = patientInfo


                elif extUrlCore == US_CORE_BIRTHSEX:
                    patientInfo = currentPageRes['extension'][j]["valueCode"]

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore] = patientInfo

                elif extUrlCore == US_CORE_BIRTHPLACE:
                    patientInfoBirthAddress = currentPageRes['extension'][j]["valueAddress"]
                    patientInfoBirthCity = patientInfoBirthAddress['city']
                    patientInfoBirthState = patientInfoBirthAddress['state']
                    patientInfoBirthCountry = patientInfoBirthAddress['country']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore + "City"] = patientInfoBirthCity
                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore + "State"] = patientInfoBirthState
                    df.loc[(df.index[df['patientId'] == patientId])[0]][
                        extUrlCore + "Country"] = patientInfoBirthCountry

                elif extUrlCore == DISABILITY_ADJUSTED_LIFE_YEARS:
                    patientInfo = currentPageRes['extension'][j]['valueDecimal']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore] = patientInfo

                elif extUrlCore == QUALITY_ADJUSTED_LIFE_YEARS:
                    patientInfo = currentPageRes['extension'][j]['valueDecimal']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore] = patientInfo

                elif extUrlCore2 == US_CORE_RACE or extUrlCore2 == US_CORE_ETHNICITY:
                    patientInfo = currentPageRes['extension'][j]['extension'][0]['valueCoding']['display']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2] = patientInfo

                elif extUrlCore2 == US_CORE_BIRTHSEX:
                    patientInfo = currentPageRes['extension'][j]["valueCode"]

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2] = patientInfo

                elif extUrlCore2 == US_CORE_BIRTHPLACE:
                    patientInfoBirthAddress = currentPageRes['extension'][j]["valueAddress"]
                    patientInfoBirthCity = patientInfoBirthAddress['city']
                    patientInfoBirthState = patientInfoBirthAddress['state']
                    patientInfoBirthCountry = patientInfoBirthAddress['country']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2 + "City"] = patientInfoBirthCity
                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2 + "State"] = patientInfoBirthState
                    df.loc[(df.index[df['patientId'] == patientId])[0]][
                        extUrlCore2 + "Country"] = patientInfoBirthCountry

                elif extUrlCore2 == DISABILITY_ADJUSTED_LIFE_YEARS:
                    patientInfo = currentPageRes['extension'][j]['valueDecimal']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2] = patientInfo

                elif extUrlCore2 == QUALITY_ADJUSTED_LIFE_YEARS:
                    patientInfo = currentPageRes['extension'][j]['valueDecimal']

                    df.loc[(df.index[df['patientId'] == patientId])[0]][extUrlCore2] = patientInfo

            # Update df with info -- not completed cause this method is deemed unscalable for now
            # looking into Google/Fhir
            # change accordingly below as shown in the same code above.
            patientGender = currentPageRes["gender"]
            patientBirthDate = currentPageRes["birthDate"]
            patientMaritalStatus = currentPageRes["maritalStatus"]['coding'][0]['display']
            patientMultipleBirthBoolean = currentPageRes['multipleBirthBoolean']

            df.loc[(df.index[df['patientId'] == patientId])[0]]["gender"] = patientGender

            df.loc[(df.index[df['patientId'] == patientId])[0]]["birthDate"] = patientBirthDate

            df.loc[(df.index[df['patientId'] == patientId])[0]]["maritalStatus"] = patientMaritalStatus

            df.loc[(df.index[df['patientId'] == patientId])[0]]["multipleBirthBoolean"] = patientMultipleBirthBoolean



    except KeyError as error:
        print(error)

    if not checkHasNext(currentPage):
        hasNoNextLinkBoolean = True
        currentPage = requests.get(currentPage['link'][1]['url']).json()

    else:
        currentPage = requests.get(currentPage['link'][1]['url']).json()

print(df)
# display(df)