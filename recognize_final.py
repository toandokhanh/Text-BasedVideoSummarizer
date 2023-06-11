# nthai: modify 02/05/2023
# dktoan: modify 09/05/2023 update giam nhieu
# dktoan: modify 15/05/2023 update phan loai chu de bang underthesea
# dktoan: modify 03/06/2023 fix bug
# dktoan: modify 07/06/2023 update cac giai thuat tom tat 
# dktoan: modify 08/06/2023 fix bug google_translate 
# original soucre: https://github.com/nestyme/Subtitles-generator

import time
import scipy.io.wavfile as wavfile
import numpy as np
import speech_recognition as sr
import librosa
import argparse
import os
import noisereduce as nr
import soundfile as sf
import ffmpeg
import requests
import soundfile as sf
import re
import sumy_final # sumy_final.py
from sumy_final import lexrank_summarize
from sumy_final import textrank_summarize
from sumy_final import lsa_summarize
from sumy_final import luhn_summarize
from sumy_final import edmundson_summarize
from sumy_final import random_summarize
from sumy_final import reduction_summarize
from sumy_final import kl_summarize
from glob import glob
from noisereduce.generate_noise import band_limited_noise
from regex import F
from datetime import datetime
from underthesea import classify #topic videos
from langdetect import detect
from googletrans import Translator
from gingerit.gingerit import GingerIt
from pyvi import ViTokenizer
from nltk.tokenize import sent_tokenize
import handle_save_log #handle_save_log.py
from handle_save_log import read_video_info
from handle_save_log import count_sentence
import accuracy
from accuracy import calculate_ROUGE


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-video', type=str,
                        help='path to audiofile')
    parser.add_argument('-l','--language', type=str,
                        help='language: vi, en, ru,')
    parser.add_argument('-s','--step_time', type=int, default=55,
                        help='step_time: default : 55')
    parser.add_argument('-noise','--algorithm_noise',
                        help="---> Chọn thuật toán giảm nhiễu",default="no")
    parser.add_argument('-summary','--algorithm_summary',
                        help="---> Chọn thuật toán dùng để tóm tắt văn bản",default="no")
    parser.add_argument('-sentence', '--extra_argument', help="---> số dòng tóm tắt ", default=None)
    # step_time = 50
    arguments = parser.parse_args()
    return arguments

def recognize(wav_filename, args):
    data, s = librosa.load(wav_filename)
    # librosa.output.write_wav('tmp.wav', data, s)
    sf.write('tmp/tmp.wav', data, s)
    y = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
    wavfile.write('tmp/tmp_32.wav', s, y)

    r = sr.Recognizer()
    with sr.AudioFile('tmp/tmp_32.wav') as source:
        audio = r.record(source)  

    print('audiofile loaded')

    try:
        # https://pypi.org/project/SpeechRecognition/
        result = r.recognize_google(audio, language = args.language).lower()
    except sr.UnknownValueError:
        print("cannot understand audio")
        result = ''
        
        # Xóa file wav gốc
        os.remove(wav_filename)
 
    video_name = os.path.splitext(args.video)[0]
    with open( video_name +'_'+args.language+ '.txt', 'w', encoding='utf-8') as f:
        f.write(' {}'.format(result))
    # print(result) 

def get_audio(video):
    os.system('ffmpeg -y  -threads 4 -i {} -f wav -ab 192000 -vn {}'.format(video, 'tmp/current.wav'))
    
# def get_audio(video, name_file):
#     os.system('ffmpeg -y  -threads 4\
#  -i {} -f wav -ab 192000 -vn {}'.format(video, name_file))

