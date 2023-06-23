Khi language output là (en)

    (1) en_en.txt => text trong (en.mp4)

    (2) en_en_vi.txt => chuyển sang tiếng việt để phân loại chủ đề bằng Underthesea (Vietnamese NLP Toolkit)
###### https://github.com/undertheseanlp/underthesea

    (3) en_en_processed_text.txt => chuyển sang tiếng anh và xử lý chính tả thêm dấu câu bằng (Punctuator2)
###### https://github.com/ottokart/punctuator2

    (4) en_en_processed_text_lexrank_summary.txt => bản tóm tắt của lexrank (en)
###### https://github.com/miso-belica/sumy

    (5) en_en_lexrank_summary.txt  => bản tóm tắt (vi)

Khi language output là (vi)

    (1) noise_vi.txt => sau khi chuyển video thành văn bản và phân loại chủ đề bằng Underthesea (Vietnamese NLP Toolkit)
###### https://github.com/undertheseanlp/underthesea

    (2) noise_en.txt => từ file (1) chuyển sang ngôn ngữ anh 

    (3) noise_en_processed_text.txt => từ file (2) chuyển qua để xử lý chính tả thêm dấu câu bằng (Punctuator2)
###### https://github.com/ottokart/punctuator2

    (4) noise_en_processed_text_textrank_summary.txt => bản tóm tắt của textrank (en)
###### https://github.com/miso-belica/sumy

    (5) noise_vi_lexrank_summary.txt => bản tóm tắt (vi)

=> Tính độ chính xác bằng cách so sánh file (3) và (4) 

=> File (1) và (5) được show ra