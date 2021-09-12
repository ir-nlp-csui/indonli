#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:2
#SBATCH --time=72:00:00
#SBATCH --mem=70GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=cv50@nyu.edu
#SBATCH --job-name=nli.sbatch
#SBATCH --output=/scratch/cv50/indo-nli/logs/slurm_%j.out
#SBATCH --error=/scratch/cv50/indo-nli/logs/slurm_%j.err


source activate jiant2

JIANT_PATH=/scratch/cv50/indo-nli/jiant/jiant
echo $MODELS_DIR
echo $MODEL_TYPE
echo $RUN_CONFIG_DIR
echo $SEED
export PYTHONPATH=jiant/

timestamp=$(date +%s)

python \
    $JIANT_PATH/proj/main/runscript.py   \
    run_with_continue \
       --ZZsrc ${MODELS_DIR}/${MODEL_TYPE}/config.json \
       --jiant_task_container_config_path ${RUN_CONFIG_DIR} \
       --model_load_mode from_transformers \
       --learning_rate $LR \
       --force_overwrite \
       --do_train \
       --do_val \
       --do_save \
       --eval_every_steps $VAL_INTERVAL \
       --no_improvements_for_n_evals 30 \
       --save_checkpoint_every_steps $VAL_INTERVAL \
       --output_dir ${OUTPUT_DIR}/${TASK_NAME}/config_${CONFIG_NO} \
       --seed $SEED \
       --save_every_steps 5000
