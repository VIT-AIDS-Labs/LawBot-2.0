---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:23481
- loss:MultipleNegativesRankingLoss
base_model: nlpaueb/legal-bert-base-uncased
widget:
- source_sentence: Someone circulated defamatory statements about public transit safety.
  sentences:
  - Whoever wrongfully restrains any person in such a manner as to prevent that person
    from proceeding beyond certain limits...
  - Whoever makes, publishes or circulates any statement, rumour or report with intent
    to cause, or which is likely to cause fear or alarm...
  - Whoever wrongfully restrains any person shall be punished.
- source_sentence: A woman negligent doctor during surgery led to patient dying in
    the factory during a quarrel
  sentences:
  - Whoever, with intent to cause or knowing that he is likely to cause wrongful loss
    or damage...
  - Whoever kidnaps or abducts any woman with intent that she may be compelled to
    marry any person...
  - Whoever causes death by rash or negligent act not amounting to culpable homicide.
- source_sentence: I paid for a mobile phone online but never got it delivered.
  sentences:
  - Whoever cheats and thereby dishonestly induces the person deceived to deliver
    any property...
  - Whoever does any act with intention or knowledge to cause death shall be punished
    with imprisonment up to 10 years.
  - Theft committed in any building, tent or vessel used as human dwelling.
- source_sentence: He mishandled celebration gun causing death
  sentences:
  - Whoever, being in any manner entrusted with property or with any dominion over
    property, dishonestly misappropriates...
  - Whoever causes death by doing an act with knowledge that it is likely to cause
    death but without intention of murder...
  - Whoever by words, spoken or written, or by signs, or by visible representation,
    brings or attempts to bring into hatred or contempt...
- source_sentence: A coworker made disrespectful remarks while she walked past at
    the bus stop.
  sentences:
  - Whoever dishonestly receives or retains any stolen property knowing or having
    reason to believe it to be stolen...
  - Whoever, intending to insult the modesty of any woman, utters any word, makes
    any sound or gesture...
  - Whoever imports into India from any country outside India any girl under the age
    of twenty-one years with intent...
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on nlpaueb/legal-bert-base-uncased

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [nlpaueb/legal-bert-base-uncased](https://huggingface.co/nlpaueb/legal-bert-base-uncased). It maps sentences & paragraphs to a 768-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, text classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [nlpaueb/legal-bert-base-uncased](https://huggingface.co/nlpaueb/legal-bert-base-uncased) <!-- at revision 15b570cbf88259610b082a167dacc190124f60f6 -->
- **Maximum Sequence Length:** 512 tokens
- **Output Dimensionality:** 768 dimensions
- **Similarity Function:** Cosine Similarity
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'max_seq_length': 512, 'do_lower_case': False, 'architecture': 'BertModel'})
  (1): Pooling({'word_embedding_dimension': 768, 'pooling_mode_cls_token': False, 'pooling_mode_mean_tokens': True, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False, 'pooling_mode_weightedmean_tokens': False, 'pooling_mode_lasttoken': False, 'include_prompt': True})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```

Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'A coworker made disrespectful remarks while she walked past at the bus stop.',
    'Whoever, intending to insult the modesty of any woman, utters any word, makes any sound or gesture...',
    'Whoever imports into India from any country outside India any girl under the age of twenty-one years with intent...',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 768]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.8765, 0.1315],
#         [0.8765, 1.0000, 0.1523],
#         [0.1315, 0.1523, 1.0000]])
```

<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 23,481 training samples
* Columns: <code>sentence_0</code> and <code>sentence_1</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                        | sentence_1                                                                         |
  |:--------|:----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|
  | type    | string                                                                            | string                                                                             |
  | details | <ul><li>min: 7 tokens</li><li>mean: 15.63 tokens</li><li>max: 46 tokens</li></ul> | <ul><li>min: 12 tokens</li><li>mean: 23.54 tokens</li><li>max: 37 tokens</li></ul> |
