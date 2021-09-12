import os
import json

path = 'data/indo_xnli/xnli.test.translated.id'

data = open(path).readlines()
fout = open('data/indo_xnli/test.jsonl', 'w')

header = ['gold_label', 'sentence1', 'sentence2', 'promptid', 'pairid', 'genre', 'match']
for d in data[1:]:

	items = d.strip().split('\t')

	if len(items) != len(header):
		continue

	datum = {}
	for i, x in enumerate(items):
		datum[header[i]] = x

	fout.write(json.dumps(datum, ensure_ascii=False) + '\n')

fout.close()

