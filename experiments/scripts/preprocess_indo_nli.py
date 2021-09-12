import os
import sys
import csv
import json

data_dir = 'data/indo_nli'
phases = ['train', 'val']

for phase in phases:
	json_file = open(os.path.join(data_dir, phase + '.jsonl'), 'w')
	with open(os.path.join(data_dir, phase + '.csv')) as f:
		reader = csv.DictReader(f)
		for row in reader:
			json_file.write(json.dumps(dict(row), ensure_ascii=False) + "\n")
	json_file.close()


