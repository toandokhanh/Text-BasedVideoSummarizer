# nthai: modify 02/05/2023
# dktoan: modify 09/05/2023 update giam nhieu
# dktoan: modify 15/05/2023 update phan loai chu de bang underthesea
# dktoan: modify 03/06/2023 fix bug
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



from glob import glob
from noisereduce.generate_noise import band_limited_noise
from regex import F
from datetime import datetime
from underthesea import classify
from langdetect import detect
from googletrans import Translator
from gingerit.gingerit import GingerIt

from pyvi import ViTokenizer
from nltk.tokenize import sent_tokenize
# text-rank
from summa import summarizer
# tách câu
from pyvi import ViTokenizer


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
    with open( video_name +'_sub.txt', 'a', encoding='utf-8') as f:
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
    print('Giảm nhiễu với thuật toán noise_reduce thành công!')

def noise_deepfilternet(file,file_out):
    os.system('deepFilter {} -o {}'.format(file,file_out))
    print('Giảm nhiễu với thuật toán noise_deepfilternet thành công!')

def rename(filename,newname): 
    os.rename(filename, newname)

def punctuate_text(text, args):
    # Kiểm tra ngôn ngữ đầu vào
    translator = Translator()
    # input_lang = translator.detect(text).lang

    # Nếu ngôn ngữ không phải tiếng Anh, dịch sang tiếng Anh
    if args.language != "en":
        translation = translator.translate(text, src=args.language, dest="en")
        text = translation.text

    # Gọi API add các dấu chấm câu
    url = "http://bark.phon.ioc.ee/punctuator"
    payload = {"text": text}
    response = requests.post(url, data=payload)
    result = response.text.strip()

    # Nếu ngôn ngữ đầu vào không phải tiếng Anh, dịch kết quả về ngôn ngữ gốc
    # if input_lang != "en":
    #     translation = translator.translate(result, src="en", dest=input_lang)
    #     result = translation.text
    if '_' in result:
        result = result.replace('_', ' ')
    result = re.sub(r'\s+', ' ', result)
    # Thêm dấu chấm sau câu cuối cùng
    # result = re.sub(r'(\S)(\s*$)', r'\1.', result)
    # Đảm bảo sau dấu chấm luôn có một khoảng trắng
    result = re.sub(r'(\.)(\S)', r'\1 \2', result)
    parser = GingerIt()
    corrected_text = ''
    sentences = result.split('. ')
    for sentence in sentences:
        result = parser.parse(sentence)
        corrected_text += result['result'] + '. '
    # Xử lý dấu chấm câu
    sentences = sent_tokenize(corrected_text)
    # Xử lý chính tả cho mỗi câu
    corrected_sentences = []
    for sentence in sentences:
        corrected_sentence = ViTokenizer.tokenize(sentence)
        corrected_sentences.append(corrected_sentence)
    
    filepath = os.path.splitext(args.video)[0]
    with open( filepath +'_'+args.algorithm_summary+'_processed_text.txt', 'a', encoding='utf-8') as file:
        for sentence in corrected_sentences:
            file.write(sentence + '\n')
    return filepath +'_'+args.algorithm_summary+'_processed_text.txt'

def get_topic(text):
    translator = Translator()
    # Kiểm tra ngôn ngữ của text
    if detect(text) == 'vi':
        text_trans = text
    else:
        # Dịch sang Tiếng Việt nếu đoạn văn bản không phải Tiếng Việt
        text_trans = translator.translate(text, dest='vi').text
        with open(video_name + '_sub_vi.txt', 'w', encoding='utf-8') as f:
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

    # Dịch sang tiếng Việt
    translator = Translator()
    result_str_translated = translator.translate(result_str_without_spaces, dest='vi').text
    if '_' in result_str_translated:
        result_str_translated = result_str_translated.replace('_', ' ')
    with open(file_path +'_'+args.language+'_summary_'+args.algorithm_summary+'.txt', 'w', encoding='utf-8') as file:
        file.write(result_str_translated)
    print(f"File summary at {file_path +'_'+args.language+'_summary_'+args.algorithm_summary+'.txt',} successfully saved")

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
    open(video_name +'_sub.txt', 'w', encoding = 'utf-8').write('')
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
    
    end = time.time()
    video_name = os.path.splitext(args.video)[0]
    file_path = video_name + '_sub.txt'

    # Mở tệp tin và gán nội dung cho biến text
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        sumamary = args.algorithm_summary
        if sumamary:
            if sumamary == 'lexrank':
                print('Use lexRank')  
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
                print('Use edmundson')  
                path_processed_text = punctuate_text(text, args)
                result_edmundson = edmundson_summarize(path_processed_text, args.extra_argument)
                save_result_to_file(result_edmundson, args)
            elif sumamary == 'random':
                print('Use random')  
                path_processed_text = punctuate_text(text, args)
                result_random = random_summarize(path_processed_text, args.extra_argument)
                save_result_to_file(result_random, args)
            else:
                print('Do not use summary algorithm')  

    topic = get_topic(text)
    print('The topic of the video is :',topic)
    print('elapsed time: {}'.format(end - start))
    # os.system('rm tmp/*')
