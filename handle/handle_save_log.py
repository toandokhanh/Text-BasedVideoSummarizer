from moviepy.editor import VideoFileClip
import nltk
import os


def count_sentence(file_path):
    with open(file_path, 'r') as file:
        # Đọc nội dung từ tệp tin
        content = file.read()

        # Đếm số từ
        so_tu = len(content.split())

        # Đếm số câu
        sentences = nltk.sent_tokenize(content)
        so_cau = len(sentences)

        return str(so_tu) + ', ' + str(so_cau)


def read_video_info(filename):
    """
    Lấy thông tin của video theo đường dẫn filename.
    Return dung_luong +', '+ thoi_gian dưới dạng chuỗi str.
    """

    if os.path.exists(filename):
        clip = VideoFileClip(filename)
        duration = clip.duration
        size = os.stat(filename).st_size / 1024 # Chuyển từ byte sang KB
        return str(int(size)) + ', ' + str(duration)
    else:
        print("Không tìm thấy file!")


