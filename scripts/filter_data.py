import os
import json
from typing import Set


def collect_files_by_category(files: Set[str], keywords: Set[str]) -> Set[str]:
    """
    Collect files with filter keywords in their paths.

    Args:
        files (Set[str]): file paths.
        keywords (Set[str]): Keywords to search.

    Returns:
        Set[str]: Filtered set of files.
    """
    return {
        file for file in files if any(keyword in file.lower() for keyword in keywords)
    }


def process_language_directory(
    lang_dir: str,
    lang: str = "ak",
    filter_keywords: dict = {},
    selected_keywords: Set[str] = "validator",
) -> Set[str]:
    """
    Process files for a given language and filter them.

    Args:
        lang_dir (str): Path to language directory.
        lang (str): Language name.
        filter_keywords (dict): Keywords to filter.

    Returns:
        Set[str]: Set of selected files.
    """
    lang_code_files = set()
    for root, _, files in os.walk(lang_dir):
        for file_name in files:
            if file_name.endswith("." + lang):
                lang_code_files.add(os.path.join(root, file_name))
    remaining_files = lang_code_files.copy()
    for _, keywords in filter_keywords.items():
        filtered_files = collect_files_by_category(remaining_files, keywords)
        remaining_files -= filtered_files
    selected_files = collect_files_by_category(remaining_files, selected_keywords)
    return selected_files


def create_dataset_jsonl(
    data_dir: str = "",
    filter_keywords: dict = {},
    selected_keywords: Set[str] = "validator",
    output_file: str = "out.jsonl",
) -> None:
    """
    Process directory to filter files, select files based on keyword and write them to a JSONL file.

    Args:
        data_dir (str): Base dir path
        filter_keywords (dict): Keywords for filtering
        select_keyword (str): Keyword based on which to select data
        output_file (str): Path to the output file
    """
    if not os.path.isdir(data_dir):
        print(f"Error: Directory '{data_dir}' does not exist.")
        return

    with open(output_file, "w") as jsonl_file:
        for lang in os.listdir(data_dir):
            lang_dir = os.path.join(data_dir, lang)
            if not os.path.isdir(lang_dir):
                print(f"Skipping non-directory entry: {lang}")
                continue

            selected_files = process_language_directory(
                lang_dir, lang, filter_keywords, selected_keywords
            )
            for file_path in selected_files:
                try:
                    with open(file_path, "r") as file:
                        file_contents = file.read()
                    json_line = {
                        "contract": file_contents,
                        "path": file_path,
                        "language": lang,
                    }
                    jsonl_file.write(json.dumps(json_line) + "\n")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")


def main():
    data_dir = "cardano-smart-contracts/data"
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/filtered_data.jsonl"

    # selected_keywords = {"validator", "onchain"}
    selected_keywords = {"validator"}
    filter_keywords = {
        "test": {"test"},
        "utility": {"util"},
        "type": {"type"},
        "config": {"config", "cfg"},
        "offchain": {"offchain"},
        "blueprint": {"blueprint"},
        "helper": {"helper"},
    }
    create_dataset_jsonl(data_dir, filter_keywords, selected_keywords, output_file)


if __name__ == "__main__":
    main()
