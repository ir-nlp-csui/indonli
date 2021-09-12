import os
import json
import numpy as np

filepath = 'data/indo_nli/train_sorted.jsonl'
target_path = 'experiments/tasks/data/indo_nli/train_augment.jsonl'


np.random.seed(1252021)

data = open(filepath).readlines()
data = [json.loads(d) for d in data]
least_similar = data[:1000]

keep_examples = [] 
sample_ids = np.random.choice(1000, 500, replace=False)

for i in sample_ids:
	keep_examples.append(least_similar[i])

full_data = keep_examples + data[1000:]


# shuffle data order
np.random.seed(1252021)
np.random.shuffle(full_data)

with open(target_path, 'w') as f:
	for d in full_data:
		f.write(json.dumps(d, ensure_ascii=False) + '\n')