from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.random import RandomSummarizer

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
