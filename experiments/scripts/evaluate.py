import os
import sys
import torch


# ex: python evaluate.py test.preds gold_labels.csv predictions.txt
pred_file = sys.argv[1]
gold_file = sys.argv[2]
output_file = sys.argv[3]

task_name = 'indo_nli_mt'
mapping = {0:'c', 1:'e', 2:'n'}

# get gold labels
gold_labels = []
with open(gold_file) as f:
	for i, line in enumerate(f):
		gold_labels.append(line.strip())


# get predictions
predictions = []
for pred in torch.load(pred_file)[task_name]['preds']:
	predictions.append(mapping[pred])

num_correct_lay = 0
num_correct_expert = 0
num_total_lay = 0
num_total_expert = 0

assert len(predictions) == len(gold_labels)

# compare prediction to gold label
for i, (pred, gold) in enumerate(zip(predictions, gold_labels)):
	if i <= 2200:
		if pred == gold:
			num_correct_lay += 1
		num_total_lay += 1
	else:
		if pred == gold:
			num_correct_expert += 1
		num_total_expert += 1


lay_acc = round(num_correct_lay * 100.0 / num_total_lay, 2)
expert_acc = round(num_correct_expert * 100.0 / num_total_expert, 2)


print('Lay Acc:', lay_acc)
print('Expert Acc:', expert_acc)

with open(output_file, 'w') as f:
	for p in predictions:
		f.write(p + '\n')







