# tính độ chính xác chi tiết từng file của các thuật toán : python3 comparison_detail.py -o src -s summary
import os
import argparse
from rouge import Rouge
from tabulate import tabulate

def compare_files(goc_dir, tomtat_dir, result_file):
    rouge = Rouge()
    goc_files = os.listdir(goc_dir)
    
    name_method = ['textrank', 'lexrank', 'lsa', 'luhn', 'edmundson', 'random', 'reduction', 'kl']
    
    with open(result_file, "w", encoding="utf-8") as result:
        table = []
        for file in goc_files:
            if file.endswith('_vi.txt'):
                goc_file_path = os.path.join(goc_dir, file)
                for method in name_method:
                    tomtat_file_path = os.path.join(tomtat_dir, file.replace("_vi.txt", f"_{method}_summary.txt"))
                    if os.path.exists(tomtat_file_path):
                        with open(goc_file_path, "r", encoding="utf-8") as goc_file, open(tomtat_file_path, "r", encoding="utf-8") as tomtat_file:
                            goc_text = goc_file.read()
                            tomtat_text = tomtat_file.read()
                            scores = rouge.get_scores(goc_text, tomtat_text)
                            row = []
                            method_label = f"{method.upper()} ({file} vs {file.replace('_vi.txt', f'_{method}_summary.txt')})"
                            row.append(method_label)
                            for score in scores:
                                if (
                                    score['rouge-l']['f'] != 0.0
                                    or score['rouge-l']['p'] != 0.0
                                    or score['rouge-l']['r'] != 0.0
                                ):
                                    row.append(f"f: {score['rouge-l']['f']}\n"
                                               f"p: {score['rouge-l']['p']}\n"
                                               f"r: {score['rouge-l']['r']}")
                                    row.append(f"f: {score['rouge-2']['f']}\n"
                                               f"p: {score['rouge-2']['p']}\n"
                                               f"r: {score['rouge-2']['r']}")
                                    row.append(f"f: {score['rouge-l']['f']}\n"
                                               f"p: {score['rouge-l']['p']}\n"
                                               f"r: {score['rouge-l']['r']}")
                            if len(row) > 1:  # Kiểm tra nếu có ít nhất một kết quả khác 0.0
                                table.append(row)
            else:
                if file.endswith(".txt"):
                    goc_file_path = os.path.join(goc_dir, file)
                    for method in name_method:
                        tomtat_file_path = os.path.join(tomtat_dir, file.replace(".txt", f"_{method}_summary.txt"))
                        if os.path.exists(tomtat_file_path):
                            with open(goc_file_path, "r", encoding="utf-8") as goc_file, open(tomtat_file_path, "r", encoding="utf-8") as tomtat_file:
                                goc_text = goc_file.read()
                                tomtat_text = tomtat_file.read()
                                scores = rouge.get_scores(goc_text, tomtat_text)
                                row = []
                                method_label = f"{method.upper()} ({file} vs {file.replace('.txt', f'_{method}_summary.txt')})"
                                row.append(method_label)
                                for score in scores:
                                    if (
                                        score['rouge-l']['f'] != 0.0
                                        or score['rouge-l']['p'] != 0.0
                                        or score['rouge-l']['r'] != 0.0
                                    ):
                                        row.append(f"f: {score['rouge-l']['f']}\n"
                                                f"p: {score['rouge-l']['p']}\n"
                                                f"r: {score['rouge-l']['r']}")
                                        row.append(f"f: {score['rouge-2']['f']}\n"
                                                f"p: {score['rouge-2']['p']}\n"
                                                f"r: {score['rouge-2']['r']}")
                                        row.append(f"f: {score['rouge-l']['f']}\n"
                                                f"p: {score['rouge-l']['p']}\n"
                                                f"r: {score['rouge-l']['r']}")
                                if len(row) > 1:  # Kiểm tra nếu có ít nhất một kết quả khác 0.0
                                    table.append(row)
        headers = ["Method", "ROUGE - 1", "ROUGE - 2", "ROUGE - L"]
        result.write(tabulate(table, headers=headers, tablefmt="grid"))

def main():
    parser = argparse.ArgumentParser(description='Compare files using ROUGE.')
    parser.add_argument('-o', dest='goc_dir', required=True, help='Path to the directory containing original files.')
    parser.add_argument('-s', dest='tomtat_dir', required=True, help='Path to the directory containing summary files.')
    args = parser.parse_args()
    result_file = "result/result_detail.txt"

    compare_files(args.goc_dir, args.tomtat_dir, result_file)

if __name__ == "__main__":
    main()

