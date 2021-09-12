import os
import json
import random
import numpy as np


path = 'data/indo_nli/data.jsonl'

train_examples = []
dev_examples = []
test_examples = []
with open(path) as f:
	for line in f:
		items = json.loads(line)

		new_entry = dict()
		for k in items:
			if k == 'id_pair':
				new_entry['pair_id'] = items[k]
			elif k == 'id_premis':
				new_entry['premise_id'] = items[k]
			elif k == "premis_text":
				new_entry['premise'] = items[k]
			elif k == 'hypothesis_text':
				new_entry['hypothesis'] = items[k]
			else:
				new_entry[k] = items[k]

		if new_entry['data_split'] == 'train':
			train_examples.append(new_entry)
		elif new_entry['data_split'] == 'dev':
			dev_examples.append(new_entry)
		else:
			test_examples.append(new_entry)


np.random.seed(1252021)
np.random.shuffle(train_examples)
np.random.seed(1252021)
np.random.shuffle(dev_examples)
np.random.seed(1252021)
np.random.shuffle(test_examples)

ftrain = open('data/indo_nli/train.jsonl', 'w')
fdev = open('data/indo_nli/val.jsonl', 'w')
ftest = open('data/indo_nli/test_lay.jsonl', 'w')

for ex in train_examples:
	ftrain.write(json.dumps(ex) + '\n')

for ex in dev_examples:
	fdev.write(json.dumps(ex) + '\n')

for ex in test_examples:
	ftest.write(json.dumps(ex) + '\n')

ftrain.close()
fdev.close()
ftest.close()

# process expert data
path = 'data/indo_nli/expert.jsonl'
examples = []
with open(path) as f:
	for line in f:
		items = json.loads(line)

		new_entry = dict()
		for k in items:
			if k == 'id_pair':
				new_entry['pair_id'] = items[k]
			elif k == 'id_premis':
				new_entry['premise_id'] = items[k]
			elif k == "premis_text":
				new_entry['premise'] = items[k]
			elif k == 'hypothesis_text':
				new_entry['hypothesis'] = items[k]
			else:
				new_entry[k] = items[k]

		examples.append(new_entry)

np.random.seed(1252021)
np.random.shuffle(examples)
ftest = open('data/indo_nli/test_expert.jsonl', 'w')

for ex in examples:
	ftest.write(json.dumps(ex) + '\n')

ftest.close()
