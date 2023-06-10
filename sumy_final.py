from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.random import RandomSummarizer
from sumy.summarizers.reduction import ReductionSummarizer
from sumy.summarizers.kl import KLSummarizer
from googletrans import Translator

def lexrank_summarize(file_path, num_sentences):
    with open(file_path, 'r') as file:
        text = file.read()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return [str(sentence) for sentence in summary]

def textrank_summarize(file_path, num_sentences):
    with open(file_path, 'r') as file:
        text = file.read()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return [str(sentence) for sentence in summary]

def lsa_summarize(file_path, num_sentences):
    with open(file_path, 'r') as file:
        text = file.read()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return [str(sentence) for sentence in summary]

def luhn_summarize(file_path, num_sentences):
    with open(file_path, 'r') as file:
        text = file.read()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return [str(sentence) for sentence in summary]

def edmundson_summarize(file_path, num_sentences):
    with open(file_path, 'r') as file:
        text = file.read()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = EdmundsonSummarizer()
    summarizer.bonus_words = ["your", "bonus", "words", "go", "here"]  # Thay thế bằng tập từ khóa bonus thực tế của bạn
    summarizer.stigma_words = ["your", "stigma", "words", "go", "here"]  # Thay thế bằng tập từ khóa stigma thực tế của bạn
    summarizer.null_words = ["your", "null", "words", "go", "here"]  # Thay thế bằng tập từ khóa null thực tế của bạn
    summary = summarizer(parser.document, num_sentences)
    return [str(sentence) for sentence in summary]



def random_summarize(file_path, num_sentences):
    with open(file_path, 'r') as file:
        text = file.read()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = RandomSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return [str(sentence) for sentence in summary]


def reduction_summarize(file_path, num_sentences):
    with open(file_path, 'r') as file:
        text = file.read()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = ReductionSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return [str(sentence) for sentence in summary]

def kl_summarize(file_path, num_sentences):
    with open(file_path, 'r') as file:
        text = file.read()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = KLSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return [str(sentence) for sentence in summary]

def translate_text(text, src, dest):
    translator = Translator()
    chunk_size = 5000  # Kích thước mỗi phần nhỏ (giới hạn của Google Translate API)
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = []

    for chunk in chunks:
        translation = translator.translate(chunk, src=src, dest=dest)
        translated_chunks.append(translation.text)

    translated_text = ' '.join(translated_chunks)
    return translated_text

# lexrank_summarize = lexrank_summarize('data/noise_reduction_processed_text.txt',2)
# print('lexrank_summarize: ',lexrank_summarize)
# result_str = '\n'.join(lexrank_summarize)
# print('result_str: ',result_str)
# # text = result_str.replace(",", " ").replace(".", " ")
# text = result_str
# print('text: ',text)
# translator = Translator()
# translated_text = translate_text(text, src='en', dest='vi')
# print('translated_text: ',translated_text)
