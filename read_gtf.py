import pandas as pd
import gffutils
from tqdm import tqdm

# 路径
cdna_file = "/data/home/liguanghao/jul3/all_cdna_data.csv"
dna_file = "/data/home/liguanghao/jul3/all_dna_data.csv"
gtf_file = "/data/home/liguanghao/jul3/Rattus_norvegicus.mRatBN7.2.112.gtf"
cdna_data = pd.read_csv(cdna_file)
dna_data = pd.read_csv(dna_file)

original_cdna_columns = cdna_data.columns.tolist()
original_dna_columns = dna_data.columns.tolist()

# 创建并保存GTF文件数据库
db_file = '/data/home/liguanghao/jul3/Rattus_norvegicus.mRatBN7.2.112.db'
db = gffutils.create_db(gtf_file, dbfn=db_file, force=True, keep_order=True, 
                        disable_infer_genes=True, disable_infer_transcripts=True)

# 加载GTF文件数据库
db = gffutils.FeatureDB(db_file)

# 从GTF数据库中提取信息
def extract_info(transcript_id, search_by='transcript'):
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

# cDNA
tqdm.pandas(desc="Processing cDNA data")
cdna_info = cdna_data['Transcript'].progress_apply(lambda x: extract_info(x, search_by='transcript'))
cdna_data = pd.concat([cdna_data, cdna_info], axis=1)

# DNA
tqdm.pandas(desc="Processing DNA data")
dna_info = dna_data['Transcript'].progress_apply(lambda x: extract_info(x, search_by='gene'))
dna_data = pd.concat([dna_data, dna_info], axis=1)

all_cdna_columns = original_cdna_columns + [col for col in cdna_data.columns if col not in original_cdna_columns]
all_dna_columns = original_dna_columns + [col for col in dna_data.columns if col not in original_dna_columns]

cdna_data = cdna_data.reindex(columns=all_cdna_columns, fill_value='')
dna_data = dna_data.reindex(columns=all_dna_columns, fill_value='')

cdna_data.to_csv("/data/home/liguanghao/jul3/cdna_data_with_info.csv", index=False)
dna_data.to_csv("/data/home/liguanghao/jul3/dna_data_with_info.csv", index=False)

print("cDNA和DNA数据已成功保存。")

# 检查GTF数据库中的所有信息
all_features = list(db.all_features())
print(f"Total number of features in GTF database: {len(all_features)}")

# 保存所有特征信息到文件
all_features_file = "/data/home/liguanghao/jul3/all_features_info.txt"
with open(all_features_file, 'w') as f:
    for feature in all_features:
        f.write(f"{feature}\n")

print(f"所有特征信息已保存到 {all_features_file}")
