# Winogrande 

Version 1.0 (Aug 5th, 2019)

- - - 

## Data

    .
    ├── train-labels.lst		# answer labels for (debiased) training set
    ├── train.jsonl				# (debiased) training set
    ├── train_all-labels.lst	# answer labels for training set
    ├── train_all.jsonl			# training set 
    ├── dev-labels.lst			# answer labels for development set
    ├── dev.jsonl				# development set
    ├── test.jsonl				# test set
    └── eval.py					# evaluation script
    
You can use `train`, `train_all` for training models and `dev` for validation.
Please note that labels are not included in `test.jsonl`. To evaluate your models, make a submission to our leaderboard (`https://leaderboard.allenai.org/winogrande/submissions/public`).


## Evaluation

You can use `eval.py` for evaluation on the dev split, which yields `metrics.json`. 

    e.g. python eval.py --preds_file ./YOUR_PREDICTIONS.lst --labels_file ./dev-labels.lst

You can submit your predictions (on the `test` set) to the leaderboard. (`https://leaderboard.allenai.org/winogrande/submissions/public`)

    
## Reference
If you use this dataset, please cite the following paper:

	@article{sakaguchi2019winogrande,
	    title={WINOGRANDE: An Adversarial Winograd Schema Challenge at Scale},
	    author={Sakaguchi, Keisuke and Bras, Ronan Le and Bhagavatula, Chandra and Choi, Yejin},
	    journal={arXiv preprint arXiv:1907.10641},
	    year={2019}
	}


## License 

Winogrande is licensed under the Apache License 2.0.