* Samples:
  | sentence_0                                                                                                                | sentence_1                                                                                     |
  |:--------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------|
  | <code>Accused took children for begging and kept them under control at home without due caution and fled the scene</code> | <code>Whoever kidnaps a minor to compel them to beg shall be punished.</code>                  |
  | <code>The contractor negligent doctor during surgery led to patient dying</code>                                          | <code>Whoever causes death by rash or negligent act not amounting to culpable homicide.</code> |
  | <code>He wrongfully restrained a person from leaving a room during argument intentionally</code>                          | <code>Whoever wrongfully restrains any person shall be punished.</code>                        |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 20.0,
      "similarity_fct": "cos_sim",
      "gather_across_devices": false
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `num_train_epochs`: 6
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `overwrite_output_dir`: False
- `do_predict`: False
- `eval_strategy`: no
- `prediction_loss_only`: True
- `per_device_train_batch_size`: 8
- `per_device_eval_batch_size`: 8
- `per_gpu_train_batch_size`: None
- `per_gpu_eval_batch_size`: None
- `gradient_accumulation_steps`: 1
- `eval_accumulation_steps`: None
- `torch_empty_cache_steps`: None
- `learning_rate`: 5e-05
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `max_grad_norm`: 1
- `num_train_epochs`: 6
- `max_steps`: -1
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: {}
- `warmup_ratio`: 0.0
- `warmup_steps`: 0
- `log_level`: passive
- `log_level_replica`: warning
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `save_safetensors`: True
- `save_on_each_node`: False
- `save_only_model`: False
- `restore_callback_states_from_checkpoint`: False
- `no_cuda`: False
- `use_cpu`: False
- `use_mps_device`: False
- `seed`: 42
- `data_seed`: None
- `jit_mode_eval`: False
- `bf16`: False
- `fp16`: False
- `fp16_opt_level`: O1
- `half_precision_backend`: auto
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `local_rank`: 0
- `ddp_backend`: None
- `tpu_num_cores`: None
- `tpu_metrics_debug`: False
- `debug`: []
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_prefetch_factor`: None
- `past_index`: -1
- `disable_tqdm`: False
- `remove_unused_columns`: True
- `label_names`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `fsdp`: []
- `fsdp_min_num_params`: 0
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `fsdp_transformer_layer_cls_to_wrap`: None
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `deepspeed`: None
- `label_smoothing_factor`: 0.0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `adafactor`: False
- `group_by_length`: False
- `length_column_name`: length
- `project`: huggingface
- `trackio_space_id`: trackio
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `skip_memory_metrics`: True
- `use_legacy_prediction_loop`: False
- `push_to_hub`: False
- `resume_from_checkpoint`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_private_repo`: None
- `hub_always_push`: False
- `hub_revision`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `include_inputs_for_metrics`: False
- `include_for_metrics`: []
- `eval_do_concat_batches`: True
- `fp16_backend`: auto
- `push_to_hub_model_id`: None
- `push_to_hub_organization`: None
- `mp_parameters`: 
- `auto_find_batch_size`: False
- `full_determinism`: False
- `torchdynamo`: None
- `ray_scope`: last
- `ddp_timeout`: 1800
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `include_tokens_per_second`: False
- `include_num_input_tokens_seen`: no
- `neftune_noise_alpha`: None
- `optim_target_modules`: None
- `batch_eval_metrics`: False
- `eval_on_start`: False
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `eval_use_gather_object`: False
- `average_tokens_across_devices`: True
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Logs
| Epoch  | Step  | Training Loss |
|:------:|:-----:|:-------------:|
| 0.1703 | 500   | 0.3705        |
| 0.3406 | 1000  | 0.1711        |
| 0.5109 | 1500  | 0.1441        |
| 0.6812 | 2000  | 0.1351        |
| 0.8515 | 2500  | 0.1306        |
| 1.0218 | 3000  | 0.1208        |
| 1.1921 | 3500  | 0.1275        |
| 1.3624 | 4000  | 0.118         |
| 1.5327 | 4500  | 0.1245        |
| 1.7030 | 5000  | 0.1281        |
| 1.8733 | 5500  | 0.1376        |
| 2.0436 | 6000  | 0.1109        |
| 2.2139 | 6500  | 0.1236        |
| 2.3842 | 7000  | 0.1212        |
| 2.5545 | 7500  | 0.1255        |
| 2.7248 | 8000  | 0.1196        |
| 2.8951 | 8500  | 0.1179        |
| 3.0654 | 9000  | 0.1179        |
| 3.2357 | 9500  | 0.1251        |
| 3.4060 | 10000 | 0.1188        |
| 3.5763 | 10500 | 0.1151        |
| 3.7466 | 11000 | 0.1186        |
| 3.9169 | 11500 | 0.1103        |
| 4.0872 | 12000 | 0.1182        |
| 4.2575 | 12500 | 0.1156        |
| 4.4278 | 13000 | 0.115         |
| 4.5981 | 13500 | 0.1258        |
| 4.7684 | 14000 | 0.1164        |
| 4.9387 | 14500 | 0.1182        |
| 5.1090 | 15000 | 0.1162        |
| 5.2793 | 15500 | 0.1133        |
| 5.4496 | 16000 | 0.1183        |
| 5.6199 | 16500 | 0.1133        |
| 5.7902 | 17000 | 0.1142        |
| 5.9605 | 17500 | 0.1161        |


### Framework Versions
- Python: 3.12.12
- Sentence Transformers: 5.1.2
- Transformers: 4.57.1
- PyTorch: 2.8.0+cu126
- Accelerate: 1.11.0
- Datasets: 4.0.0
- Tokenizers: 0.22.1

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### MultipleNegativesRankingLoss
```bibtex
@misc{henderson2017efficient,
    title={Efficient Natural Language Response Suggestion for Smart Reply},
    author={Matthew Henderson and Rami Al-Rfou and Brian Strope and Yun-hsuan Sung and Laszlo Lukacs and Ruiqi Guo and Sanjiv Kumar and Balint Miklos and Ray Kurzweil},
    year={2017},
    eprint={1705.00652},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->