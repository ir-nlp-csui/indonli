import os
import sys
import json	

config_file = sys.argv[1]
task_name = sys.argv[2]

if task_name == 'indo_nli':
	task_mapping = {task_name: task_name,
			    	"indo_xnli": task_name,
			    	"indo_xnli_small": task_name}
else:  # zero-shot
	task_mapping = {task_name: task_name,
			    	"indo_nli": task_name}


with open(config_file) as f:
	config = json.load(f)
	config["taskmodels_config"]["task_to_taskmodel_map"] = task_mapping
	

os.remove(config_file)
with open(config_file, 'w') as f:
	json.dump(config, f, indent=4)