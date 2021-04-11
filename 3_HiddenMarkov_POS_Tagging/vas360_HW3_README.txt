Author: Vikram Aditya Sharma
NetID: vas360
Class: CSCI-UA.0480-057
Homework: 3

> How to run the program:

You can run the program via Python from any command line interface on a machine by running the following code:

'python vas360_viterbi_HW3.py input_file output_file'

input_file --> Must be replaced with a .words entry that you wish to parse using the viterbi code

output_file --> Must be replaced with a .pos entry that will be created/overwritten upon program completion

> Handling OOV values:

In order to handle OOV values, a hardcoded approach was taken, defaulting all OOV values to 1.0/1000.0. This approach seemed the most reasonable to initial word likelihood for a POS of OOV due to the fact that there is not a large database of contextual information from which to produce definitions of all OOV items. 

> Required files:

The following files must be in the same directory as vas360_viterbi_HW3.py in order to run without errors:
-> WSJ_24.pos
-> WSJ_02_21.pos

