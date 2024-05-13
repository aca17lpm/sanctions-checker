import csv
from typing import List

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element   
import pandas as pd

from packages.sanctions.entities import UNSanctionedEntity
from packages.sanctions.constants import ( 
    UK_HEADER, EU_HEADER, USA_ADDRESS_HEADER, USA_SDN_HEADER,
    UK_LIST, EU_LIST, UN_LIST, AU_LIST, USA_FOLDER, SANCTIONS_FOLDER
)
from packages.sanctions.entities import SanctionedEntity, UKSanctionedEntity, EUSanctionedEntity, USSanctionedEntity, AUSanctionedEntity
from packages.sanctions.index import Index
from packages.sanctions.fuzzy_matcher import get_matching_entities

        
def get_uk_entities():
    """Collects entities from UK CSV list"""
    entities = []

    with open(SANCTIONS_FOLDER + UK_LIST, encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, fieldnames=UK_HEADER)

        row_list = list(reader)
        
        for index, row in enumerate(row_list):

            names = []
            names.append(row['Name 6'])
            names.append(row['Name 1'])
            names.append(row['Name 2'])
            names.append(row['Name 3'])
            names.append(row['Name 4'])
            names.append(row['Name 5'])

            address = []
            address.append(row['Address 1'])
            address.append(row['Address 2'])
            address.append(row['Address 3'])
            address.append(row['Address 4'])
            address.append(row['Address 5'])
            address.append(row['Address 6'])
            address.append(row['Post/Zip Code'])
            address.append(row['Country'])

            entity = UKSanctionedEntity(
                source='UK',
                group_id=row['Group ID'],
                names=names,
                address=address,
                description=row['Other Information']
            )
            entities.append(entity)

    return entities

def check_for_imo(text):
    if text and 'IMO' in text:
        return True
    else:
        return False

def get_eu_entities():
    """Collects entities from EU CSV list"""

    with open(SANCTIONS_FOLDER + EU_LIST, encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, fieldnames=EU_HEADER, delimiter=';')

        entities = []
        for index, row in enumerate(reader):

            names = []
            names.append(row['NameAlias_LastName'])
            names.append(row['NameAlias_FirstName'])
            names.append(row['NameAlias_MiddleName'])
            names.append(row['NameAlias_WholeName'])

            address = []
            address.append(row['Address_PoBox'])
            address.append(row['Address_Street'])
            address.append(row['Address_City'])
            address.append(row['Address_CountryDescription'])
            address.append(row['Address_CountryIso2Code'])
            address.append(row['Address_PoBox'])
            address.append(row['Address_ZipCode'])

            identifiers = []
            # Only add the remark to text search if it contains an IMO
            if check_for_imo(row['Entity_Remark']):
                identifiers.append(row['Entity_Remark'])                

            entity = EUSanctionedEntity(
                source='EU',
                names=names,
                address=address,
                description=row['Entity_Remark'],
                reference=row['Entity_EU_ReferenceNumber'],
                url=row['Entity_Regulation_PublicationUrl'],
                identifiers=identifiers
            )

            if not entity.address : print(entity)
            entities.append(entity)

    return entities

def rewrite_eu_csv():
    with open(SANCTIONS_FOLDER + EU_LIST, encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, fieldnames=EU_HEADER, delimiter=';')
        writer = csv.writer(open('FormattedEU.csv','w', encoding='utf-8', newline=''))
        for index, row in enumerate(reader):
            writer.writerow([value for key, value in (row.items())])

def get_us_entities():
    """Collects entities from US CSV list"""

    def get_addresses(file) -> List[USSanctionedEntity]:
        with open(file, encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f, fieldnames=USA_ADDRESS_HEADER)
            entities = []

            for index, row in enumerate(reader):
                address = []
                address.append(row['Street'])
                address.append(row['City'])
                address.append(row['Country'])

                entity = USSanctionedEntity(
                    source='US',
                    names=[],
                    address=address,
                    lookup_id=row['Ent_num'],
                    description=row['Add_remarks']
                )
                entities.append(entity)
        return entities

    def get_names(file):
        with open(file, encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f, fieldnames=USA_SDN_HEADER)
            entities = []
            for index, row in enumerate(reader):
                names = []
                names.append(row['SDN_Name'])

                # Check whether IMO is present in remarks
                remarks = row['remarks']

                identifiers = []
                if check_for_imo(remarks):
                    identifiers.append(remarks)

                entity = USSanctionedEntity(
                    source='US',
                    names=names,
                    address=[],
                    lookup_id=row['Ent_num'],
                    identifiers=identifiers,
                    description=row['remarks']
                )
                entities.append(entity)
        return entities

    entities = []
    entities.extend(get_addresses(SANCTIONS_FOLDER + USA_FOLDER + '/add.csv'))
    entities.extend(get_addresses(SANCTIONS_FOLDER + USA_FOLDER + '/cons_add.csv'))
    entities.extend(get_names(SANCTIONS_FOLDER + USA_FOLDER + '/sdn.csv'))
    entities.extend(get_names(SANCTIONS_FOLDER + USA_FOLDER + '/cons_prim.csv'))
    return entities

