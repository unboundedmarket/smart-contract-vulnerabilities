import json
import openai
import os
import tiktoken
import argparse

# Try to get API key from environment variable first, then fallback to secret.py
try:
    from secret import OPENAIKEY
except ImportError:
    OPENAIKEY = os.environ.get('OPENAI_API_KEY')
    if not OPENAIKEY:
        raise ValueError(
            "OpenAI API key not found. Please either:\n"
            "1. Set the OPENAI_API_KEY environment variable, or\n"
            "2. Create scripts/secret.py with: OPENAIKEY = 'your-api-key-here'\n"
            "   (You can copy scripts/secret.py.example as a template)"
        )

from utils.bug_prompts import (
    AIKEN_BUG_PROMPTS,
    OPSHIN_BUG_PROMPTS,
    PLUTUS_BUG_PROMPTS,
    DEFAULT_NO_BUG_PROMPT,
)

from utils.constants import (
    LANGUAGES,
    DEFAULT_NO_BUG_EXPLANATION,
    BUG_LABEL,
    NO_BUG_LABEL,
)

openai.api_key = OPENAIKEY
MAX_PROMPT_TOKENS = 4096


def estimate_token_count(prompt: str, code: str) -> int:
    """Estimate token count using tiktoken."""
    enc = tiktoken.encoding_for_model("gpt-4o")
    return len(enc.encode(prompt + code))


def get_bug_prompts_for_language(lang):
    if lang == "hs":
        return PLUTUS_BUG_PROMPTS
    elif lang == "ak":
        return AIKEN_BUG_PROMPTS
    elif lang == "py":
        return OPSHIN_BUG_PROMPTS
    else:
        raise ValueError(f"Unknown language: {lang}")


def call_gpt4o_api(original_code, prompt, contract_language):
    system_msg = (
        "You are a helpful assistant. You will receive a smart contract and a request to introduce exactly one subtle bug. "
        "Return the modified code first, then on a new line write 'Explanation:' followed by a brief, objective description of the bug. "
        "Do not highlight or explicitly mark the bug in the code, or mention that you introduced it. "
        "Present the bug as if it naturally exists in the modified code."
    )

    user_msg = (
        f"You are given a {LANGUAGES[contract_language]} smart contract. "
        "Introduce exactly one subtle bug according to the following instruction:\n\n"
        f"{prompt}\n\n"
        "The modified code should remain syntactically valid and the bug should be subtle but impactful. "
        "Return the modified code first, then on a new line write 'Explanation:' followed by a brief description of what the bug does."
        "\n\nOriginal code:\n" + original_code
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=6500,
            temperature=0,
        )

        content = response.choices[0].message.content
        if "Explanation:" in content:
            print("Found explanation in response")
            parts = content.split("Explanation:", 1)
            modified_code = parts[0].strip()
            bug_explanation = parts[1].strip()
            return {"modified_code": modified_code, "bug_explanation": bug_explanation}

        else:
            # default explanation for postprocessing
            print("Couldn't find explanation in response")
            modified_code = content.strip()
            bug_explanation = "No clear explanation found."
            return {}

    except Exception as e:
        print(f"Error generating bug: {e}")
        return {}


def load_processed_files(output_file_path):
    """Loads the list of already processed files."""
    processed_files = {}
    if os.path.exists(output_file_path):
        with open(output_file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    path = data.get("path", "")
                    bug_prompt = data.get("bug_prompt", "")
                    if path and bug_prompt:
                        if not path in processed_files:
                            processed_files[path] = {bug_prompt: data}
                        else:
                            processed_files[path].update({bug_prompt: data})

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
    return processed_files


def process_contracts(input_file, output_file, processed_files):
    with open(input_file, "r", encoding="utf-8") as infile, open(
        output_file, "a", encoding="utf-8" 
    ) as outfile:

        for line in infile:
            if not line.strip():
                continue
            entry = json.loads(line)

            original_contract = entry["contract"]
            contract_path = entry.get("path", "")
            contract_language = entry.get("language", "")

            if not contract_path or not contract_language:
                continue

            if contract_path in processed_files and DEFAULT_NO_BUG_PROMPT in processed_files[contract_path]:
                print(f"Skipping already processed original contract file: {contract_path}")
            else:
                print(f"Processing original contract: {contract_path}")
                original_output = {
                    "contract": original_contract,
                    "bug_explanation": DEFAULT_NO_BUG_EXPLANATION,
                    "label": NO_BUG_LABEL,
                    "path": contract_path,
                    "language": contract_language,
                    "bug_prompt": DEFAULT_NO_BUG_PROMPT,
                }
                outfile.write(json.dumps(original_output, ensure_ascii=False) + "\n")

            bug_prompts = get_bug_prompts_for_language(contract_language)
            for bug_prompt in bug_prompts:
                if contract_path in processed_files and bug_prompt in processed_files[contract_path]:
                    print(f"Skipping already processed bug prompt for contract file: {contract_path}")
                    continue

                print(f"Processing bug prompt: {bug_prompt}")
                estimated_tokens = estimate_token_count(bug_prompt, original_contract)
                if estimated_tokens > MAX_PROMPT_TOKENS:
                    print(f"Skipping contract due to length ({estimated_tokens} tokens): {contract_path}")
                    continue

                response = call_gpt4o_api(original_contract, bug_prompt, contract_language)
                if "modified_code" in response and "bug_explanation" in response:
                    bug_output = {
                        "contract": response["modified_code"],
                        "bug_explanation": response["bug_explanation"],
                        "label": BUG_LABEL,
                        "path": contract_path,
                        "language": contract_language,
                        "bug_prompt": bug_prompt,
                    }
                    outfile.write(json.dumps(bug_output, ensure_ascii=False) + "\n")



def main():
    parser = argparse.ArgumentParser(
        description="Generate buggy versions of smart contracts with explanations using GPT-4o."
    )
    parser.add_argument(
        "--input-file",
        default="data/filtered_data.jsonl",
        help="Input JSONL file with filtered contracts (default: data/filtered_data.jsonl)"
    )
    parser.add_argument(
        "--output-file",
        default="data/vulnerabilities_data.jsonl",
        help="Output JSONL file for vulnerabilities data (default: data/vulnerabilities_data.jsonl)"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        return

    output_dir = os.path.dirname(args.output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    processed_files = load_processed_files(args.output_file)
    process_contracts(args.input_file, args.output_file, processed_files)
    print(f"Vulnerabilities data written to {args.output_file}")


if __name__ == "__main__":
    main()
