import json

input_file = "data/postprocessed/postprocessed_good.jsonl"
output_file = "data/training/formatted_dataset.jsonl"

with open(input_file, "r") as fin, open(output_file, "w") as fout:
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