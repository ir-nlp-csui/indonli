# IndoNLI: A Natural Language Inference Dataset for Indonesian

This is a repository for data and code accompanying our EMNLP 2021 paper "IndoNLI: A Natural Language Inference Dataset for Indonesian". The datasets used for our experiments can be found under the `data` directory:
- `indonli`: human-annotated NLI data, split into `train`, `val`, and `test` (`test_lay` and `test_expert`)

   `diagnostic`: subset of examples from test_expert that are annotated with linguistic and logical phenomena
- `translate_train.tar.gz`: MNLI dataset translated to Indonesian (train and dev)
- `translate_train_small.tar.gz`: sampled of `translate_train` used for the `translate_train_small` experiment.

The experiment code can be found under `experiment` directory, please check the related [README](https://github.com/ir-nlp-csui/indonli/blob/main/experiments/README.md) file.


## License

We use premises taken from the Indonesian Wikipedia, news, and Web articles. 

Wikipedia is licensed under Creative Commons Attribution-ShareAlike 3.0 Unported License (CC-BY-SA) and the GNU Free Documentation License (GFDL).

For the news genre, we use premise text from Indonesian PUD and GSD treebanks provided by the Universal Dependencies 2.5 (Zeman et al., 2019) and IndoSum (Kurniawan and Louvan, 2018). Indonesian PUD and GSD treebanks are licensed under Creative Commons Attribution-ShareAlike 3.0 Unported License (CC-BY-SA) and Creative Commons Attribution-ShareAlike 4.0 International License (CC-BY-SA). IndoSum is licensed under Apache License, Version 2.0.


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


