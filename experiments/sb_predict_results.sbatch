#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:1
#SBATCH --time=2:00:00
#SBATCH --mem=40GB
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=cv50@nyu.edu
#SBATCH --job-name=g_predict.sbatch
#SBATCH --output=/scratch/cv50/indo-nli/logs/pred_%j.out
#SBATCH --error=/scratch/cv50/indo-nli/logs/pred_%j.err


# source activate jiant2


JIANT_PATH=/scratch/cv50/indo-nli/jiant/jiant
export PYTHONPATH=jiant/

model=$1
task=$2
config_no=$3
model_path=$4
mkdir -p experiments/predict_files/${model}

echo "${model} ${task} ${config_no} ${model_path}"

python $JIANT_PATH/proj/main/runscript.py run   \
        --ZZsrc experiments/models/${model}/config.json  \
        --jiant_task_container_config_path experiments/run_config_dir/taskmaster/${model}/${task}_${config_no}/${task}.json  \
		--model_load_mode all --model_path experiments/output_dir/taskmaster_${model}/${task}/config_${config_no}/${model_path}  \
        --output_dir  experiments/predict_files/${model}/${task}_config_${config_no}_${model_path}  \
        --ZZoverrides model_path --do_val --write_val_preds \
         --write_test_preds

