# jul3_pipeline
下面是README文件的内容，你可以将其复制到一个名为`README.txt`的文件中：

```
# Gene Data Processing Pipeline

This repository contains scripts for processing and annotating gene data. The scripts are designed to work together to convert, annotate, and aggregate gene expression data from various formats.

## Table of Contents

1. Requirements
2. Scripts Overview
   - agg_counts.py
   - annotate_csv.py
   - bt.py
   - csv_um.py
   - gen_csv.py
   - multicov_folder_to_csv.py
   - read_gtf.py
   - bedtools_conv.py
3. Usage
4. Pipeline Workflow

## 1. Requirements

- Python 3.6 or higher
- Pandas
- gffutils
- tqdm
- argparse
- bedtools
- pysradb

Install dependencies using pip:

```sh
pip install pandas gffutils tqdm argparse pysradb
```

## 2. Scripts Overview

### agg_counts.py

**Function:** Aggregates count data from multiple samples.

**Dependencies:** 
- pandas

**Usage:**
```sh
python agg_counts.py input.csv output.csv
```

### annotate_csv.py

**Function:** Annotates merged CSV file with information from GTF file.

**Dependencies:**
- pandas
- gffutils
- tqdm
- argparse
- os

**Usage:**
```sh
python annotate_csv.py merged.csv annotations.gtf annotations.db annotated.csv
```

### bt.py

**Function:** Performs bedtools operations on gene data files.

**Dependencies:**
- pandas
- os

**Usage:**
```sh
python bt.py input.csv output.csv
```

### csv_um.py

**Function:** Processes and cleans CSV files.

**Dependencies:**
- pandas
- argparse
- os

**Usage:**
```sh
python csv_um.py input.csv output.csv
```

### gen_csv.py

**Function:** Generates final CSV file from processed data.

**Dependencies:**
- pandas
- argparse
- os

**Usage:**
```sh
python gen_csv.py input.csv output.csv
```

### multicov_folder_to_csv.py

**Function:** Converts bedtools multicov output TXT files in a folder to CSV format, adds new columns, and merges all CSV files.

**Dependencies:**
- pandas
- argparse
- os
- re

**Usage:**
```sh
python multicov_folder_to_csv.py input_folder output_folder merged.csv
```

### read_gtf.py

**Function:** Reads GTF file and extracts information.

**Dependencies:**
- pandas
- gffutils
- argparse
- os

**Usage:**
```sh
python read_gtf.py annotations.gtf annotations.db
```

### bedtools_conv.py

**Function:** Converts bedtools output to desired format.

**Dependencies:**
- pandas
- os

**Usage:**
```sh
python bedtools_conv.py input.csv output.csv
```

## 3. Usage

1. Install the dependencies:

```sh
pip install pandas gffutils tqdm argparse pysradb
```

2. Follow the Pipeline Workflow to process your data.

## 4. Pipeline Workflow

1. Convert and merge bedtools multicov output files:

```sh
python multicov_folder_to_csv.py /path/to/input_folder /path/to/output_folder /path/to/merged.csv
```

2. Annotate the merged CSV file with GTF file information:

```sh
python annotate_csv.py /path/to/merged.csv /path/to/annotations.gtf /path/to/annotations.db /path/to/annotated.csv
```

3. Process and clean the annotated CSV file:

```sh
python csv_um.py /path/to/annotated.csv /path/to/processed.csv
```

4. Aggregate count data:

```sh
python agg_counts.py /path/to/processed.csv /path/to/aggregated.csv
```

5. Perform bedtools operations:

```sh
python bt.py /path/to/aggregated.csv /path/to/bt_output.csv
```

6. Convert bedtools output to final format:

```sh
python bedtools_conv.py /path/to/bt_output.csv /path/to/final_output.csv
```

7. Generate the final CSV file:

```sh
python gen_csv.py /path/to/final_output.csv /path/to/report.csv
```

Follow these steps to process your gene data files from initial conversion to final report generation.
```
