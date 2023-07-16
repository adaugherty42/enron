from document import Document
from heapq import heappush, heappushpop
import math


def calculate_term_frequency(email, term):
    text = (email['subject'] + ' ' + email['body']).split()
    if len(text) == 0:
        return 0
    return len([w for w in text if w.lower() == term.lower()]) / len(text)


def calculate_term_frequencies(email, search):
    return {w: calculate_term_frequency(email, w) for w in search.split()}


def calculate_inverse_document_frequency(documents, term):
    num_matches = len([d for d in documents if d.term_frequencies.get(term, 0) > 0])
    return 0 if num_matches == 0 else math.log(len(documents) / num_matches, 10)


def initialize_documents(emails, search):
    print('Initializing documents with term frequencies...')
    documents = []

    for email in emails:
        term_frequencies = calculate_term_frequencies(email, search)
        documents.append(
            Document(
                author=email['from'],
                term_frequencies=term_frequencies,
                subject=email['subject'],
                body=email['body']
            )
        )

    # Some emails are in multiple inboxes, so deduplicate here
    dedup = set()

    def check_duplicates(document):
        if document.body in dedup:
            return False
        else:
            dedup.add(document.body)
            return True

    print('Finished initializing documents with term frequencies')
    return list(filter(check_duplicates, documents))


def calculate_tfidf_score(document, search, inverse_document_frequencies):
    score = 0
    for term in search.split():
        term_frequency = document.term_frequencies.get(term.lower()) or 0
        inverse_document_frequency = inverse_document_frequencies.get(term.lower())
        score += term_frequency * inverse_document_frequency
    return score


def calculate_top_search_results(documents, search, num_results=25):
    inverse_document_frequencies = {
        w.lower(): calculate_inverse_document_frequency(documents, w.lower()) for w in search.split()
    }

    minheap = []
    for i, document in enumerate(documents):
        score = calculate_tfidf_score(document, search, inverse_document_frequencies)
        if score == 0:
            continue

        if len(minheap) < num_results:
            heappush(minheap, (score, i, document))
        else:
            heappushpop(minheap, (score, i, document))

    return sorted(minheap, reverse=True)