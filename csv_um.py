import pandas as pd
import argparse
from Bio import SeqIO
from tqdm import tqdm

def main(unmapped_csv, input_fastq, output_fastq):
    Counter = 0
    # 读取unmapped.csv文件
    unmapped_df = pd.read_csv(unmapped_csv)

    # 获取未映射的序列集合
    unmapped_sequences = set(unmapped_df['Sequence'].tolist())

    # 用于进度条
    with open(input_fastq, 'r') as f:
        total_records = sum(1 for line in f) // 4

    # 从原始FASTQ文件中提取未映射的reads并写入新的FASTQ文件
    with open(input_fastq, 'r') as in_fq, open(output_fastq, 'w') as out_fq:
        for record in tqdm(SeqIO.parse(in_fq, 'fastq'), total=total_records, desc="Processing"):
            if str(record.seq) in unmapped_sequences:
                SeqIO.write(record, out_fq, 'fastq')
                Counter += 1
                

    print(f"Unmapped reads have been written to {output_fastq}")
    print(Counter, "reads have been written")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract unmapped reads from original fastq file')
    parser.add_argument('-u', '--unmapped_csv', required=True, help='Path to the unmapped.csv file')
    parser.add_argument('-i', '--input_fastq', required=True, help='Path to the original FASTQ file')
    parser.add_argument('-o', '--output_fastq', required=True, help='Path to the output FASTQ file')

    args = parser.parse_args()
    main(args.unmapped_csv, args.input_fastq, args.output_fastq)