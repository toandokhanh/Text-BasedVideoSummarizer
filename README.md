# Text-based video summarization

A 2023 research prototype combining audio extraction, noise reduction, speech recognition, topic tagging and extractive text summarization. It explores LexRank, TextRank, LSA, Luhn, Edmundson, KL and related Sumy methods.

## Pipeline

Video → FFmpeg audio extraction → optional noise reduction → transcript → text preprocessing and topic tagging → extractive summary.

The recognition stage uses an external speech service. Dataset videos and transcripts are not bundled. Configure the original dependencies in an isolated environment if reproducing the study; no environment was installed during maintenance.

## Entry points

Run commands from the repository root. `requirements.txt` and `environment.yml` record the historical environment; FFmpeg and the `deepFilter` executable are external prerequisites for their respective options. The evaluation helper also needs the `rouge` package.

```sh
python3 recognize_final.py -l vi -video data/input.mp4 -noise deep -summary lexrank -sentence 2
```

`recognize_datetime.py` is an earlier pipeline variant. `summary/sumy_final.py` contains summarizers, while `handle/` contains text and result utilities. Speech and punctuation integrations may require adaptation to current provider APIs.

## Evaluation

The original pipeline's ROUGE values measure **overlap with the source transcript**. They must not be presented as ROUGE against human-written reference summaries. The original tables are preserved with this explanation in [historical results](docs/historical-results.md).

For an independent reference, the helper accepts separate reference and hypothesis files:

```sh
python3 accuracy.py --reference data/human-summary.txt --summary data/generated-summary.txt
```

No metrics were recomputed during the 2026 repository cleanup. See [third-party notices](THIRD_PARTY_NOTICES.md) for the source generator and libraries.
