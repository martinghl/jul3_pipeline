import pandas as pd
import gffutils
from tqdm import tqdm
import argparse
import os

def create_or_load_db(gtf_file, db_file):
    if not os.path.exists(db_file):
        db = gffutils.create_db(gtf_file, dbfn=db_file, force=True, keep_order=True, 
                                disable_infer_genes=True, disable_infer_transcripts=True)
    db = gffutils.FeatureDB(db_file)
    return db

def extract_info(transcript_id, db, search_by='transcript'):
    try:
        if search_by == 'transcript':
            transcript_id = transcript_id.split('.')[0]  # 只用 '.' 之前的部分
            feature = db[transcript_id]
        elif search_by == 'gene':
            feature = db[transcript_id]

        attributes = feature.attributes
        info = {key: attributes.get(key, [''])[0] for key in attributes}
        return pd.Series(info)
    except gffutils.exceptions.FeatureNotFoundError:
        print(f"Error: {search_by} ID {transcript_id} not found in GTF database.")
        return pd.Series({})
    except Exception as e:
        print(f"Error processing {search_by} ID {transcript_id}: {e}")
        return pd.Series({})

def annotate_csv_with_gtf_info(merged_csv, gtf_file, db_file, output_file):
    # 创建或加载GTF文件数据库
    db = create_or_load_db(gtf_file, db_file)
    
    # 读取合并后的CSV文件
    data = pd.read_csv(merged_csv)
    original_columns = data.columns.tolist()

    # 提取信息并添加到DataFrame
    tqdm.pandas(desc="Processing merged CSV data")
    info = data['name'].progress_apply(lambda x: extract_info(x, db, search_by='transcript'))
    data = pd.concat([data, info], axis=1)

    all_columns = original_columns + [col for col in data.columns if col not in original_columns]
    data = data.reindex(columns=all_columns, fill_value='')

    # 保存带有信息的CSV文件
    data.to_csv(output_file, index=False)
    print(f"Annotated data saved to {output_file}")

    # 检查GTF数据库中的所有信息
    all_features = list(db.all_features())
    print(f"Total number of features in GTF database: {len(all_features)}")

    # 保存所有特征信息到文件
    all_features_file = os.path.splitext(output_file)[0] + "_all_features_info.txt"
    with open(all_features_file, 'w') as f:
        for feature in all_features:
            f.write(f"{feature}\n")

    print(f"All feature information saved to {all_features_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Annotate merged CSV file with information from GTF file.')
    parser.add_argument('merged_csv', type=str, help='File path of the merged CSV file.')
    parser.add_argument('gtf_file', type=str, help='File path of the GTF file.')
    parser.add_argument('db_file', type=str, help='File path of the GTF database file.')
    parser.add_argument('output_file', type=str, help='File path to save the annotated CSV file.')

    args = parser.parse_args()
    annotate_csv_with_gtf_info(args.merged_csv, args.gtf_file, args.db_file, args.output_file)
