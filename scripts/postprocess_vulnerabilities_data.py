import json
import os
import argparse
from collections import defaultdict
import difflib

from utils.bug_prompts import DEFAULT_NO_BUG_PROMPT
from utils.constants import NO_BUG_LABEL, DEFAULT_NO_BUG_EXPLANATION, BUG_LABEL


def strip_exact(contract: str) -> str:
    if contract.startswith("```haskell\n"):
        contract = contract[len("```haskell\n") :]
    if contract.startswith("```rust\n"):
        contract = contract[len("```rust\n") :]
    if contract.startswith("```python\n"):
        contract = contract[len("```python\n") :]
    if contract.startswith("```aiken\n"):
        contract = contract[len("```aiken\n") :]
    # elif contract.startswith("```"):
    #    contract = contract[len("```") :]
    # elif contract.startswith("aiken\n"):
    #    contract = contract[len("aiken\n") :]

    if contract.endswith("\n```"):
        contract = contract[: -len("\n```")]
    elif contract.endswith("```"):
        contract = contract[: -len("```")]

    return contract


def postprocess_vulnerabilities_data(
    vulnerabilities_data: str,
    postprocessed_explanation_data: str,
    postprocessed_extract_error: str,
    postprocessed_generate_error: str,
    identical_contract: str,
):
    """
    Postprocess vulnerabilities data.

    Args:
    """
    with open(vulnerabilities_data, "r", encoding="utf-8") as infile, open(
        postprocessed_explanation_data, "w", encoding="utf-8"
    ) as explanation_outfile, open(
        postprocessed_extract_error, "w", encoding="utf-8"
    ) as extract_error_outfile, open(
        postprocessed_generate_error, "w", encoding="utf-8"
    ) as generate_error_outfile, open(
        identical_contract, "w", encoding="utf-8"
    ) as identical_contract_outfile:
        grouped_contracts = defaultdict(
            lambda: {
                "original": None,
                "modified": [],
            }
        )

        for line in infile:
            if not line.strip():
                continue
            entry = json.loads(line)

            contract = entry["contract"]
            processed_contract = strip_exact(contract)
            entry["contract"] = processed_contract
            contract_path = entry.get("path", "")
            label = entry.get("label", "")
            bug_explanation = entry.get("bug_explanation", "")
            # Sort data
            if label == NO_BUG_LABEL:
                assert bug_explanation == DEFAULT_NO_BUG_EXPLANATION
                print("Skipping original contract with no bugs.")
                explanation_outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")
                grouped_contracts[contract_path]["original"] = entry

            else:
                if bug_explanation == "Error generating explanation.":
                    print("found error")
                    generate_error_outfile.write(
                        json.dumps(entry, ensure_ascii=False) + "\n"
                    )
                elif bug_explanation == "No clear explanation found.":
                    extract_error_outfile.write(
                        json.dumps(entry, ensure_ascii=False) + "\n"
                    )
                else:
                    grouped_contracts[contract_path]["modified"].append(entry)

        for path, data in grouped_contracts.items():
            original = data["original"]["contract"]
            modified_list = data["modified"]
            for i, modified in enumerate(modified_list, start=1):
                modified_contract = modified["contract"]

                # Check for identical content
                if original.strip() == modified_contract.strip():
                    identical_contract_outfile.write(
                        json.dumps(modified, ensure_ascii=False) + "\n"
                    )
                else:
                    explanation_outfile.write(
                        json.dumps(modified, ensure_ascii=False) + "\n"
                    )


def main():
    parser = argparse.ArgumentParser(
        description="Postprocess vulnerabilities data to remove invalid entries."
    )
    parser.add_argument(
        "--input-file",
        default="data/vulnerabilities_data.jsonl",
        help="Input vulnerabilities JSONL file (default: data/vulnerabilities_data.jsonl)"
    )
    parser.add_argument(
        "--output-file",
        default="data/postprocessed/postprocessed_good.jsonl",
        help="Output file for valid entries (default: data/postprocessed/postprocessed_good.jsonl)"
    )
    parser.add_argument(
        "--removed-dir",
        default="data/postprocessed/removed",
        help="Directory for removed entries (default: data/postprocessed/removed)"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        return

    output_dir = os.path.dirname(args.output_file)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(args.removed_dir, exist_ok=True)

    postprocessed_extract_error = os.path.join(args.removed_dir, "postprocessed_extract_error.jsonl")
    postprocessed_generate_error = os.path.join(args.removed_dir, "postprocessed_generate_error.jsonl")
    identical_contract = os.path.join(args.removed_dir, "postprocessed_identical_contract.jsonl")

    postprocess_vulnerabilities_data(
        args.input_file,
        args.output_file,
        postprocessed_extract_error,
        postprocessed_generate_error,
        identical_contract,
    )
    print(f"Postprocessed data written to {args.output_file}")
    print(f"Removed entries saved to {args.removed_dir}")


if __name__ == "__main__":
    main()
