# Historical source-overlap measurements

These are the original reported numbers. The checked-in pipeline compares an extractive summary with the processed source transcript. Precision close to 1 therefore measures overlap with that source; it does not establish agreement with an independently authored reference summary or human judgments. The experiments were not rerun during cleanup, and provenance of every table row has not been reconstructed.

# Experimental results with Vietnamese news
#### ROUGE-1
| Summarizers | Recall  | Precision | F1-score |
|------------|---------|-----------|----------|
| Edmundson  | 0.3747  | 1.0       | 0.5260   |
| K-L        | 0.2756  | 1.0       | 0.4119   |
| Lexrank    | 0.4059  | 1.0       | 0.5574   |
| LSA        | 0.3684  | 1.0       | 0.5125   |
| Luhn       | 0.4658  | 1.0       | 0.6192   |
| Textrank   | 0.4818  | 1.0       | 0.6349   |
#### ROUGE-2
| Summarizers | Recall  | Precision | F1-score |
|------------|---------|-----------|----------|
| Edmundson  | 0.3227  | 0.9952    | 0.4645   |
| K-L        | 0.2336  | 0.9935    | 0.3563   |
| Lexrank    | 0.3563  | 0.9967    | 0.5024   |
| LSA        | 0.3074  | 0.9960    | 0.4403   |
| Luhn       | 0.4189  | 0.9973    | 0.5724   |
| Textrank   | 0.4340  | 0.9971    | 0.5884   |
#### ROUGE-L
| Summarizers | Recall  | Precision | F1-score |
|------------|---------|-----------|----------|
| Edmundson  | 0.3746  | 1.0       | 0.5260   |
| K-L        | 0.2756  | 1.0       | 0.4119   |
| Lexrank    | 0.4059  | 1.0       | 0.5574   |
| LSA        | 0.3684  | 1.0       | 0.5125   |
| Luhn       | 0.4658  | 1.0       | 0.6192   |
| Textrank   | 0.4818  | 1.0       | 0.6349   |

