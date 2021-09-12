import os
import json
import pandas as pd

from collections import defaultdict


eval_type = 'indo_xnli'
size = 'small'  # large or small, only for eval on indo-xnli dev

if eval_type == 'indo_nli':
	path = 'experiments/' + eval_type + '_predictions/dev'
else:
	path = 'experiments/' + eval_type + '_predictions/dev/' + size

model_mapping = {
	'xlm-roberta-large': 'xlm-r',
	'bert-base-multilingual-cased': 'm-bert',
	'indobert-large-p2': 'indobert-large',
	'indobert-lite-base-p2': 'indobert-base'
}

gold_labels = os.path.join(path, 'gold_labels.csv')
labels = []
with open(gold_labels) as f:
	for i, line in enumerate(f):
		labels.append(line.strip())

predictions = {}
all_acc = defaultdict(lambda: defaultdict(list))

for subdir in sorted(os.listdir(path)):

	if 'gold_labels' in subdir:
		continue

	num_correct = 0
	num_total = 0

	with open(os.path.join(path, subdir)) as f:

		subdir = subdir.replace('indo_nli_ho', 'indo-nli-ho')
		subdir = subdir.replace('indo_nli_augment', 'indo-nli-augment')
		subdir = subdir.replace('indo_nli', 'indo-nli')
		subdir = subdir.replace('indo_xnli_small_ho', 'zero-shot-small-ho')
		subdir = subdir.replace('indo_xnli_small', 'zero-shot-small')
		subdir = subdir.replace('indo_xnli_config_7', 'combined_config_7')
		subdir = subdir.replace('indo_xnli_config_8', 'zero-shot_config_8')
		subdir = subdir.replace('config_', '')
		subdir = subdir.replace('.csv', '')
		
		model, exp_name, config = subdir.split('_')
		print(model, exp_name, config)
		if len(config) > 1:
			config = str(int(config[-1]) + 1)
		else:
			config = '1'

		if exp_name not in predictions:
			predictions[exp_name] = pd.DataFrame({'gold_label': labels})

		preds = []
		for i, line in enumerate(f):
			pred_label = line.strip()
			preds.append(pred_label)
			if pred_label == labels[i]:
				num_correct += 1
			num_total += 1
		
		predictions[exp_name][model_mapping[model] + '_' + config] = preds

	acc = round(num_correct * 100.0 / num_total, 2)
	all_acc[exp_name][model_mapping[model]].append(acc)

eval_dir_name = ''
if eval_type == 'indo_xnli':
	eval_dir_name = '-xnli-' + size
for exp_name in predictions:
	df = predictions[exp_name]
	df.sort_index(axis=1, inplace=True)
	df.to_csv('combined_preds/dev' + eval_dir_name + '/' + exp_name + '.csv', index=False)

with open('combined_preds/dev' + eval_dir_name + '/' + 'dev_overall_acc.csv', 'w') as f:
	headers = ['exp_name', 'model', 'run_1', 'run_2', 'run_3']
	f.write(','.join(headers) + '\n')
	lines = []
	for exp_name in sorted(list(all_acc.keys())):
		for m in sorted(list(all_acc[exp_name].keys())):
			line = [exp_name, m] + all_acc[exp_name][m]
			assert len(line) == 5
			f.write(','.join([str(x) for x in line]) + '\n')
