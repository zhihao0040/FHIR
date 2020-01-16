import requests
import pandas as pd

def checkHasNext(jsonPage):
    for i in range(len(jsonPage['link'])):
        if jsonPage['link'][i]['relation'] == "next":
            return True
    return False


patientPage = requests.get("http://hapi-fhir.erc.monash.edu:8080/baseDstu3/Patient").json()
df = pd.DataFrame(columns = ['patientId', 'birthDate'])


##########################################################################################################

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

while not (hasNoNextLinkBoolean):
    #     currentPage = currentPage.json()
    #     print(currentPage)
    try:
        for i in range(len(currentPage['entry'])):
            currentPageRes = currentPage['entry'][i]['resource']
            patientId = currentPageRes['id']
            #             print(patientId)
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

##########################################################################################################
print(df.loc[df["patientId"] == "82821"])
print(df.loc[df['patientId'] == 71525])

observationPage = requests.get("http://hapi-fhir.erc.monash.edu:8080/baseDstu3/Observation").json()

##########################################################################################################
def unitConversion(value, fromUnit="noPrefix", toUnit="noPrefix"):
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


def getValueString(observationEntryResource):
    for key in observationEntryResource.keys():
#         print(key)
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
    counter = 0
    hasNoNextLinkBoolean = False

    while not (hasNoNextLinkBoolean):
        counter += len(jsonPage['entry'])
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
            df[observationEntryResource['code']['text']] = ""

        if not checkHasNext(jsonPage):
            hasNoNextLinkBoolean = True
            jsonPage = requests.get(jsonPage['link'][1]['url']).json()

        else:
            jsonPage = requests.get(jsonPage['link'][1]['url']).json()
            print(counter)


# print(observationPage)
upadteDFWithObservationColumnNames(df, observationPage)
print(df)

##########################################################################################################
hasNoNextLinkBoolean = False
currentPage = observationPage


while not (hasNoNextLinkBoolean):
    #     currentPage = currentPage.json()
    #     print(currentPage)
    try:

        for i in range(len(currentPage['entry'])):
            currentPageRes = currentPage['entry'][i]['resource']
            patientId = currentPageRes['subject']
            effectiveDateTime = currentPageRes["effectiveDateTime"]
            valueStringKey = getValueString(currentPageRes)

            #             print(patientId)
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