import sys
from rouge import Rouge
from nltk.translate import bleu_score

def calculate_rouge_scores(original_text, summarized_text):
    rouge = Rouge()
    scores = rouge.get_scores(summarized_text, original_text)
    rouge_1_recall = scores[0]['rouge-1']['r']
    rouge_1_precision = scores[0]['rouge-1']['p']
    rouge_1_fscore = scores[0]['rouge-1']['f']

    rouge_2_recall = scores[0]['rouge-2']['r']
    rouge_2_precision = scores[0]['rouge-2']['p']
    rouge_2_fscore = scores[0]['rouge-2']['f']

    reference_tokenized = original_text.split()
    summary_tokenized = summarized_text.split()

    rouge_l_recall = bleu_score.sentence_bleu([reference_tokenized], summary_tokenized, weights=(1, 0, 0))
    rouge_l_precision = rouge_l_recall
    rouge_l_fscore = rouge_l_recall

    # ROUGE-N
    rouge_n_recall = bleu_score.sentence_bleu([reference_tokenized], summary_tokenized)
    rouge_n_precision = rouge_n_recall
    rouge_n_fscore = rouge_n_recall

    # ROUGE-S
    rouge_s_recall = bleu_score.sentence_bleu([summary_tokenized], reference_tokenized)
    rouge_s_precision = rouge_s_recall
    rouge_s_fscore = rouge_s_recall

    return (rouge_1_recall, rouge_1_precision, rouge_1_fscore), (rouge_2_recall, rouge_2_precision, rouge_2_fscore), (rouge_l_recall, rouge_l_precision, rouge_l_fscore), (rouge_n_recall, rouge_n_precision, rouge_n_fscore), (rouge_s_recall, rouge_s_precision, rouge_s_fscore)


if len(sys.argv) < 3:
    print("Vui lòng cung cấp đường dẫn đến tệp tin đầu vào.")
    print("Ví dụ: accuracy.py vanbangoc.txt vanbantomtat.txt")
    sys.exit(1)


original_text_path = sys.argv[1]
summarized_text_path = sys.argv[2]


with open(original_text_path, "r", encoding="utf-8") as file:
    original_text = file.read()

with open(summarized_text_path, "r", encoding="utf-8") as file:
    summarized_text = file.read()

rouge_1_scores, rouge_2_scores, rouge_l_scores, rouge_n_scores, rouge_s_scores = calculate_rouge_scores(original_text, summarized_text)

rouge_1_recall, rouge_1_precision, rouge_1_fscore = rouge_1_scores
rouge_2_recall, rouge_2_precision, rouge_2_fscore = rouge_2_scores
rouge_l_recall, rouge_l_precision, rouge_l_fscore = rouge_l_scores
rouge_n_recall, rouge_n_precision, rouge_n_fscore = rouge_n_scores
rouge_s_recall, rouge_s_precision, rouge_s_fscore = rouge_s_scores

print("ROUGE-1:")
print("Recall:", rouge_1_recall)
print("Precision:", rouge_1_precision)
print("F-Score:", rouge_1_fscore)

print("ROUGE-2:")
print("Recall:", rouge_2_recall)
print("Precision:", rouge_2_precision)
print("F-Score:", rouge_2_fscore)

print("ROUGE-L:")
print("Recall:", rouge_l_recall)
print("Precision:", rouge_l_precision)
print("F-Score:", rouge_l_fscore)

print("ROUGE-N:")
print("Recall:", rouge_n_recall)
print("Precision:", rouge_n_precision)
print("F-Score:", rouge_n_fscore)

print("ROUGE-S:")
print("Recall:", rouge_s_recall)
print("Precision:", rouge_s_precision)
print("F-Score:", rouge_s_fscore)