import os
import json
import numpy as np


train_size = 10330
dev_size = 2198

ori_train_size, ori_dev_size = 392702, 20000

source_dir = 'experiments/tasks/data/indo_xnli'
target_dir = 'experiments/tasks/data/indo_xnli_small'

np.random.seed(1252021)
train_examples = open(os.path.join(source_dir, 'train.jsonl')).readlines()
sample_ids = np.random.choice(ori_train_size, train_size, replace=False)

fout = open(os.path.join(target_dir, 'train.jsonl'), 'w')
for i in range(ori_train_size):
	if i in sample_ids:
		fout.write(train_examples[i])
fout.close()


np.random.seed(1252021)
dev_examples = open(os.path.join(source_dir, 'dev.jsonl')).readlines()
sample_ids = np.random.choice(ori_dev_size, dev_size, replace=False)

fout = open(os.path.join(target_dir, 'dev.jsonl'), 'w')
for i in range(ori_dev_size):
	if i in sample_ids:
		fout.write(dev_examples[i])
fout.close()

