import pandas as pd
import argparse

def parse_multicov_output(input_file, output_file):
    # 读取multicov文件
    df = pd.read_csv(input_file, sep='\t', header=None)
    
    # 为DataFrame命名列
    df.columns = [
        "chrom", "start", "end", "name", "score", "strand",
        "thickStart", "thickEnd", "itemRgb", "blockCount", 
        "blockSizes", "blockStarts", "coverage"
    ]
    
    # 保存为CSV文件
    df.to_csv(output_file, index=False)
    print(f"Data transformed and saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert bedtools multicov output to CSV format.')
    parser.add_argument('input_file', type=str, help='Input file path containing the multicov output data.')
    parser.add_argument('output_file', type=str, help='Output file path to save the CSV data.')
    
    args = parser.parse_args()
    parse_multicov_output(args.input_file, args.output_file)