def split_into_frames(audiofile, args, folder='samples'):
    data, sr = librosa.load(audiofile)
    print(data)
    print(sr)
    try:
        duration = librosa.get_duration(y=data, sr=sr)
    except:
        duration = librosa.get_duration(audiofile)
    
    #print('video duration, hours: {}'.format(duration/3600))
    print('video duration, seconds: {}'.format(duration))

    # tach moi file dai tam 50s
    
    for i in range(0,int(duration-1),args.step_time):
        tmp_batch = data[(i)*sr:sr*(i+args.step_time)]
        # librosa.output.write_wav('samples/{}.wav'.format(chr(int(i/50)+65)), tmp_batch, sr)
        # librosa.output.write_wav('samples/'+str(int(i/50)+65), y=tmp_batch,sr= sr)

        #import soundfile as sf
        # sap xep theo bang chu cai
        # sf.write( folder +'/{}.wav'.format(chr(int(i/50)+65)), tmp_batch, sr)
        sf.write( folder +'/{}.wav'.format(str(i)), tmp_batch, sr)

def checkfolder (path):
    # path = 'tmp'
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The "+str(path)+" directory is created!")

def noise_reduce(file,file_out):
    y, sr = librosa.load(file)
    reduced_noise = nr.reduce_noise(y = y, sr=sr, thresh_n_mult_nonstationary=2,stationary=False)
    sf.write(file_out,reduced_noise, sr, subtype='PCM_24')
    print('Đang giảm nhiễu với thuật toán noise_reduce!')

def noise_deepfilternet(file,file_out):
    os.system('deepFilter {} -o {}'.format(file,file_out))
    print('Đang giảm nhiễu với thuật toán noise_deepfilternet!')

def rename(filename,newname): 
    os.rename(filename, newname)

def punctuate_text(text, args):
    # Kiểm tra ngôn ngữ đầu vào
    translator = Translator()
    # input_lang = translator.detect(text).lang
    filepath = os.path.splitext(args.video)[0]
    # Nếu ngôn ngữ không phải tiếng Anh, dịch sang tiếng Anh
    if args.language != "en":
        # translation = translator.translate(text, src=args.language, dest="en")
        # text = translation.text
        translated_text = translate_text(text, src=args.language, dest="en")
        text = translated_text.replace(",", " ").replace(".", " ")
        with open(filepath+'_en.txt', 'w', encoding='utf-8') as file:
            file.write(text)

    # Gọi API add các dấu chấm câu
    url = "http://bark.phon.ioc.ee/punctuator"
    payload = {"text": text}
    response = requests.post(url, data=payload)
    result = response.text.strip()

    if '_' in result:
        result = result.replace('_', ' ')
    result = re.sub(r'\s+', ' ', result)
    # Thêm dấu chấm sau câu cuối cùng
    # result = re.sub(r'(\S)(\s*$)', r'\1.', result)
    # Đảm bảo sau dấu chấm luôn có một khoảng trắng
    result = re.sub(r'(\.)(\S)', r'\1 \2', result)
    # parser = GingerIt()
    # corrected_text = ''
    # sentences = result.split('. ')
    # for sentence in sentences:
    #     result = parser.parse(sentence)
    #     corrected_text += result['result'] + '. '
    # Xử lý dấu chấm câu
    sentences = sent_tokenize(result)
    # Xử lý chính tả cho mỗi câu
    # corrected_sentences = []
    # for sentence in sentences:
    #     corrected_sentence = ViTokenizer.tokenize(sentence)
    #     corrected_sentences.append(corrected_sentence)
    
    with open( filepath +'_en_processed_text'+'.txt', 'w', encoding='utf-8') as file:
        for sentence in sentences:
            file.write(sentence + '\n')
    return filepath +'_en_processed_text'+'.txt'

def get_topic(text):
    translator = Translator()
    # Kiểm tra ngôn ngữ của text
    if detect(text) == 'vi':
        text_trans = text
    else:
        # Dịch sang Tiếng Việt nếu đoạn văn bản không phải Tiếng Việt
        text_trans = translator.translate(text, dest='vi').text
        with open(video_name +'_'+args.language+'_vi.txt', 'w', encoding='utf-8') as f:
            f.write(text_trans)
        if os.path.exists(video_name + '_sub_vi.txt'):
            print("Save the sub-vi file successfully")
        else:
            print("Save the sub-vi file failed") 
    topic = '_'.join(classify(text))
    return topic

