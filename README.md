# sanctions-checker
Python tool for checking sanctions lists.

Gathers sanctions lists from the following sources.

USA - https://ofac.treasury.gov/

EU - https://data.europa.eu/data/datasets/consolidated-list-of-persons-groups-and-entities-subject-to-eu-financial-sanctions?locale=en

UK - https://www.gov.uk/government/publications/the-uk-sanctions-list

Australia - https://www.dfat.gov.au/international-relations/security/sanctions/consolidated-list

UN - https://www.un.org/securitycouncil/content/un-sc-consolidated-list

Run `python main.py` to gather the lists, and run a search for a name. Use the modules separately in your own code to update the lists how often you need, and run searches on your gathered lists.

## How it works

This project processes information from each file from each authority into a list of **SanctionedEntities**. These are a Python dataclass which record key information about an entity, which can be a person, place, or organisation. These entities can then be filtered with a fulltext search, through either fuzzy matching or using indexed terms.