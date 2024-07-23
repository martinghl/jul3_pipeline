import pandas as pd
import argparse
import re

def parse_info(info_str):
    # 使用正则表达式解析字段信息
    info_dict = {}
    pattern = re.compile(r'(\w+)\s+"([^"]+)"')
    matches = pattern.findall(info_str)
    for match in matches:
        key, value = match
        info_dict[key] = value
    return info_dict

def parse_bedtools_output(input_file, output_file):
    # 读取CSV文件
    df = pd.read_csv(input_file, header=None)
    
    # 打印DataFrame的前几行以确认其结构
    print("DataFrame head:\n", df.head())
    
    # 初始化一个集合来收集所有可能的字段名称
    all_columns = set()
    parsed_data = []

    # 填充解析后的信息
    for _, row in df.iterrows():
        try:
            info_dict = parse_info(row[8])
            parsed_data.append(info_dict)
            all_columns.update(info_dict.keys())
        except KeyError:
            print(f"Skipping row due to missing column: {row}")

    # 将解析后的数据转换为DataFrame
    parsed_df = pd.DataFrame(parsed_data)
    
    # 将原始数据添加到解析后的DataFrame中
    df.columns = ["0", "Transcript", "Type", "4", "5", "6", "7", "8", "Info", "Count"]
    final_df = pd.concat([df[['Transcript', 'Count', 'Type']], parsed_df], axis=1)
    
    # 将所有缺失的列填充为空字符串
    for col in all_columns:
        if col not in final_df.columns:
            final_df[col] = ""
    
    # 指定新的列顺序
    columns = ["Transcript", "Count", "File", "Sample", "Level", "Type"] + sorted(all_columns)
    
    # 填写空列
    final_df["File"] = ""
    final_df["Sample"] = ""
    final_df["Level"] = ""
    
    # 重排序列
    final_df = final_df[columns]
    
    # 保存为CSV文件
    final_df.to_csv(output_file, index=False)
    print(f"Data transformed and saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse BEDTools output data and transform to desired format.')
    parser.add_argument('input_file', type=str, help='Input file path containing the BEDTools output data.')
    parser.add_argument('output_file', type=str, help='Output file path to save the transformed data.')
    
    args = parser.parse_args()
    parse_bedtools_output(args.input_file, args.output_file)