def save_result_to_file(result, args):
    file_path = os.path.splitext(args.video)[0] #data/video
    result_str = '\n'.join(result)  # Chuyển đổi danh sách thành chuỗi, mỗi phần tử trên một dòng
    # Chỉnh sửa lỗi chính tả
    result_str_corrected = result_str.replace('Vietnam ,', 'Vietnam,')

    # Xóa khoảng trắng trước dấu chấm và dấu phẩy
    result_str_without_spaces = re.sub(r'\s+([.,])', r'\1', result_str_corrected)
    with open(file_path +'_en_processed_text_'+args.algorithm_summary+'_summary.txt', 'w', encoding='utf-8') as file:
        file.write(result_str_without_spaces)
        # video_name+'_en_processed_text'+'.txt'
    result_str_translated = translate_text(result_str_without_spaces, src="en", dest="vi")
    if '_' in result_str_translated:
        result_str_translated = result_str_translated.replace('_', ' ')
    with open(file_path +'_'+args.language+'_'+args.algorithm_summary+'_summary.txt', 'w', encoding='utf-8') as file:
        file.write(result_str_translated)
    print(f"File summary at {file_path +'_'+args.language+'_'+args.algorithm_summary+'_summary.txt',} successfully saved")


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



if __name__ == '__main__':
    from time import gmtime, strftime
    time_text = str(strftime("%Y%m%d_%H%M%S", gmtime())) 
    folder = time_text
    # os.mkdir(folder)
    # os.mkdir(folder)
    checkfolder(folder)
    checkfolder('tmp')

    start = time.time()
    # get argss
    args = get_arguments()
    # reading video
    get_audio(args.video)

    # convert to audio file current
    split_into_frames('tmp/current.wav',args,folder)
    
    # tra ve cac file wav nam trong thu muc tmp
    # files = sorted(glob('tmp/*.wav'))
    #files = sorted(glob('samples/*.wav'))
    
    # files = sorted(glob( folder + '/*.wav'))
    files = sorted(glob( folder + '/*.wav'), key = os.path.getmtime)
    print(files)
    # tao file de luu phu de
    video_name = os.path.splitext(args.video)[0]
    open(video_name +'_'+args.language+'.txt', 'w', encoding = 'utf-8').write('')
    noises = args.algorithm_noise
    if noises:
        # Giảm nhiễu dùng thuật toán deepfilter
        if noises == 'deep':
            print("Use DeepFilterNet")
            for file in files:
                path = file[:file.rindex('/') + 1]
                nameFile = file[file.rindex('/') + 1:file.rindex('.')]
                noise_deepfilternet(file,path)
                rename(path+nameFile+'_DeepFilterNet2.wav',file)
            for file in files:
                recognize(file,args)

            pass
        # Giải thuật giảm nhiễu Noisereduce (không cố định)
        elif noises == 'noise':
            print("Use NoiseReduce")
            for file in files:
                noise_reduce(file,file)
            for file in files:
                recognize(file,args)
        else:
        # Không chọn giải thuật
            # rename(path+name+'.wav',path+newname+'.wav')
            print("Do not use reduce_noise algorithm")
            for file in files:
                recognize(file,args)
            
            pass
    
    
    video_name = os.path.splitext(args.video)[0]
    file_path = video_name +'_'+args.language+'.txt'

    # Mở tệp tin và gán nội dung cho biến text
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        topic = get_topic(text)
        sumamary = args.algorithm_summary
        if sumamary:
            if sumamary == 'lexrank':
                path_processed_text = punctuate_text(text, args)
                result_lexrank = lexrank_summarize(path_processed_text, args.extra_argument)
                save_result_to_file(result_lexrank, args)
            elif sumamary == 'textrank':
                print('Use textRank')  
                path_processed_text = punctuate_text(text, args)
                result_textrank = textrank_summarize(path_processed_text, args.extra_argument)
                save_result_to_file(result_textrank, args)
            elif sumamary == 'lsa':
                print('Use LSA')
                path_processed_text = punctuate_text(text, args)
                result_lsa = lsa_summarize(path_processed_text, args.extra_argument)
                save_result_to_file(result_lsa, args)
            elif sumamary == 'luhn':
                print('Use LUHN')  
                path_processed_text = punctuate_text(text, args)
                result_luhn = luhn_summarize(path_processed_text, args.extra_argument)
                save_result_to_file(result_luhn, args)
            elif sumamary == 'edmundson':
                print('Use Edmundson')
                path_processed_text = punctuate_text(text, args)
                result_edmundson = edmundson_summarize(path_processed_text, args.extra_argument)
                save_result_to_file(result_edmundson, args)
            elif sumamary == 'random':
                print('Use random')  
                path_processed_text = punctuate_text(text, args)
                result_random = random_summarize(path_processed_text, args.extra_argument)
                save_result_to_file(result_random, args)
            elif sumamary == 'kl':
                print('Use KL-sum')  
                path_processed_text = punctuate_text(text, args)
                result_kl = kl_summarize(path_processed_text, args.extra_argument)
                save_result_to_file(result_kl, args)
            elif sumamary == 'reduction':
                print('Use reduction')  
                path_processed_text = punctuate_text(text, args)
                result_reduction = reduction_summarize(path_processed_text, args.extra_argument)
                save_result_to_file(result_reduction, args)
            else:
                print('Do not use summary algorithm') 
                 

    print('The topic of the video is :',topic)
    end = time.time()
    history_file = 'result/history.txt'
    if args.algorithm_summary == 'no':
        path_processed_text = 'None, None, None'
        path_processed_summary_text = 'None, None, None'
    else:    
        # day là file text đã xử lý (gốc)
        path_processed_text = video_name+'_en_processed_text'+'.txt'
        count_sentence_processed_text = count_sentence(path_processed_text)
        path_processed_text = path_processed_text+', '+count_sentence_processed_text
        # day là file tóm tắt dùng để so sash với file gốc
        path_processed_summary_text = video_name +'_en_processed_text_'+args.algorithm_summary+'_summary.txt'
        count_sentence_summary_text = count_sentence(path_processed_summary_text)
        path_processed_summary_text = path_processed_summary_text+', '+count_sentence_summary_text
        # goi ham để tính độ chính xác
        rouge_1_recall, rouge_1_precision, rouge_1_f1, rouge_2_recall, rouge_2_precision, rouge_2_f1, rouge_l_recall, rouge_l_precision, rouge_l_f1 = calculate_ROUGE(video_name+'_en_processed_text'+'.txt', video_name +'_en_processed_text_'+args.algorithm_summary+'_summary.txt')

    if os.path.exists(history_file):
        with open(history_file, 'a') as file:
            count_sentence = count_sentence(video_name+'_en.txt')
            read_video_info = read_video_info(args.video)
            content = folder+', '+args.video+', '+read_video_info+', '+args.language+', '+file_path+', '+count_sentence+', '+path_processed_text+', '+path_processed_summary_text+', '+args.algorithm_noise+', '+args.algorithm_summary+', '+args.extra_argument +', '+format(end - start)+', '+topic+', '+rouge_1_recall+', '+rouge_1_precision+', '+rouge_1_f1+', '+rouge_2_recall+', '+rouge_2_precision+', '+rouge_2_f1+', '+rouge_l_recall+', '+rouge_l_precision+', '+rouge_l_f1
            # print(content)print("Recall:", rouge_1_recall)
            # print("Precision:", rouge_1_precision)
            # print("F1-score:", rouge_1_f1)
            file.write(f'{content} \n')

    # Đã lưu lịch sử chạy code thành công
    
    print('elapsed time: {}'.format(end - start))
    # os.system('rm tmp/*')