def get_au_entities():
    """Collects entities from AU XLSX list"""

    df = pd.read_excel(SANCTIONS_FOLDER + AU_LIST)
    df = df.fillna('')

    entities = []
    for index, row in df.iterrows():
        identifiers = []
        if check_for_imo(row['Additional Information']):
            identifiers.append(row['Additional Information'])

        entity = AUSanctionedEntity(
            source='AU',
            names=[row['Name of Individual or Entity']],
            address=[row['Address']],
            description=row['Additional Information'],
            reference=row['Reference'],
            identifiers=identifiers
        )
        entities.append(entity)
    return entities

def get_un_entities():
    """Collects entities from the UN XML list
    Included aliases in fulltext search"""
    entities = []

    tree = ET.parse(SANCTIONS_FOLDER + UN_LIST) 
    root = tree.getroot()

    NAME_FIELDS = ['FIRST_NAME', 'SECOND_NAME', 'THIRD_NAME', 'FOURTH_NAME', 'FIFTH_NAME']
    def individual_to_entity(individual : Element) -> UNSanctionedEntity:
        names = [
            individual.find(name).text
            for name in NAME_FIELDS
            if individual.find(name) is not None
        ]

        # Find 'INDIVIDUAL_ADDRESS' and get all nodes, add to address
        address = []
        xml_address = individual.find('INDIVIDUAL_ADDRESS')
        for line in xml_address:
            if line is not None and line.text: address.append(line.text)

        # Find all 'INDIVIDUAL_ALIAS' and get all nodes, add to aliases
        aliases = []
        xml_aliases = individual.findall('INDIVIDUAL_ALIAS')
        for xml_alias in xml_aliases:
            alias_name = xml_alias.find('ALIAS_NAME')
            if alias_name is not None and alias_name.text: aliases.append(alias_name.text)

        reference = individual.find('REFERENCE_NUMBER').text
        description = individual.find('COMMENTS1').text

        # Includes comments in full text if IMO number present
        identifiers = []
        if check_for_imo(description):
            identifiers.append(description)

        return UNSanctionedEntity(
            source='UN',
            names=names,
            address=address,
            description=description,
            reference=reference,
            aliases=aliases,
            identifiers=identifiers
        )
    
    def xml_entity_to_entity(xml_entity : Element) -> UNSanctionedEntity:
        names = [
            xml_entity.find(name).text
            for name in NAME_FIELDS
            if xml_entity.find(name) is not None
        ]

        # Find 'ENTITY_ADDRESS' and get all nodes, add to address
        address = []
        xml_address = xml_entity.find('ENTITY_ADDRESS')
        for line in xml_address:
            if line is not None and line.text: address.append(line.text)

        # Find all 'ENTITY_ALIAS' and get all nodes, add to aliases
        aliases = []
        xml_aliases = xml_entity.findall('ENTITY_ALIAS')
        for xml_alias in xml_aliases:
            alias_name = xml_alias.find('ALIAS_NAME')
            if alias_name is not None and alias_name.text: aliases.append(alias_name.text)

        reference = xml_entity.find('REFERENCE_NUMBER').text
        description = xml_entity.find('COMMENTS1').text

        return UNSanctionedEntity(
            source='UN',
            names=names,
            address=address,
            description=description,
            reference=reference,
            aliases=aliases,
        )


    individuals = root[0]
    xml_entities = root[1]

    for xml_individual in individuals:
        entities.append(individual_to_entity(xml_individual))

    for xml_entity in xml_entities:
        entities.append(xml_entity_to_entity(xml_entity))

    print(f"Found {len(individuals)} individuals and {len(entities)} entities")
    return entities

def get_all_entities():
    entities = []
    entities.extend(get_uk_entities())
    entities.extend(get_eu_entities())
    entities.extend(get_us_entities())
    entities.extend(get_au_entities())
    entities.extend(get_un_entities())
    return entities 

def index_entities(entities : List[SanctionedEntity], index : Index):
    for i, document in enumerate(entities):
        index.index_entity(document)
    return index

if __name__ == "__main__":

    ents = get_un_entities()
    print(ents[-1])
    exit()

    all_entities = get_all_entities()
    index = index_entities(all_entities, Index())
    print(f"Index contains {len(index.entities)} documents")

    search = 'MURADOV'
    results = index.search(search, search_type='AND')
    print(f"Found {len(results)} results for {search}")
    print(results[0])

    
    print(f"====================")
    print()
    print(f"Doing fuzzy matching")
    results = get_matching_entities(search, all_entities)
    print(f"Found {len(results)} results for {search}")
