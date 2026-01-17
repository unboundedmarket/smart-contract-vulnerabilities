import json
import os
import argparse
import random

parser = argparse.ArgumentParser(
    description="Split formatted dataset into training and test sets."
)
parser.add_argument(
    "--input-file",
    default="data/training/formatted_dataset.jsonl",
    help="Input formatted dataset JSONL file (default: data/training/formatted_dataset.jsonl)"
)
parser.add_argument(
    "--train-file",
    default="data/training/train_dataset.jsonl",
    help="Output training dataset JSONL file (default: data/training/train_dataset.jsonl)"
)
parser.add_argument(
    "--test-file",
    default="data/training/test_dataset.jsonl",
    help="Output test dataset JSONL file (default: data/training/test_dataset.jsonl)"
)
parser.add_argument(
    "--split-ratio",
    type=float,
    default=0.9,
    help="Ratio of training data (default: 0.9)"
)
parser.add_argument(
    "--seed",
    type=int,
    default=42,
    help="Random seed for reproducibility (default: 42)"
)
args = parser.parse_args()

if not os.path.exists(args.input_file):
    print(f"Error: Input file '{args.input_file}' does not exist.")
    exit(1)

output_dir = os.path.dirname(args.train_file)
if output_dir:
    os.makedirs(output_dir, exist_ok=True)

random.seed(args.seed)

with open(args.input_file, "r") as fin:
    data_list = [json.loads(line) for line in fin]

random.shuffle(data_list)

split_index = int(args.split_ratio * len(data_list))
train_data = data_list[:split_index]
test_data = data_list[split_index:]

with open(args.train_file, "w") as fout:
    for record in train_data:
        fout.write(json.dumps(record) + "\n")

with open(args.test_file, "w") as fout:
    for record in test_data:
        fout.write(json.dumps(record) + "\n")

print(f"Split {len(data_list)} records into {len(train_data)} training and {len(test_data)} test samples")
print(f"Training data written to {args.train_file}")
print(f"Test data written to {args.test_file}")
