# Full text search engine
# See https://bart.degoe.de/building-a-full-text-search-engine-150-lines-of-code/ for main inspiration 

import re
import string
from typing import List

from checker.entities import SanctionedEntity

PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

def tokenize(text):
    return text.split()

def lowercase_filter(tokens):
    return [token.lower() for token in tokens]

def punctuation_filter(tokens):
    return [PUNCTUATION.sub('', token) for token in tokens]

def analyze(text):
    tokens = tokenize(text)
    tokens = lowercase_filter(tokens)
    tokens = punctuation_filter(tokens)

    return [token for token in tokens if token]

class Index:
    def __init__(self):
        self.index = {}
        self.entities = {}
    
    def index_entity(self, entity : SanctionedEntity):
        if entity.uid not in self.entities:
            self.entities[entity.uid] = entity

        for token in analyze(entity.fulltext):
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(entity.uid)

    def _results(self, analyzed_query):
        return [self.index.get(token, set()) for token in analyzed_query]

    def search(self, query, search_type='AND', rank=False) -> List[SanctionedEntity]:
        """
        Search; this will return documents that contain words from the query,
        and rank them if requested (sets are fast, but unordered).

        Parameters:
          - query: the query string
          - search_type: ('AND', 'OR') do all query terms have to match, or just one
          - score: (True, False) if True, rank results based on TF-IDF score
        """
        if search_type not in ('AND', 'OR'):
            return []

        analyzed_query = analyze(query)
        results = self._results(analyzed_query)
        if search_type == 'AND':
            # all tokens must be in the document
            entities = [self.entities[doc_id] for doc_id in set.intersection(*results)]
        if search_type == 'OR':
            # only one token has to be in the document
            entities = [self.entities[doc_id] for doc_id in set.union(*results)]

        if rank:
            return self.rank(analyzed_query, entities)
        return entities