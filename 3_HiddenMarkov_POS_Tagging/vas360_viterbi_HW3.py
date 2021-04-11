# Penn Treebank --> Defacto standard of part of speech tagging

import re
import os
import sys

'''
:param input_filename: Filename to .pos file in format 'word\tpos'
:return: 2 matrix of sentences with each sentence element being the word + pos
'''
def sentences_pos(input_filename):
    corpus = open(input_filename, 'r')
    tmp_sentence = []
    corpus_storage = []
    while True:
        line = corpus.readline()
        if not line:
            corpus.close()
            break
        res = line.rstrip().split("\t")
        if len(res) > 1: # You are parsing a sentence
            res[0] = res[0].lower()
            tmp_sentence.append(res)
        else: # Sentence is over
            corpus_storage.append(tmp_sentence)
            tmp_sentence = []
    return corpus_storage

'''
Table of frequencies of words that occur w/ that POS
'''
def likelihood_pos(sentences_with_pos):
    likelihood = dict()
    for sentence in sentences_with_pos:
        for word,pos in sentence:
            if pos not in likelihood: # add a pos to the likelihood
                likelihood[pos] = dict()
            if word not in likelihood[pos]:
                likelihood[pos][word] = 1
            else: # word is in likelihood under pos
                likelihood[pos][word] += 1
    return likelihood

'''
Table of frequencies of following states
'''
def following_states(sentences_with_pos):
    transitions = dict()
    for sentence in sentences_with_pos:
        tmp_array = []
        tmp_array.append('Begin_Sent')
        for word,pos in sentence:
            tmp_array.append(pos)
        tmp_array.append('End_Sent')
        # Calculate all next probabilities
        for i in range(0, len(tmp_array)-1):
            current_pos = tmp_array[i]
            next_pos = tmp_array[i+1]

            if current_pos not in transitions:
                transitions[current_pos] = dict()
            if next_pos not in transitions[current_pos]:
                transitions[current_pos][next_pos] = 0
            transitions[current_pos][next_pos] += 1
    return transitions

'''
Convert all elements in implicit parameters to probabilities
'''
def probability_transform(dictionary):
    for dict1d in dictionary:
        total_sum = sum(dictionary[dict1d].values())
        for key in dictionary[dict1d]:
            dictionary[dict1d][key] = float(dictionary[dict1d][key])/float(total_sum)

'''
:param input_filename: Filename to file with which to assemble 2d sentences
:return: 2d matrix of sentences [[0,1,2,...n, length+1]]
'''
def text_to_sentences2d(input_filename):
    corpus = open(input_filename, 'r')
    tmp_sentence = []
    corpus_storage = []
    tmp_sentence.append('Begin_Sent')
    while True:
        line = corpus.readline()
        if not line:
            corpus.close()
            break
        if len(line) > 1: # You are still parsing the sentence
            tmp_sentence.append(line.rstrip())
        else: # Sentence is over
            tmp_sentence.append('End_Sent')
            corpus_storage.append(tmp_sentence)
            tmp_sentence = []
            tmp_sentence.append('Begin_Sent')
    return corpus_storage

'''
:param sentence: [Begin_Sent, word, word, word...., End_Sent]
'''
def viterbi_sentence_tagger(sentence):
    output = []
    previous_pos = 'Begin_Sent'
    tmp_pos = ''
    for idx in range(1, len(sentence)-1):
        previous_probability = 0.0
        current_word = sentence[idx].lower()
        for pos in likelihood_pos.keys():
            likelihood = 0.0
            transition = 0.0
            if current_word in likelihood_pos[pos].keys():
                #print("P(" + current_word + "|" + pos + "): " + str(likelihood_pos[pos][current_word]))
                likelihood = likelihood_pos[pos][current_word]
                if previous_pos in transitions_pos.keys() and pos in transitions_pos[previous_pos].keys():
                    #print("P(" + previous_pos + " --> " + pos + "): " + str(transitions_pos[previous_pos][pos]))
                    transition = transitions_pos[previous_pos][pos]
                else:
                    #print("P(" + previous_pos + " --> " + pos + "): " + str(1.0/1000.0))
                    transition = 1.0/1000.0
            if likelihood * transition > previous_probability:
                previous_probability = likelihood * transition
                tmp_pos = pos
        if previous_probability == 0.0:
            # Word is OOV
            previous_pos = 'OOV'
        else:
            previous_pos = tmp_pos
        #print(previous_pos)
        output.append(previous_pos)
    return output

# Get input and output filenames
input_fn = sys.argv[1]
output_fn = sys.argv[2]
# Generate complete sentence corpus from all available datasets
sentence_corpus_1 = sentences_pos('WSJ_02-21.pos')
sentence_corpus_2 = sentences_pos('WSJ_24.pos')
complete_sentence_corpus = sentence_corpus_1 + sentence_corpus_2
# Generate the likelihood of words being certain POS
likelihood_pos = likelihood_pos(complete_sentence_corpus)
# Generate the likelihood of transition words
transitions_pos = following_states(complete_sentence_corpus)
# Transform the dictionaries from raw data to frequencies
probability_transform(likelihood_pos)
probability_transform(transitions_pos)
# Open the output file
output_file = open(output_fn, "w")
test_sentences = text_to_sentences2d(input_fn)
for sentence in test_sentences:
    poses = viterbi_sentence_tagger(sentence)
    sentence.pop(len(sentence)-1)
    sentence.pop(0)
    for idx in range(0,len(sentence)):
        output_file.write(sentence[idx] + '\t' + poses[idx] + '\n')
    output_file.write('\n')
output_file.close()
# Output file resource handling
