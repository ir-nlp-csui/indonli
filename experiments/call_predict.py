import os
import glob
import sys

model_name =  sys.argv[1]
task_name = sys.argv[2]
config_num = sys.argv[3]

print("task_name: ", task_name)

output_path = '/scratch/cv50/indo-nli/experiments/output_dir/taskmaster_'+ model_name + '/' + task_name + '/config_'+ str(config_num) + '/best_model.p'

print(output_path)

for file_name in glob.glob(output_path):
    names = file_name.split('/')
    ckpt_name = names[-1]
    config_no = names[-2].split('_')[-1]
    
    os.system("sbatch sb_predict_results.sbatch {} {} {} {}".format(model_name, task_name, config_no, ckpt_name))
