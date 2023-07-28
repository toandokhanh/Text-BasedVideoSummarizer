import summary.sumy_final as sumy_final # sumy_final.py
from summary.sumy_final import lexrank_summarize
from summary.sumy_final import textrank_summarize
from summary.sumy_final import lsa_summarize
from summary.sumy_final import luhn_summarize
from summary.sumy_final import edmundson_summarize
from summary.sumy_final import random_summarize
from summary.sumy_final import reduction_summarize
from summary.sumy_final import kl_summarize
from underthesea import classify


file_path = "data/thunghiem/tt_phapluat.txt"
with open(file_path, 'r') as file:
    text = file.read()
    classify = classify(text)
print(text)
print(classify)

# 0.350316231	1	0.504497843	0.286492053	0.992090142	0.427666838	0.350316231	1	0.504497843 





