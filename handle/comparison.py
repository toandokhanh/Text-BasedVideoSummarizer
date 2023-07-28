
# tính độ chính xác trung bình của các thuật toán : python3 comparison.py -o src -s summary
import os
import argparse
from rouge import Rouge
from tabulate import tabulate

def compare_files(goc_dir, tomtat_dir, result_file):
    rouge = Rouge()
    goc_files = os.listdir(goc_dir)
    
    name_method = ['textrank', 'lexrank', 'lsa', 'luhn', 'edmundson', 'random', 'reduction', 'kl']
    
    result_dict = {}
    
    for file in goc_files:
        if file.endswith("_vi.txt"):
            goc_file_path = os.path.join(goc_dir, file)
            for method in name_method:
                tomtat_file_path = os.path.join(tomtat_dir, file.replace("_vi.txt", f"_{method}_summary.txt"))
                if os.path.exists(tomtat_file_path):
                    with open(goc_file_path, "r", encoding="utf-8") as goc_file, open(tomtat_file_path, "r", encoding="utf-8") as tomtat_file:
                        table = []
                        goc_text = goc_file.read()
                        tomtat_text = tomtat_file.read()
                        scores = rouge.get_scores(goc_text, tomtat_text)
                        row = []
                        if method in result_dict:
                            result_dict[method].append(scores)
                        else:
                            result_dict[method] = [scores]
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
        if file.endswith(".txt"):
            goc_file_path = os.path.join(goc_dir, file)
            for method in name_method:
                tomtat_file_path = os.path.join(tomtat_dir, file.replace(".txt", f"_{method}_summary.txt"))
                if os.path.exists(tomtat_file_path):
                    with open(goc_file_path, "r", encoding="utf-8") as goc_file, open(tomtat_file_path, "r", encoding="utf-8") as tomtat_file:
                        table = []
                        goc_text = goc_file.read()
                        tomtat_text = tomtat_file.read()
                        scores = rouge.get_scores(goc_text, tomtat_text)
                        row = []
                        if method in result_dict:
                            result_dict[method].append(scores)
                        else:
                            result_dict[method] = [scores]
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
    with open(result_file, "w", encoding="utf-8") as result:
        table = []
        for method, scores_list in result_dict.items():
            row = []
            row.append(f"{method.upper()}")
            avg_scores = {}
            for scores in scores_list:
                for metric in scores[0].keys():
                    if metric not in avg_scores:
                        avg_scores[metric] = scores[0][metric]
                    else:
                        avg_scores[metric]['f'] += scores[0][metric]['f']
                        avg_scores[metric]['p'] += scores[0][metric]['p']
                        avg_scores[metric]['r'] += scores[0][metric]['r']
            
            for metric in avg_scores.keys():
                avg_scores[metric]['f'] /= len(scores_list)
                avg_scores[metric]['p'] /= len(scores_list)
                avg_scores[metric]['r'] /= len(scores_list)
                row.append(f"f: {avg_scores[metric]['f']}\n"
                           f"p: {avg_scores[metric]['p']}\n"
                           f"r: {avg_scores[metric]['r']}")
            table.append(row)
                
        headers = ["Method", "ROUGE - 1", "ROUGE - 2", "ROUGE - L"]
        result.write(tabulate(table, headers=headers, tablefmt="grid"))

def main():
    parser = argparse.ArgumentParser(description='Compare files using ROUGE.')
    parser.add_argument('-o', dest='goc_dir', required=True, help='Path to the directory containing original files.')
    parser.add_argument('-s', dest='tomtat_dir', required=True, help='Path to the directory containing summary files.')
    args = parser.parse_args()
    result_file = "result/result_averaged.txt"

    compare_files(args.goc_dir, args.tomtat_dir, result_file)

if __name__ == "__main__":
    main()