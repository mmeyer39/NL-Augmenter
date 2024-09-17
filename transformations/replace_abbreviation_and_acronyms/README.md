# Replace Abbreviations and Acronyms 🦎  + ⌨️ → 🐍
This transformation changes abbreviations and acronyms appearing in a text to their expended form and respectively, 
changes expended abbreviations and acronyms appearing in a text to their shorter form.
E.g.: `send this file asap to human resources` might be changed to `send this file as soon as possible to HR`.

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
1) This perturbation was used as part of several augmentation modules used to augment short text and helps with diversity when combined to other perturbation such as back translation (Arxiv 2020):
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
The transformation from the expanded form to the short form might be context dependant 
(this might help improve robustness in some context, e.g.: medical context).
It is relatively easy to provide a new list of accepted acronyms and abbreviations when using the transformation.