from typing import List
import difflib
from fuzzywuzzy import fuzz
from checker.index import analyze

THRESHOLD = 0.7

def analyze_and_join(text):
    return ' '.join(analyze(text))

def return_fuzzy_matches(query, corpus, threshold) -> List[tuple[str, float]]:
    
    # Use fuzzywuzzy partial ratio
    matches = []
    
    # Lowercase, unpunctuate, sort
    query = analyze_and_join(query)
    corpus = analyze_and_join(corpus)
    ratio = fuzz.partial_ratio(query, corpus)

    if ratio >= threshold * 100:
        matches.append((corpus, ratio))
    return matches
    
    # Use sequence match on whole corpus
    matches = []
    ratio = difflib.SequenceMatcher(None, query, corpus).ratio()
    if ratio >= threshold:
        matches.append((corpus, ratio))
    return matches

    query_terms = analyze_and_join(query)
    choices = analyze_and_join(corpus)

    # Use sequence match on tokenized corpus
    matches = []
    for term in query_terms:
        for choice in choices:
            ratio = difflib.SequenceMatcher(None, term, choice).ratio()
            if ratio >= threshold:
                matches.append((choice, ratio))
    return matches


def get_matching_entities(query, entities, threshold=THRESHOLD):
    scores_and_entities = []

    for entity in entities:
        query_word_matches = return_fuzzy_matches(query, entity.fulltext, threshold)

        if query_word_matches:
            scores_and_entities.append((query_word_matches[0][1], entity))

    return scores_and_entities