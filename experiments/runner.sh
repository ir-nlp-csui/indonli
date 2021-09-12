WORKING_DIR=/scratch/cv50/indo-nli/experiments
DATA_DIR=${WORKING_DIR}/tasks
MODELS_DIR=${WORKING_DIR}/models
CACHE_DIR=${WORKING_DIR}/cache
RUN_CONFIG_DIR=${WORKING_DIR}/run_config_dir/taskmaster
OUTPUT_DIR=${WORKING_DIR}/output_dir/taskmaster

export PYTHONPATH=jiant/

MODEL_TYPE=$1
SEED=12345678


function run_exp() {
    MODEL_TYPE=$1
    TASK_NAME=$2
    CONFIG_NUMS=$3
    echo "$OUTPUT_DIR"

    if [[ ${TASK_NAME} == "indo_xnli" ]]; then
      train_batch_size=4
      grad_acc=4
    elif [[ ${TASK_NAME} == "indo_xnli_plus" ]]; then
      train_batch_size=4
      grad_acc=4
    elif [[ ${TASK_NAME} == "zero_shot" ]]; then
      train_batch_size=4
      grad_acc=4
    else
      train_batch_size=16
      grad_acc=1
    fi

    ###
    VAL_TASKS=$TASK_NAME
    TRAIN_TASKS=$TASK_NAME
    TEST_TASKS=$TASK_NAME
    ZERO_SHOT=false
    if [[ ${TASK_NAME} == "indo_xnli_plus" ]]; then
        TASK_NAME="indo_xnli"
        TRAIN_TASKS="indo_xnli,indo_nli"
        VAL_TASKS="indo_xnli,indo_nli"
        TEST_TASKS="indo_nli"
    elif [[ ${TASK_NAME} == "zero_shot" ]]; then
        TASK_NAME="indo_xnli"
        TRAIN_TASKS="indo_xnli"
        VAL_TASKS="indo_xnli,indo_nli"
        TEST_TASKS="indo_nli"
        ZERO_SHOT=true
    elif [[ ${TASK_NAME} == "indo_nli" ]]; then
        VAL_TASKS="indo_nli,indo_xnli,indo_xnli_small"
        TEST_TASKS="indo_nli,indo_xnli"
    elif [[ ${TASK_NAME} == "indo_xnli_sampled" ]]; then
        TASK_NAME="indo_xnli_small"
        TRAIN_TASKS="indo_xnli_small"
        VAL_TASKS="indo_xnli_small,indo_nli"
        TEST_TASKS="indo_nli"
        ZERO_SHOT=true
    fi
    # ###

    for CONFIG_NO in ${CONFIG_NUMS[@]}
    do
        val_interval=500
        echo "Train tasks: ${TRAIN_TASKS}"
        echo "Val tasks: ${VAL_TASKS}"
        echo "Test tasks: ${TEST_TASKS}"
        echo "Val: ${val_interval}"
        echo "CONFIG: ${CONFIG_NO}"
        echo "Batch size: $train_batch_size"
        echo "Gradient Accumulation Steps: $grad_acc"


        if [[ ${CONFIG_NO} == 0 ]]; then
            lr=1e-5
            epochs=10
        elif [[ ${CONFIG_NO} == 1 ]]; then
            lr=3e-5
            epochs=10
        elif [[ ${CONFIG_NO} == 2 ]]; then
            lr=1e-6
            epochs=10
        elif [[ ${CONFIG_NO} == 3 ]]; then
            lr=3e-6
            epochs=10
        elif [[ ${CONFIG_NO} == 6 ]]; then
            lr=3e-6
            epochs=3
        elif [[ ${CONFIG_NO} == 7 ]]; then
            lr=3e-6
            epochs=3
        elif [[ ${CONFIG_NO} == 8 ]]; then
            lr=3e-6
            epochs=3
        elif [[ ${CONFIG_NO} == 01 ]]; then
            lr=1e-5
            epochs=10
            SEED=76239294
        elif [[ ${CONFIG_NO} == 02 ]]; then
            lr=1e-5
            epochs=10
            SEED=52398571
        elif [[ ${CONFIG_NO} == 11 ]]; then
            lr=3e-5
            epochs=10
            SEED=76239294
        elif [[ ${CONFIG_NO} == 12 ]]; then
            lr=3e-5
            epochs=10
            SEED=52398571
        elif [[ ${CONFIG_NO} == 21 ]]; then
            lr=1e-6
            epochs=10
            SEED=76239294
        elif [[ ${CONFIG_NO} == 22 ]]; then
            lr=1e-6
            epochs=10
            SEED=52398571
        elif [[ ${CONFIG_NO} == 31 ]]; then
            lr=3e-6
            epochs=10
            SEED=76239294
        elif [[ ${CONFIG_NO} == 32 ]]; then
            lr=3e-6
            epochs=10
            SEED=52398571
        elif [[ ${CONFIG_NO} == 61 ]]; then
            lr=3e-6
            epochs=3
            SEED=76239294
        elif [[ ${CONFIG_NO} == 62 ]]; then
            lr=3e-6
            epochs=3
            SEED=52398571
        elif [[ ${CONFIG_NO} == 71 ]]; then
            lr=3e-6
            epochs=3
            SEED=76239294
        elif [[ ${CONFIG_NO} == 72 ]]; then
            lr=3e-6
            epochs=3
            SEED=52398571
        elif [[ ${CONFIG_NO} == 81 ]]; then
            lr=3e-6
            epochs=3
            SEED=76239294
        elif [[ ${CONFIG_NO} == 82 ]]; then
            lr=3e-6
            epochs=3
            SEED=52398571
        fi

        RUN_CONFIG=${RUN_CONFIG_DIR}/${MODEL_TYPE}/${TASK_NAME}_${CONFIG_NO}/${TASK_NAME}.json 

        echo ${MODEL_TYPE}
        python jiant/jiant/proj/main/scripts/configurator.py \
           SimpleAPIMultiTaskConfigurator ${RUN_CONFIG} \
           --task_config_base_path ${DATA_DIR}/configs \
           --task_cache_base_path  ${CACHE_DIR}/${MODEL_TYPE} \
           --epochs $epochs \
           --train_batch_size $train_batch_size \
           --eval_batch_multiplier 2 \
           --train_task_name_list ${TRAIN_TASKS} \
           --val_task_name_list ${VAL_TASKS} \
           --gradient_accumulation_steps ${grad_acc} \
           --test_task_name_list ${TEST_TASKS} 
        echo "Done" 

      if [[ $ZERO_SHOT == true ]]; then
        python add_task_model_map.py ${RUN_CONFIG} ${TASK_NAME}
      elif [[ $TASK_NAME == 'indo_nli' ]]; then
        python add_task_model_map.py ${RUN_CONFIG} ${TASK_NAME}
      fi

      sbatch --export=DATA_DIR=$DATA_DIR,SEED=$SEED,MODELS_DIR=$MODELS_DIR,CACHE_DIR=$CACHE_DIR,RUN_CONFIG_DIR=${RUN_CONFIG},CONFIG_NO=${CONFIG_NO},OUTPUT_DIR=$OUTPUT_DIR,TASK_NAME=$TASK_NAME,MODEL_TYPE=$MODEL_TYPE,VAL_INTERVAL=$val_interval,LR=$lr task.sbatch
    
    done
}

