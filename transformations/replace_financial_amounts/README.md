# Replace Financial amounts 🦎  + ⌨️ → 🐍
This transformation replaces consistently financial amounts throughout a text.
The replacement changes the amount as well as the currency of the financial amount.
The change is consistent in regard to:
- the modifier used to change all amounts of the same currency throughout the text.
  - e.g., the sentence `I own Fred € 20 and I need € 10 for the bus.` might be changed to `I own Fred 2 906.37 Yen and I need 1 453.19 Yen for the bus.`
- the modifier used to change the amounts so that new amounts are relatively close to the original amount.
- the rate used for a change of currency, reflecting the actual bank rate.

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Generated transformations display high similarity to the 
source sentences i.e. the code outputs highly precise generations. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

The accuracy of a RoBERTa model (fine-tuned on IMDB) on a subset of IMDB sentiment dataset = X
The accuracy of the same model on the perturbed set = X

The average bleu score of a distillbert model (fine-tuned on xsum) on a subset of xsum dataset = X
The average bleu score of same model on the pertubed set = X

## Previous Work
1) This perturbation was as part of an augmentation library describe by Regina and al. in (Arxiv 2020):
```bibtex
@article{DBLP:journals/corr/abs-2007-02033,
  author    = {Mehdi Regina and
               Maxime Meyer and
               S{\'{e}}bastien Goutal},
  title     = {Text Data Augmentation: Towards better detection of spear-phishing
               emails},
  journal   = {CoRR},
  volume    = {abs/2007.02033},
  year      = {2020},
  url       = {https://arxiv.org/abs/2007.02033},
  archivePrefix = {arXiv},
  eprint    = {2007.02033},
  timestamp = {Fri, 17 Jul 2020 15:39:46 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2007-02033.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation as a standalone module.
However, combined with other modules, it helps improve the understanding of the context, and generate simple but precise
similar sentences (same semantic similarity).
The transformation outputs financial amounts independently of the format expected for the country.
I.e. we might have 12,38 $ or 12.38 $ output by the generator.
The transformation can only change numeric financial amounts (i.e. it will not handle "two dollars" or "14k euros").
Finally, the transformation is case dependent i.e. 13 usd will not be considered as an amount. 
