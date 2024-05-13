import os
from pprint import pprint

from checker.updater import update_all
from checker.collector import get_all_entities, index_entities, Index, get_matching_entities

if __name__ == "__main__":

    # Retrieve all sanctions lists (only need to do this once in your code)
    update_all()

    # Bring in all entities
    all_entities = get_all_entities()
    index = index_entities(all_entities, Index())

    search = input("Enter your search phrase:") # e.g. 'MURADOV'

    # Use direct term matching to 
    results = index.search(search, search_type='AND')
    print(f"Found {len(results)} results for search phrase '{search}'")
    pprint(results)
    
    print()
    print(f"====================")
    print()

    print(f"Doing fuzzy matching")
    results = get_matching_entities(search, all_entities)
    print(f"Found {len(results)} results uszing fuzzy matching for search phrase '{search}'")