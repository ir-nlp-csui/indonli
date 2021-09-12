import os
import torch

eval_type = "indo_xnli"
mode = "large"  # large or small

# eval_type = "indo_nli"
# mode = "dev"  # dev or test

split = 'val'

data_dir = "experiments/predict_files"
model = ["bert-base-multilingual-cased", "xlm-roberta-large", "indobenchmark/indobert-large-p2", "indobenchmark/indobert-lite-base-p2"]

mapping = {0:'c', 1:'e', 2:'n'}

for m in model:
	model_dir = os.path.join(data_dir, m)
	config_dir = os.listdir(model_dir)
	for config in sorted(config_dir):
		if not config.endswith('.p'):
			continue
		
		pred_file = os.path.join(model_dir, config, split + "_preds.p")
		config_name = config.replace('_best_model.p', '')
		m = m.replace('indobenchmark/', '')

		if not os.path.exists(pred_file):
			continue

		predictions = torch.load(pred_file)
		
		if mode == "test" or mode == "dev":  # only one key
			fout = open(os.path.join("experiments/" + eval_type + "_predictions", mode, m + '_' + config_name + '.csv'), 'w')
			key = eval_type
			if "indo_nli_ho" in predictions:
				key = "indo_nli_ho"
			elif "indo_nli_augment" in predictions:
				key = "indo_nli_augment"
			if key not in predictions:
				continue
			for pred in predictions[key]["preds"]:
				fout.write(mapping[pred] + '\n')
			fout.close()
		else:
			if eval_type == 'indo_xnli' and mode == 'small':
				key = eval_type + '_' + mode
			else:
				key = eval_type
			print(model_dir, config, predictions.keys())
			if key in predictions:
				fout = open(os.path.join("experiments/" + eval_type + "_predictions/dev", mode, m + '_' + config_name + '.csv'), 'w')
				for pred in predictions[key]["preds"]:
					fout.write(mapping[pred] + '\n')
				fout.close()

