import re
import os
import sys

# Get input and output filenames
input_fn = sys.argv[1]
#output_fn = sys.argv[2]

def get_chunks(input_filename):
    chunks = open(input_filename, 'r')
    while True:
        line = chunks.readline()
        if not line:
            chunks.close()
            break
        print(chunks)

get_chunks(input_fn)
