#!/usr/bin/env python3

import pandas as pd
import sys

# 检查输入参数
if len(sys.argv) != 3:
    print("Usage: aggregate_counts.py <input_file> <output_file>")
    sys.exit(1)

# 获取输入文件和输出文件路径
input_file = sys.argv[1]
output_file = sys.argv[2]

# 读取 bedtools multicov 的输出文件
df = pd.read_csv(input_file, sep='\t', header=None)

# 添加列名
df.columns = ['chrom', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'attribute', 'count']

# 统计相同序列的计数并保留所有字段
grouped = df.groupby(['chrom', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'attribute']).agg({'count': 'sum'}).reset_index()

# 保存结果为CSV文件
grouped.to_csv(output_file, index=False)

print(f"Aggregated counts with attributes saved to {output_file}")
