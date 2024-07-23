import pandas as pd
import argparse
import os
import re

def parse_multicov_output(input_file, output_file):
    # 读取multicov文件
    df = pd.read_csv(input_file, sep='\t', header=None)
    
    # 为DataFrame命名列
    df.columns = [
        "chrom", "start", "end", "name", "score", "strand",
        "thickStart", "thickEnd", "itemRgb", "blockCount", 
        "blockSizes", "blockStarts", "coverage"
    ]
    
    # 从文件名中提取n值和样本类型并添加到新列
    n_value = determine_n_value(input_file)
    sample_type = determine_sample_type(input_file)
    df['n'] = n_value
    df['sample_type'] = sample_type
    
    # 保存为CSV文件
    df.to_csv(output_file, index=False)
    print(f"Data transformed and saved to {output_file}")

def determine_n_value(file_name):
    # 使用正则表达式从文件名中提取n值
    match = re.search(r'n[0-3]', file_name)
    return match.group(0) if match else 'unknown'

def determine_sample_type(file_name):
    # 使用非捕获组来确保正确匹配样本类型
    match = re.search(r'rCMC_(cont_IP|cont|PE_IP|PE)', file_name)
    return match.group(0) if match else 'unknown'

def process_folder(input_folder, output_folder, merged_file):
    # 检查输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    all_csv_files = []
    
    # 遍历文件夹中的所有TXT文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename.replace(".txt", ".csv"))
            parse_multicov_output(input_file, output_file)
            all_csv_files.append(output_file)
    
    # 合并所有CSV文件
    combined_csv = pd.concat([pd.read_csv(f) for f in all_csv_files])
    
    # 保存合并后的CSV文件
    combined_csv.to_csv(merged_file, index=False)
    print(f"All CSV files merged and saved to {merged_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert all bedtools multicov output TXT files in a folder to CSV format, add new columns n and sample_type, and merge all CSV files.')
    parser.add_argument('input_folder', type=str, help='Input folder path containing the multicov output TXT files.')
    parser.add_argument('output_folder', type=str, help='Output folder path to save the CSV files.')
    parser.add_argument('merged_file', type=str, help='File path to save the merged CSV file.')
    
    args = parser.parse_args()
    process_folder(args.input_folder, args.output_folder, args.merged_file)
