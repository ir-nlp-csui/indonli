# IndoNLI: A Natural Language Inference Dataset for Indonesian

This is a repository for data and code accompanying our EMNLP 2021 paper "IndoNLI: A Natural Language Inference Dataset for Indonesian". The datasets used for our experiments can be found under the `data` directory:
- `indonli`: crowdsourced NLI data, split into train, dev, and test (lay and expert)
- `translate_train.tar.gz`: MNLI dataset translated to Indonesian (train and dev)
- `translate_train_small.tar.gz`: sampled of `translate_train` used for the `translate_train_small` experiment.

The experiment code can be found under `experiment` directory, please check the related [README](https://github.com/ir-nlp-csui/indonli/blob/main/experiments/README.md) file.


## License

We use premises taken from the Indonesian Wikipedia. Wikipedia is licensed under Creative Commons Attribution-ShareAlike 3.0 Unported License (CC-BY-SA) and the GNU Free Documentation License (GFDL).


## Citation

If you use our corpus in your work, please consider citing our paper:
```
@inproceedings{indonli,
    title = "IndoNLI: A Natural Language Inference Dataset for Indonesian",
    author = "Mahendra, Rahmad and Aji, Alham Fikri and Louvan, Samuel and Rahman, Fahrurrozi and Vania, Clara",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    publisher = "Association for Computational Linguistics",
}
```


