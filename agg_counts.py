import pandas as pd
import argparse

def parse_bedtools_output(input_file):
    data = []
    with open(input_file, 'r') as file:
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) > 8:
                gene_info = {item.split()[0]: item.split()[1].strip('"') for item in fields[8].split(';') if item}
                gene_id = gene_info.get("gene_id", "")
                gene_version = gene_info.get("gene_version", "")
                gene_source = gene_info.get("gene_source", "")
                gene_biotype = gene_info.get("gene_biotype", "")
                transcript = fields[1]
                count = 0  # Placeholder, replace with actual count if available
                file = ""
                sample = ""
                level = ""
                type = ""
                gene_name = ""
                data.append([transcript, count, file, sample, level, type, gene_id, gene_version, gene_name, gene_source, gene_biotype])
    
    return data

def main(input_file, output_file):
    data = parse_bedtools_output(input_file)
    columns = ["Transcript", "Count", "File", "Sample", "Level", "Type", "gene_id", "gene_version", "gene_name", "gene_source", "gene_biotype"]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_file, index=False)
    print(f"Data transformed and saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform BEDTools output data to desired format.')
    parser.add_argument('input_file', type=str, help='Input file path containing BEDTools output data.')
    parser.add_argument('output_file', type=str, help='Output file path to save the transformed data.')
    
    args = parser.parse_args()
    main(args.input_file, args.output_file)
