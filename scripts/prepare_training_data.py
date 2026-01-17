import json
import os
import argparse

parser = argparse.ArgumentParser(
    description="Prepare training data by formatting postprocessed contracts."
)
parser.add_argument(
    "--input-file",
    default="data/postprocessed/postprocessed_good.jsonl",
    help="Input postprocessed JSONL file (default: data/postprocessed/postprocessed_good.jsonl)"
)
parser.add_argument(
    "--output-file",
    default="data/training/formatted_dataset.jsonl",
    help="Output formatted dataset JSONL file (default: data/training/formatted_dataset.jsonl)"
)
args = parser.parse_args()

if not os.path.exists(args.input_file):
    print(f"Error: Input file '{args.input_file}' does not exist.")
    exit(1)

output_dir = os.path.dirname(args.output_file)
if output_dir:
    os.makedirs(output_dir, exist_ok=True)

with open(args.input_file, "r") as fin, open(args.output_file, "w") as fout:
    for line in fin:
        data = json.loads(line)
        contract_code = data.get("contract", "")
        instruction_text = (
            "Determine if the following smart contract contains a bug and explain the bug."
        )
        input_text = (
            contract_code
        )
        output_text = data.get("bug_explanation", "No bugs found.")

        new_data = {
            "instruction": instruction_text,
            "input": input_text,
            "output": output_text,
        }
        new_data.update(data)
        fout.write(json.dumps(new_data) + "\n")

print(f"Formatted training data written to {args.output_file}")