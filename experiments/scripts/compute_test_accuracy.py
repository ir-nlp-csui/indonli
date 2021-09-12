import os
import json
import pandas as pd

from collections import defaultdict

path = 'experiments/indo_nli_predictions/test'
model_mapping = {
	'xlm-roberta-large': 'xlm-r',
	'bert-base-multilingual-cased': 'm-bert',
	'indobert-large-p2': 'indobert-large',
	'indobert-lite-base-p2': 'indobert-base'
}

gold_labels = os.path.join(path, 'gold_labels.csv')
labels = []
lay_gold, expert_gold = [], []
with open(gold_labels) as f:
	for i, line in enumerate(f):
		labels.append(line.strip())
		if i <= 2200:
			lay_gold.append(line.strip())
		else:
			expert_gold.append(line.strip())

lay_predictions = {}
expert_predictions = {}
lay_acc = defaultdict(lambda: defaultdict(list))
expert_acc = defaultdict(lambda: defaultdict(list))

for subdir in sorted(os.listdir(path)):

	if 'gold_labels' in subdir:
		continue

	num_correct_lay = 0
	num_correct_expert = 0
	num_total_lay = 0
	num_total_expert = 0

	with open(os.path.join(path, subdir)) as f:

		subdir = subdir.replace('indo_nli_ho', 'indo-nli-ho')
		subdir = subdir.replace('indo_nli_augment', 'indo-nli-augment')
		subdir = subdir.replace('indo_nli', 'indo-nli')
		subdir = subdir.replace('indo_xnli_small', 'zero-shot-small')
		subdir = subdir.replace('indo_xnli_config_7', 'combined_config_7')
		subdir = subdir.replace('indo_xnli_config_8', 'zero-shot_config_8')
		subdir = subdir.replace('config_', '')
		subdir = subdir.replace('.csv', '')
		
		print(subdir)
		model, exp_name, config = subdir.split('_')
		if len(config) > 1:
			config = str(int(config[-1]) + 1)
		else:
			config = '1'

		if exp_name not in lay_predictions:
			lay_predictions[exp_name] = pd.DataFrame({'lay_gold_label': lay_gold})
			expert_predictions[exp_name] = pd.DataFrame({'expert_gold_label': expert_gold})

		lay_preds, expert_preds = [], []
		for i, line in enumerate(f):
			pred_label = line.strip()
			if i <= 2200:
				lay_preds.append(pred_label)
				if pred_label == labels[i]:
					num_correct_lay += 1
				num_total_lay += 1
			else:
				expert_preds.append(pred_label)
				if pred_label == labels[i]:
					num_correct_expert += 1
				num_total_expert += 1
		lay_predictions[exp_name][model_mapping[model] + '_' + config] = lay_preds
		expert_predictions[exp_name][model_mapping[model] + '_' + config] = expert_preds

	acc = round(num_correct_lay * 100.0 / num_total_lay, 2)
	lay_acc[exp_name][model_mapping[model]].append(acc)
	acc = round(num_correct_expert * 100.0 / num_total_expert, 2)
	expert_acc[exp_name][model_mapping[model]].append(acc)

for exp_name in lay_predictions:
	df = lay_predictions[exp_name]
	df.sort_index(axis=1, inplace=True)
	df.to_csv('combined_preds/test/' + exp_name + '_lay.csv', index=False)
	df = expert_predictions[exp_name]
	df.sort_index(axis=1, inplace=True)
	df.to_csv('combined_preds/test/' + exp_name + '_expert.csv', index=False)

with open('combined_preds/test/test_overall_acc.csv', 'w') as f:
	headers = ['exp_name', 'model', 'lay_1', 'lay_2', 'lay_3', 'expert_1', 'expert_2', 'expert_3']
	f.write(','.join(headers) + '\n')
	lines = []
	for exp_name in sorted(list(lay_acc.keys())):
		for m in sorted(list(lay_acc[exp_name].keys())):
			line = [exp_name, m] + lay_acc[exp_name][m] + expert_acc[exp_name][m]
			assert len(line) == 8
			f.write(','.join([str(x) for x in line]) + '\n')




