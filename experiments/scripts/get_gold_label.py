import os
import sys
import json


path = sys.argv[1]
mapping = {'contradiction': 'c', 'neutral': 'n', 'entailment': 'e'}

gold_labels = list()
with open(path) as f:
	for line in f:
		items = json.loads(line)
		label = items["gold_label"]
		if label == "-":
			continue
		else:
			gold_labels.append(label)

for lbl in gold_labels:
	print(mapping[lbl])