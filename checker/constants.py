UK_HEADER = [
    'Name 6',
    'Name 1',
    'Name 2',
    'Name 3',
    'Name 4',
    'Name 5',
    'Title',
    'Name Non-Latin Script',
    'Non-Latin Script Type',
    'Non-Latin Script Language',
    'DOB',
    'Town of Birth',
    'Country of Birth',
    'Nationality',
    'Passport Number',
    'Passport Details',
    'National Identification Number',
    'National Identification Details',
    'Position',
    'Address 1',
    'Address 2',
    'Address 3',
    'Address 4',
    'Address 5',
    'Address 6',
    'Post/Zip Code',
    'Country',
    'Other Information',
    'Group Type',
    'Alias Type',
    'Alias Quality',
    'Regime',
    'Listed On',
    'UK Sanctions List Date Designated',
    'Last Updated',
    'Group ID'
]

EU_HEADER = [
    'fileGenerationDate','Entity_LogicalId','Entity_EU_ReferenceNumber','Entity_UnitedNationId','Entity_DesignationDate','Entity_DesignationDetails','Entity_Remark','Entity_SubjectType','Entity_SubjectType_ClassificationCode','Entity_Regulation_Type','Entity_Regulation_OrganisationType','Entity_Regulation_PublicationDate','Entity_Regulation_EntryIntoForceDate','Entity_Regulation_NumberTitle','Entity_Regulation_Programme','Entity_Regulation_PublicationUrl','NameAlias_LastName','NameAlias_FirstName','NameAlias_MiddleName','NameAlias_WholeName','NameAlias_NameLanguage','NameAlias_Gender','NameAlias_Title','NameAlias_Function','NameAlias_LogicalId','NameAlias_RegulationLanguage','NameAlias_Remark','NameAlias_Regulation_Type','NameAlias_Regulation_OrganisationType','NameAlias_Regulation_PublicationDate','NameAlias_Regulation_EntryIntoForceDate','NameAlias_Regulation_NumberTitle','NameAlias_Regulation_Programme','NameAlias_Regulation_PublicationUrl','Address_City','Address_Street','Address_PoBox','Address_ZipCode','Address_Region','Address_Place','Address_AsAtListingTime','Address_ContactInfo','Address_CountryIso2Code','Address_CountryDescription','Address_LogicalId','Address_RegulationLanguage','Address_Remark','Address_Regulation_Type','Address_Regulation_OrganisationType','Address_Regulation_PublicationDate','Address_Regulation_EntryIntoForceDate','Address_Regulation_NumberTitle','Address_Regulation_Programme','Address_Regulation_PublicationUrl','BirthDate_BirthDate','BirthDate_Day','BirthDate_Month','BirthDate_Year','BirthDate_YearRangeFrom','BirthDate_YearRangeTo','BirthDate_Circa','BirthDate_CalendarType','BirthDate_ZipCode','BirthDate_Region','BirthDate_Place','BirthDate_City','BirthDate_CountryIso2Code','BirthDate_CountryDescription','BirthDate_LogicalId','BirthDate_RegulationLanguage','BirthDate_Remark','BirthDate_Regulation_Type','BirthDate_Regulation_OrganisationType','BirthDate_Regulation_PublicationDate','BirthDate_Regulation_EntryIntoForceDate','BirthDate_Regulation_NumberTitle','BirthDate_Regulation_Programme','BirthDate_Regulation_PublicationUrl','Identification_Number','Identification_Diplomatic','Identification_KnownExpired','Identification_KnownFalse','Identification_ReportedLost','Identification_RevokedByIssuer','Identification_IssuedBy','Identification_IssuedDate','Identification_ValidFrom','Identification_ValidTo','Identification_LatinNumber','Identification_NameOnDocument','Identification_TypeCode','Identification_TypeDescription','Identification_Region','Identification_CountryIso2Code','Identification_CountryDescription','Identification_LogicalId','Identification_RegulationLanguage','Identification_Remark','Identification_Regulation_Type','Identification_Regulation_OrganisationType','Identification_Regulation_PublicationDate','Identification_Regulation_EntryIntoForceDate','Identification_Regulation_NumberTitle','Identification_Regulation_Programme','Identification_Regulation_PublicationUrl','Citizenship_Region','Citizenship_CountryIso2Code','Citizenship_CountryDescription','Citizenship_LogicalId','Citizenship_RegulationLanguage','Citizenship_Remark','Citizenship_Regulation_Type','Citizenship_Regulation_OrganisationType','Citizenship_Regulation_PublicationDate','Citizenship_Regulation_EntryIntoForceDate','Citizenship_Regulation_NumberTitle','Citizenship_Regulation_Programme','Citizenship_Regulation_PublicationUrl'
]

USA_SDN_HEADER = [
    'Ent_num',
    'SDN_Name',
    'SDN_type',
    'Program',
    'Title',
    'Call_Sign',
    'Vess_type',
    'Tonnage',
    'GRT',
    'Vess_flag',
    'Vess_owner',
    'remarks'
]

USA_ADDRESS_HEADER = [
    'Ent_num',
    'Add_num',
    'Street',
    'City',
    'Country',
    'Add_remarks'
]

USA_NULL_INDICATOR = '-0- '

SANCTIONS_FOLDER = 'data'
TIMESTAMP = '/timestamp.json'

UK_LIST = '/UKSanctionsList.csv'
EU_LIST = '/EUSanctionsList.csv'
AU_LIST = '/AUSanctionsList.xlsx'
UN_LIST = '/UNconsolidated.xml'

UK_ADDRESS = 'https://ofsistorage.blob.core.windows.net/publishlive/2022format/ConList.csv'
EU_ADDRESS = 'https://webgate.ec.europa.eu/fsd/fsf/public/files/csvFullSanctionsList_1_1/content?token=n00fewjd'
AU_ADDRESS = 'https://www.dfat.gov.au/sites/default/files/regulation8_consolidated.xlsx'
UN_ADDRESS = 'https://scsanctions.un.org/resources/xml/en/consolidated.xml'

USA_FOLDER = '/usa'
USA_FILENAMES = ['add.csv', 'sdn.csv', 'cons_add.csv', 'cons_prim.csv',]
USA_ADDRESSES = [
    'https://www.treasury.gov/ofac/downloads/add.csv',
    'https://www.treasury.gov/ofac/downloads/sdn.csv',
    'https://www.treasury.gov/ofac/downloads/consolidated/cons_add.csv',
    'https://www.treasury.gov/ofac/downloads/consolidated/cons_prim.csv'
]