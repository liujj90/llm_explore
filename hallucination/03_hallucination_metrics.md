## REID discriminator for hallucination
- Finetuned ELECTRA multi-class classifer (outperforms BERT, RoBERTa, DeBERTa) 


- https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=9467&context=sis_research

- TODO: Check relatedwork for further reading
- IID and OOD datasets for evaluation 
- 

### Machine Metrics used to measure (approximate) hallucination
- ROUGE https://medium.com/nlplanet/two-minutes-nlp-learn-the-rouge-metric-by-examples-f179cc285499
  - ROUGE-N (Appearance scores of n-grams)
  - ROUGE-L (Longest common subsequence)
    -  Precision/recall/f1
  - ROUGE-S (skip gram)
- BLEU https://medium.com/nlplanet/two-minutes-nlp-learn-the-bleu-metric-by-examples-df015ca73a86
- Greedy matching
- Embedding scores (average, extreme)


- Perplexity 
https://towardsdatascience.com/the-relationship-between-perplexity-and-entropy-in-nlp-f81888775ccc
https://thegradient.pub/understanding-evaluation-metrics-for-language-models/


- Metric of quality of generated text 
  - DISTINCT https://aclanthology.org/2022.acl-short.86.pdf


### Experiments
- Different models (70b vs 13b vs mixtral?)
- Develop a larger eval set? 



### BERT/ELECTRA classifier + current metrics 



#### Temperature, RAG and hallucination 
- Does Low temperature = greater hallucination in RAG? Does it simply decrease the reliance on parametric knowledge? 


### FLARE and other recursive methods for mitigation 
- Re-retrieval when hallucination detected 
  - token level
  - dedicated retrieval prompt for masked tokens <could this be a BERT like model output?> 