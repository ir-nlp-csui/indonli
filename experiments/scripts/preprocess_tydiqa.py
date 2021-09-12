import os
import json

data_dir = 'experiments/tasks/data/tydiqa_id'

source_file = 'tydiqa.id.train.json.ori'
target_file = 'tydiqa.id.train.json'

id_data = []
data = json.load(open(os.path.join(data_dir, source_file)))
for ex in data['data']:
	ex_id = ex["paragraphs"][0]["qas"][0]["id"]
	if ex_id.startswith("indonesian-"):
		id_data.append(ex)


json_file = open(os.path.join(data_dir, target_file), 'w')
json_data = {
	"data": id_data,
	"version": "TyDiQA_id-GoldP-1.1-for-SQuAD-1.1"
}
json.dump(json_data, json_file, indent=2)
