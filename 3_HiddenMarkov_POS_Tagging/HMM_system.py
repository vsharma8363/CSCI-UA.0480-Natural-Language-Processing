# Penn Treebank --> Defacto standard of part of speech tagging

import re
import os
import sys

'''
:param input_filename: Filename to .pos file in format 'word\tpos'
:return: 2 matrix of sentences with each sentence element being the word + pos
'''
def generate_pos_2d(input_filename):
    corpus = open(input_filename, 'r', encoding="utf8")
    tmp_sentence = []
    corpus_storage = []
    while True:
        line = corpus.readline()
        if not line:
            corpus.close()
            break
        res = line.rstrip().split("\t")
        if len(res) > 1: # You are parsing a sentence
            tmp_sentence.append(res)
        else: # Sentence is over
            corpus_storage.append(tmp_sentence)
            tmp_sentence = []
    return corpus_storage

corpus_2d = generate_pos_2d('WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_02-21.pos')
print(corpus_2d[0])
