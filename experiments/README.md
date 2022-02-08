# Experiments

## Installation and Setup

Requirements (the code was successfully ran using the following versions):
- transformers==3.1.0
- torch==1.7.0

First, clone this repository:

```bash
git clone git@github.com:claravania/indo-nli.git
cd indo-nli
```

After that, install jiant under the current directory (better to use a virtual environment):
```bash
git clone -b indo-nli git@github.com:claravania/jiant.git
cd jiant
conda create -n jiant python=3.7
conda activate jiant
pip install -r requirements-dev.txt
cp ../experiments .
cd ..
```

The `experiments` folder contains some configuration files and datasets that are used for experiment. To add a new dataset, first make a similar directory under `experiments/tasks/data`, and then create a configuration file for that dataset and put it under `experiments/tasks/config`. If using dataset that has the same format as already implemented task (e.g., indo-nli), we can just write a config file for the new dataset but still using the same original task name. As an example, if we  want to use an augmented training data for `indo_nli` (e.g., `indo_nli_augment_config.json`):
```json
{
  "task": "indo_nli",
  "paths": {
    "train": "/scratch/cv50/indo-nli/experiments/tasks/data/indo_nli/train_augment.jsonl",
    "val": "/scratch/cv50/indo-nli/experiments/tasks/data/indo_nli/val.jsonl",
    "test": "/scratch/cv50/indo-nli/experiments/tasks/data/indo_nli/test.jsonl"
  },
  "name": "indo_nli_augment"
}
```

## Running experiments

Notes: please check the script if you need to change some path to adjust your JIANT experimentation path.

To run an experiments, first we need to prepare (tokenize and cache the dataset). This is done using `run_preprocess.sh` script (change `indo_nli` to the new dataset name):
```bash
bash run_preprocess.sh indobenchmark/indobert-large-p2 indo_nli
bash run_preprocess.sh indobenchmark/indobert-lite-base-p2 indo_nli
bash run_preprocess.sh xlm-roberta-large indo_nli
bash run_preprocess.sh bert-base-multilingual-cased indo_nli
```

After that, we can run experiment using `runner.sh` script. To run a set of experiments (4 pretrained models, 3 random seeds) using the same best hyperparameter as `indo_nli`, you can run the following command (change `indo_nli` to the new dataset name):

```bash
bash runner.sh indobenchmark/indobert-lite-base-p2 indo_nli 1
bash runner.sh indobenchmark/indobert-lite-base-p2 indo_nli 11
bash runner.sh indobenchmark/indobert-lite-base-p2 indo_nli 12
bash runner.sh bert-base-multilingual-cased indo_nli 0
bash runner.sh bert-base-multilingual-cased indo_nli 01
bash runner.sh bert-base-multilingual-cased indo_nli 02
bash runner.sh indobenchmark/indobert-large-p2 indo_nli 1
bash runner.sh indobenchmark/indobert-large-p2 indo_nli 11
bash runner.sh indobenchmark/indobert-large-p2 indo_nli 12
bash runner.sh xlm-roberta-large indo_nli 3
bash runner.sh xlm-roberta-large indo_nli 31
bash runner.sh xlm-roberta-large indo_nli 32
```

### Generate predictions

Once all models are trained, you can use `call_predict.py` to generate predictions:

```bash
mkdir experiments\predict_files
python call_predict.py indobenchmark/indobert-lite-base-p2 indo_nli 1
python call_predict.py indobenchmark/indobert-lite-base-p2 indo_nli 11
python call_predict.py indobenchmark/indobert-lite-base-p2 indo_nli 12
python call_predict.py bert-base-multilingual-cased indo_nli 0
python call_predict.py bert-base-multilingual-cased indo_nli 01
python call_predict.py bert-base-multilingual-cased indo_nli 02
python call_predict.py indobenchmark/indobert-large-p2 indo_nli 1
python call_predict.py indobenchmark/indobert-large-p2 indo_nli 11
python call_predict.py indobenchmark/indobert-large-p2 indo_nli 12
python call_predict.py xlm-roberta-large indo_nli 3
python call_predict.py xlm-roberta-large indo_nli 31
python call_predict.py xlm-roberta-large indo_nli 32
```

The predictions will be stored in `experiments\predict_files\[model_name]\[config_best_model]\test_preds.p`. You need to use `torch.load` to read the predictions.
