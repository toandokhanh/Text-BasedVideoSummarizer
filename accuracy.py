import argparse
import os
from rouge import Rouge

def calculate_ROUGE(reference_path, summary_path):
    rouge = Rouge()

    with open(reference_path, 'r', encoding='utf-8') as reference_file:
        reference = reference_file.read()

    with open(summary_path, 'r', encoding='utf-8') as summary_file:
        summary = summary_file.read()

    scores = rouge.get_scores(summary, reference, avg=True)

    rouge_1_recall = str(scores['rouge-1']['r'])
    rouge_1_precision = str(scores['rouge-1']['p'])
    rouge_1_f1 = str(scores['rouge-1']['f'])

    rouge_2_recall = str(scores['rouge-2']['r'])
    rouge_2_precision = str(scores['rouge-2']['p'])
    rouge_2_f1 = str(scores['rouge-2']['f'])

    rouge_l_recall = str(scores['rouge-l']['r'])
    rouge_l_precision = str(scores['rouge-l']['p'])
    rouge_l_f1 = str(scores['rouge-l']['f'])

    return rouge_1_recall, rouge_1_precision, rouge_1_f1, rouge_2_recall, rouge_2_precision, rouge_2_f1, rouge_l_recall, rouge_l_precision, rouge_l_f1
# # 
# rouge_1_recall, rouge_1_precision, rouge_1_f1, rouge_2_recall, rouge_2_precision, rouge_2_f1, rouge_l_recall, rouge_l_precision, rouge_l_f1 = calculate_ROUGE('data/en/1_en_processed_text.txt', 'data/en/1_en_processed_text_lexrank_summary.txt')


# print("ROUGE-1:")
# print("Recall:", rouge_1_recall)
# print("Precision:", rouge_1_precision)
# print("F1-score:", rouge_1_f1)
# print("ROUGE-2:")
# print("Recall:", rouge_2_recall)
# print("Precision:", rouge_2_precision)
# print("F1-score:", rouge_2_f1)
# print("ROUGE-L:")
# print("Recall:", rouge_l_recall)
# print("Precision:", rouge_l_precision)
# print("F1-score:", rouge_l_f1)
