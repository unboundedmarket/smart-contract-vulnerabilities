import json
import os
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
            contract_language = entry.get("language", "")
            label = entry.get("label", "")
            bug_explanation = entry.get("bug_explanation", "")
            # Sort data
            if label == NO_BUG_LABEL:
                assert bug_explanation == DEFAULT_NO_BUG_EXPLANATION
                print("Skipping original contract with no bugs.")
                explanation_outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")
                grouped_contracts[contract_path]["original"] = entry
                # grouped_contracts[contract_path]["original"] = entry

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
                    # entry["contract"] = processed_contract
                    grouped_contracts[contract_path]["modified"].append(entry)
                    # explanation_outfile.write(
                    #    json.dumps(entry, ensure_ascii=False) + "\n"
                    # )
        for path, data in grouped_contracts.items():
            original = data["original"]
            modified_list = data["modified"]
            for i, modified in enumerate(modified_list, start=1):
                diff = difflib.unified_diff(
                    original["contract"],
                    modified["contract"],
                    fromfile=f"{path} (original)",
                    tofile=f"{path} (modified {i})",
                    lineterm="",
                )

                diff_output = "\n".join(diff)

                filtered_lines = [
                    line for line in diff_output.splitlines() if line.strip()
                ]
                if filtered_lines:
                    explanation_outfile.write(
                        json.dumps(modified, ensure_ascii=False) + "\n"
                    )

                else:
                    identical_contract_outfile.write(
                        json.dumps(modified, ensure_ascii=False) + "\n"
                    )


def main():
    # Paths
    vulnerabilities_data = "data/vulnerabilities_data.jsonl"
    postprocessed_dir = "data/postprocessed"
    os.makedirs(postprocessed_dir, exist_ok=True)
    postprocessed_explanation_data = f"{postprocessed_dir}/postprocessed_good.jsonl"
    postprocessed_extract_error = (
        f"{postprocessed_dir}/postprocessed_extract_error.jsonl"
    )
    postprocessed_generate_error = (
        f"{postprocessed_dir}/postprocessed_generate_error.jsonl"
    )
    identical_contract = f"{postprocessed_dir}/postprocessed_identical_contract.jsonl"
    postprocess_vulnerabilities_data(
        vulnerabilities_data,
        postprocessed_explanation_data,
        postprocessed_extract_error,
        postprocessed_generate_error,
        identical_contract,
    )


if __name__ == "__main__":
    main()
