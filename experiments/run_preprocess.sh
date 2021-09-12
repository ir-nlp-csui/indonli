#!/bin/bash
#SBATCH --output=/scratch/cv50/indo-nli/logs/run-%j.out
#SBATCH --error=/scratch/cv50/indo-nli/logs/run-%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --job-name=nli

# Preprocess, download, tokenization
# must point to transformers repo currently
#conda activate /scratch/cv50/virtual_envs/v_jiant2
export PYTHONPATH=jiant/

JIANT_PATH=/scratch/cv50/indo-nli/jiant/jiant
WORKING_DIR=/scratch/cv50/indo-nli/experiments
DATA_DIR=${WORKING_DIR}/tasks
MODELS_DIR=${WORKING_DIR}/models
CACHE_DIR=${WORKING_DIR}/cache

MODEL_NAME=$1
TASK_NAME=$2

echo ${MODEL_NAME}
echo ${TASK_NAME}

python ${JIANT_PATH}/proj/main/export_model.py \
   --hf_pretrained_model_name_or_path $MODEL_NAME \
   --output_base_path ${MODELS_DIR}/${MODEL_NAME}
echo "DONE: downloading model"

if [[ $MODEL_NAME = indobenchmark/indobert-large-p2 ]]
then
    MODEL_TYPE=indobert-large-p2
elif [[ $MODEL_NAME = indobenchmark/indobert-lite-base-p2 ]]
then
    MODEL_TYPE=indobert-lite-base-p2
else
    MODEL_TYPE=${MODEL_NAME}
fi

echo ${MODEL_NAME}

python ${JIANT_PATH}/proj/main/tokenize_and_cache.py \
    		--task_config_path ${DATA_DIR}/configs/${TASK_NAME}_config.json \
    		--model_type ${MODEL_TYPE} \
    		--model_tokenizer_path ${MODELS_DIR}/${MODEL_NAME}/tokenizer \
    		--phases train,val,test \
    		--max_seq_length 512 \
    		--do_iter \
    		--smart_truncate \
    		--output_dir ${CACHE_DIR}/${MODEL_NAME}/${TASK_NAME}
