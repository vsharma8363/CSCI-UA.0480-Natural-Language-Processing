import os
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from progress_bar import progress_bar
ps = PorterStemmer()

'''
:param train_corpus_fn: Filename of the .pos-chunk file to create training features
:param training_feature_fn: Filename of the .feature file of all training features
'''
def train_file_gen(train_corpus_fn, training_feature_fn):
    # Create progress bar
    p_bar = progress_bar(os.path.getsize(train_corpus_fn))
    # Open input/output files
    training_corpus = open(train_corpus_fn, 'r')
    training_feature = open(training_feature_fn, 'w')
    # Feature attributes
    second_last_word = None
    second_last_pos = None
    second_last_stem = None
    last_word = None
    last_pos = None
    last_stem = None
    while True:
        line = training_corpus.readline()
        if not line:
            training_corpus.close()
            break
        splits = line.strip('\n').split('\t')
        if len(splits) <= 1: # New Sentence
            # Clear feature presets
            second_last_word = None
            second_last_pos = None
            second_last_stem = None
            last_word = None
            last_pos = None
            last_stem = None
            training_feature.write('\n')
        else:
            word = splits[0]
            stemmed_word = ps.stem(splits[0])
            pos = splits[1]
            bio_tag = splits[2]
            output = word + '\tPOS=' + pos + '\tstemmed_word=' + stemmed_word

            # All custom features additions
            if second_last_word is not None:
                output += '\tsecond_last_word=' + second_last_word
            elif last_word is not None: # there is no second to last word
                second_last_word = last_word

            if second_last_pos is not None:
                output += '\tsecond_last_pos=' + second_last_pos
            elif last_pos is not None: # there is no second to last word
                second_last_pos = last_pos

            if second_last_stem is not None:
                output += '\tsecond_last_stemd=' + second_last_stem
            elif last_stem is not None: # there is no second to last word
                second_last_stem = last_stem

            if last_word is not None:
                output += '\tlast_word=' + last_word
            last_word = word
            if last_pos is not None:
                output += '\tlast_pos=' + last_pos
            last_pos = pos
            if last_stem is not None:
                output += '\tlast_stem=' + last_stem
            last_stem = stemmed_word

            output += '\t' + bio_tag + '\n'
            training_feature.write(output)
        p_bar.make_progress(len(line.encode('utf-8')))
        p_bar.print_progress()

'''
:param test_corpus_fn: Filename of the .pos file that will be used to generate test features
:param test_feature_fn: Filename of the output .feature file for testing with ME model
'''
def test_file_gen(test_corpus_fn, test_feature_fn):
    # Create progress bar
    p_bar = progress_bar(os.path.getsize(test_corpus_fn))
    test_corpus = open(test_corpus_fn, 'r')
    test_feature = open(test_feature_fn, 'w')
    # Feature attributes
    second_last_word = None
    second_last_pos = None
    second_last_stem = None
    last_word = None
    last_pos = None
    last_stem = None
    while True:
        line = test_corpus.readline()
        if not line:
            test_corpus.close()
            break
        splits = line.strip('\n').split('\t')
        if len(splits) <= 1: # New Sentence
            # Clear feature presets
            second_last_word = None
            second_last_pos = None
            second_last_stem = None
            last_word = None
            last_pos = None
            last_stem = None
            test_feature.write('\n')
        else:
            word = splits[0]
            stemmed_word = ps.stem(word)
            pos = splits[1]
            output = word + '\tPOS=' + pos + '\tstemmed_word=' + stemmed_word

            # All custom features additions
            if second_last_word is not None:
                output += '\tsecond_last_word=' + second_last_word
            elif last_word is not None: # there is no second to last word
                second_last_word = last_word

            if second_last_pos is not None:
                output += '\tsecond_last_pos=' + second_last_pos
            elif last_pos is not None: # there is no second to last word
                second_last_pos = last_pos

            if second_last_stem is not None:
                output += '\tsecond_last_stemd=' + second_last_stem
            elif last_stem is not None: # there is no second to last word
                second_last_stem = last_stem

            if last_word is not None:
                output += '\tlast_word=' + last_word
            last_word = word
            if last_pos is not None:
                output += '\tlast_pos=' + last_pos
            last_pos = pos
            if last_stem is not None:
                output += '\tlast_stem=' + last_stem
            last_stem = stemmed_word

            output += '\n'
            test_feature.write(output)
        p_bar.make_progress(len(line.encode('utf-8')))
        p_bar.print_progress()

response = ''
training_feature_fn = 'training.feature'
test_feature_fn = 'test.feature'
while True:
    response = input('Select an option: (1) Generate training.feature file, (2) Generate test.feature file, (q) to quit: ')
    if response == 'q':
        print('Exiting program!')
        exit()
    elif int(response) == 1:
        training_filename = input('Type a .pos-chunk filename to generate a training file from: ')
        train_file_gen(training_filename, training_feature_fn)
    elif int(response) == 2:
        test_filename = input('Type a .pos-chunk filename to generate a training file from: ')
        test_file_gen(test_filename, test_feature_fn)
    else:
        continue
