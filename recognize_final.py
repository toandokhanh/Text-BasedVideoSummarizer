# nthai: modify 02/05/2023
# dktoan: modify 09/05/2023 update giam nhieu
# dktoan: modify 15/05/2023 update phan loai chu de bang underthesea
# original soucre: https://github.com/nestyme/Subtitles-generator
import time
import scipy.io.wavfile as wavfile
import numpy as np
import speech_recognition as sr
import librosa
import argparse
import os
from glob import glob
from noisereduce.generate_noise import band_limited_noise
from regex import F
from datetime import datetime
import noisereduce as nr
import soundfile as sf
import ffmpeg
from underthesea import classify
from langdetect import detect
from googletrans import Translator
# text-rank
from summa import summarizer
# tách câu
from pyvi import ViTokenizer

import soundfile as sf

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
        os.remove(wav_filename)  
    video_name = os.path.splitext(args.video)[0]
    with open( video_name +'_sub.txt', 'a', encoding='utf-8') as f:
        f.write(' {}'.format(result))
   #  return result

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
    open(args.video +'_sub.txt', 'w', encoding = 'utf-8').write('')
    noises = args.algorithm_noise
    if noises:
        # Giảm nhiễu dùng thuật toán deepfilter
        if noises == 'deep':
            print("Sử dụng thuật toán DeepFilterNet để giảm nhiễu")
            path="data/"
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
            print("Sử dụng thuật toán NoiseReduce để giảm nhiễu")
            for file in files:
                noise_reduce(file,file)
            for file in files:
                recognize(file,args)
        else:
        # Không chọn giải thuật
            # rename(path+name+'.wav',path+newname+'.wav')
            print("Không sử dụng thuật toán giảm nhiễu")
            for file in files:
                recognize(file,args)
            pass
    
    end = time.time()
    print('elapsed time: {}'.format(end - start))
    # os.system('rm tmp/*')