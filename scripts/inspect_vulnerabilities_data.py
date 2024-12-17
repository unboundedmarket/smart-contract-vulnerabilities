import json
import difflib
from collections import defaultdict


def read_jsonl(filepath: str):
    """Read JSON lines from a file and yield each as a dict."""
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def inspect_contracts(input_file: str, output_diff=False, output_dir="diffs"):
    grouped_contracts = defaultdict(
        lambda: {"original": None, "modified": [], "explanation": [], "bug_prompts": []}
    )

    for obj in read_jsonl(input_file):
        path = obj["path"]
        label = obj["label"]
        code = obj["contract"].splitlines()
        if label == "no_bug":
            grouped_contracts[path]["original"] = code
        elif label == "bug":
            grouped_contracts[path]["modified"].append(code)
            grouped_contracts[path]["explanation"].append(obj["bug_explanation"])
            grouped_contracts[path]["bug_prompts"].append(obj["bug_prompt"])

    # Generate diffs
    for path, data in grouped_contracts.items():
        original = data["original"]
        modified_list = data["modified"]
        explanations = data["explanation"]
        bug_prompts = data["bug_prompts"]

        if original is None:
            # If there's no original, skip
            continue

        for i, modified in enumerate(modified_list, start=1):
            diff = difflib.unified_diff(
                original,
                modified,
                fromfile=f"{path} (original)",
                tofile=f"{path} (modified {i})",
                lineterm="",
            )

            # Print diff
            diff_output = "\n".join(diff)
            print(
                f"====== DIFF for {path} (modified #{i}, prompt {bug_prompts[i-1]}) ======"
            )
            print(diff_output)
            print(f"====== Explanation (modified #{i}) ======")
            print(explanations[i - 1])
            print("==============================================\n")

            # Write diff to file
            if output_diff:
                import os

                os.makedirs(output_dir, exist_ok=True)
                out_path = os.path.join(
                    output_dir, f"{path.replace('/', '_')}_modified_{i}.diff"
                )
                with open(out_path, "w", encoding="utf-8") as diff_file:
                    diff_file.write(diff_output)
                    diff_file.write("\n\n")
                    diff_file.write("====== Original ======\n")
                    diff_file.write("\n".join(original))
                    diff_file.write("\n\n")
                    diff_file.write("====== Modified ======\n")
                    diff_file.write("\n".join(modified))
                    diff_file.write("\n\n")
                    diff_file.write("====== Explanation ======\n")
                    diff_file.write(explanations[i - 1])


def main():
    input_file = "data/postprocessed/postprocessed_good.jsonl"
    inspect_contracts(input_file, output_diff=True)


if __name__ == "__main__":
    main()
