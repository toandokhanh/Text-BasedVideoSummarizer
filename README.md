<h6 align="left">Author: <a href="https://github.com/toandokhanh">Do Khanh Toan<a/> </h6>
  
# Introduce

The internet's continuous development has led to a rise in the number of videos available online. Efficient organization and categorization based on content are important. Automatic identification of main themes in videos and text processing tasks like extraction, summarization, captions/subtitles, and sentiment analysis have growing applications. These tasks aid searchability, accessibility, and research purposes. Classifying videos by topic facilitates trend analysis and user behavior study. This paper will discuss current methods, challenges, and opportunities in video topic classification and text processing.

# Recommended method
![image](https://github.com/toandokhanh/Text-BasedVideoSummarizer/assets/98395447/441a6f9e-ad57-4f9e-8e7a-285252c108f2)

The recommended method for comprehensive processing and summary of the audio content in the video can be summarized as follows:
1. Extract the audio from the original video file using FFmpeg.
2. Apply noise reduction techniques such as Noisereduce and DeepFillterNet to remove noise from the audio.
3. Convert the processed audio into text using Speech-Recognition.
4. Perform thematic classification of the generated text to identify the subject or domain of the content.
5. Add punctuation to the text using Punctuation 2 to improve readability and comprehension.
6. Check spelling and perform sentence segmentation to correct typos and split the text into separate sentences.
7. Generate a complete summary using summary algorithms, extracting key information and the gist of the text.

This process helps create a concise and accurate version of the original content by removing noise, converting audio to text, improving readability, and summarizing important information.

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

# Parameters
- `-l vi`: Specifies the language for subtitle output, in this case, Vietnamese.
- `-video input.mp4`: Specifies the path or filename of the video file to process.
- `-noise deep`: Selects the noise reduction algorithm to be used, in this case, "deep" (noise or deep)
- `-summary lexrank`: Selects the text summarization algorithm to be used, in this case, "lexrank" (lexrank, textrank, lsa, luhn, random, reduction, edmundson, kl)
- `-sentence 2`: Specifies the number of sentences desired for the summary. In this case, 2 sentences will be extracted for the summary. (yes or no)

      python3 recognize_final.py -l vi -video d.mp4 -noise deep -summary lexrank -sentence 2

# References

1. Sainburg, T., Thielk, M., Gentner, T.Q.: Finding, visualizing, and quantifying
   latent structure across diverse animal vocal repertoires. PLOS Computational
   Biology 16(10), e1008228 (Tháng 10 năm 2020), https://doi.org/10.1371/journal.pcbi.1008228

2. Schroter, H., Escalante-B, A.N., Rosenkranz, T., Maier, A.: Deepfilternet: A low
   complexity speech enhancement framework for full-band audio based on deep filtering.
   In: ICASSP 2022 - 2022 IEEE International Conference on Acoustics, Speech and
   Signal Processing (ICASSP). IEEE (Tháng 5 năm 2022), https://doi.org/10.1109/icassp43922.2022.9747055

3. Anh Vu và Nguyen Dang Duc Tai và Bui Nhat Anh và Vuong Quoc Binh và Doan Viet Dung:
   Underthesea Documentation (2018), https://underthesea.

4. Shen, D., Sun, J.T., Li, H., Yang, Q., Chen, Z.: Document summarization using
   conditional random fields. In: IJCAI. vol. 7, pp. 2862–2867 (2007)

5. Shen, C., Li, T.: Multi-document summarization via the minimum dominating set.
   In: Proceedings of the 23rd International Conference on Computational Linguistics
   (Coling 2010). pp. 984–992 (2010)

6. Wan, X., Li, H., Xiao, J.: Cross-language document summarization based on machine
   translation quality prediction. In: Proceedings of the 48th Annual Meeting of the
   Association for Computational Linguistics. pp. 917–926 (2010)

7. Allahyari, M., Pouriyeh, S., Assefi, M., Safaei, S., Trippe, E.D., Gutierrez, J.B., Kochut, K.:
   Text summarization techniques: a brief survey. arXiv preprint arXiv:1707.02268 (2017)

8. Wu, H.C., Luk, R.W.P., Wong, K.F., Kwok, K.L.: Interpreting tf-idf term weights as
   making relevance decisions. ACM Transactions on Information Systems (TOIS) 26(3), 1–37 (2008)

9. Edmundson, H.P.: New methods in automatic extracting. Journal of the ACM 16(2), 264–285
   (Tháng 4 năm 1969), https://doi.org/10.1145/321510.321519

10. Haghighi, A., Vanderwende, L.: Exploring content models for multi-document summarization.
    In: Proceedings of Human Language Technologies: The 2009 Annual Conference of the
    North American Chapter of the Association for Computational Linguistics. pp. 362–370.
    Association for Computational Linguistics, Boulder, Colorado (Tháng 6 năm 2009),
    https://aclanthology.org/N09-1041


# License



