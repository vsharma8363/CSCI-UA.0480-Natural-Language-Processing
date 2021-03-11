# Author: Vikram Aditya Sharma (vas360)
# DateL March 11th, 2021

import re
import math
import numpy as np

closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                           'via','vs','with','that','can','cannot','could','may','might','must',\
                           'need','ought','shall','should','will','would','have','had','has','having','be',\
                           'is','am','are','was','were','being','been','get','gets','got','gotten',\
                           'getting','seem','seeming','seems','seemed',\
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                           'you','your','yours','me','my','mine','I','we','us','much','and/or'
                           ]

'''
:return: Cosine similarity value between query and abstract
:param query: Dictionary of TFIDF values for query[word]
:param abstract: Dictionary of TFIDF values for abstract[word]
'''
def cosine_similarity(query, abstract):
    query_vector = []
    abstract_vector = []
    for word in query:
        query_vector.append(query[word])
        if word in abstract:
            abstract_vector.append(abstract[word])
        else:
            abstract_vector.append(0)
    abstract_vec = np.array(abstract_vector)
    query_vec = np.array(query_vector)
    # Calculate cosine similarity
    numerator = np.sum(abstract_vec * query_vec)
    denom1 = np.sum(abstract_vec * abstract_vec)
    denom2 = np.sum(query_vec * query_vec)
    if denom1 == 0 or denom2 == 0:
        return 0.0
    return numerator / np.sqrt(denom1 * denom2)

def create_qry_list(filename):
	ids = []
	queries_tf = []
	file = open(filename, 'r')
	file_text = file.read()
	data = file_text.split('.I ')
	for i in range(1, len(data)):
		strings = data[i].split('.W')
		id = int(strings[0])
		original_text = strings[1].lower().split()
		new_text = dict()
		for word in original_text:
			word = re.sub(r'[^\w\s]', '', word)
			word = re.sub(r'[0-9\,.]+', '', word)
			if word not in closed_class_stop_words and word != '':
				# check if word is in vector dict
				if word not in new_text:
					new_text[word] = 1
				else:
					new_text[word] += 1
		queries_tf.append(new_text)
		ids.append(id)
	return ids, queries_tf

def create_abstract_list(filename):
	abstracts_tf = []
	abstract_ids = []
	file = open(filename, 'r')
	file_text = file.read()
	data = file_text.split('.I ')
	for i in range(1, len(data)):
		strings = data[i].split('.T')
		id = int(strings[0])
		abstract_ids.append(id)
		strings = strings[1].split('.A')
		title = strings[0]
		strings = strings[1].split('.B')
		bibliography = strings[0]
		strings = strings[1].split('.W')
		text = strings[1]
		original_text = text.split()
		new_text = dict()
		for word in original_text:
			word = re.sub(r'[^\w\s]', '', word)
			word = re.sub(r'[0-9\,.]+', '', word)
			if word not in closed_class_stop_words and word != '':
				# check if word is in vector dict
				if word not in new_text:
					new_text[word] = 1
				else:
					new_text[word] += 1
		abstracts_tf.append(new_text)
	return abstract_ids, abstracts_tf

def calculate_tfidf(documents):
    num_documents_with_word = dict() # word: idf value
    for document in documents:
        for word in document:
            if word not in num_documents_with_word:
                num_documents_with_word[word] = 1
            else:
                num_documents_with_word[word] += 1
    total_num_documents = len(documents)
    for document in documents:
        for word in document:
            tf = document[word]
            idf = np.log(total_num_documents / num_documents_with_word[word])
            document[word] = tf * idf

query_ids, queries_tf = create_qry_list('cran.qry')
abstract_ids, abstracts_tf = create_abstract_list('cran.all.1400')
calculate_tfidf(abstracts_tf)
calculate_tfidf(queries_tf)

# Calculate cosine similarity for all documents for each query
outputs = [] # query id, abstract id, cosine similarity
for query_idx in range(len(queries_tf)):
    query_ouput = []
    query_id = query_ids[query_idx]
    query = queries_tf[query_idx]
    for abstract_idx in range(len(abstracts_tf)):
        abstract_id = abstract_ids[abstract_idx]
        abstract = abstracts_tf[abstract_idx]
        similarity = cosine_similarity(query, abstract)
        query_ouput.append([query_id, abstract_id, similarity])
    outputs.append(query_ouput)

output_file = open('output.txt', 'w')
for query_results in outputs:
    # sort 2d array query_results
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(query_results) - 1):
            if query_results[i][2] < query_results[i + 1][2]:
                # Swap the elements
                query_results[i], query_results[i + 1] = query_results[i + 1], query_results[i]
                # Set the flag to True so we'll loop again
                swapped = True
    for query in query_results:
        #if query[2] > 0.0:
        output_file.write(str(query[0]) + " " + str(query[1]) + " " + str(query[2]) + "\n")
output_file.close()