function download_data() {
    TASKMASTER_TASKS=$1
    for TASK_NAME in "${TASKMASTER_TASKS[@]}"
    do
       echo "Downloading $TASK_NAME"
       python jiant/jiant/scripts/download_data/runscript.py download --tasks $TASK_NAME --output_path /scratch/cv50/indo-nli/experiments/tasks/ 
   done
}

function prepare_data() {
   TASKMASTER_TASKS=$2
   for TASK_NAME in "${TASKMASTER_TASKS[@]}"
   do
       echo "run preprocess $TASK_NAME"
       bash run_preprocess.sh $1 $TASK_NAME
   done
}

function tune_hyperparameters() {
   TASKMASTER_TASKS=$2
   for TASK_NAME in "${TASKMASTER_TASKS[@]}"
   do  
       echo "run exp"
       run_exp $1 $TASK_NAME $3
   done 
}

TASKMASTER_TASKS=$2
CONFIG_NO=$3

MODEL_NAME="${MODEL_TYPE}"
OUTPUT_DIR=${OUTPUT_DIR}_${MODEL_NAME}
# TASKMASTER_TASKS=(indo_nli)

# download_data $TASKMASTER_TASKS
# prepare_data $MODEL_TYPE $TASKMASTER_TASKS
# tune_hyperparameters $MODEL_NAME $TASKMASTER_TASKS $CONFIG_NO


