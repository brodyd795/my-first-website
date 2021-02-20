import re

# NOTE: the current script puts JUST the regex match into the 'target_sentences'.
# Later, we'll want to change '.append(x)' to '.append(line)' to keep the whole sentence

# NOTE: my 'best_output.txt' is simply all of the POS-tagged sentences that we had coded as #2

file = open("path/to/dir", 'r')
target_sentences = []
non_target_sentences = []
for line in file:
    x = re.findall('_EX.+?VB.+?NN.+?VB\w?',line)
    if 'WDT' not in x:
        target_sentences.append(line)
    if 'WDT' in x:
        non_target_sentences.append(line)

for item in target_sentences:
    print(item,end='')