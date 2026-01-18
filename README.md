# Smart Contract Vulnerabilities

Project Catalyst: 1200174

This repository contains the code and tools to create a dataset of Cardano smart contracts with various vulnerabilities. The dataset can be used for analysis, education, or training machine learning models to detect vulnerabilities.

## Requirements

- Python 3.8 or higher
- OpenAI API key (for vulnerability generation)
- pip (Python package installer)

## Overview

This repository provides scripts and utilities for:
1. **Cloning and setting up a dataset of smart contracts.**
2. **Filtering and preprocessing contracts to select relevant data.**
3. **Augmenting smart contracts with vulnerabilities and generating explanations.**
4. **Postprocessing and inspecting the augmented dataset.**
5. **Easily extending the dataset with new contracts or vulnerability types.**

## File Overview

### Main Directories and Files
- **`data/`**  
  Stores the generated datasets, including filtered contracts and augmented contracts with vulnerabilities.

- **`scripts/`**  
  Contains all scripts for data processing and augmentation:
  - **`scripts/filter_data.py`**  
    Filters contracts based on predefined keywords, creating a cleaned dataset.
  - **`scripts/create_vulnerabilities_data.py`**  
    Generates buggy versions of smart contracts with explanations using GPT-4o.
  - **`scripts/postprocess_vulnerabilities_data.py`**  
    Removes contracts with incomplete bug descriptions.
  - **`scripts/inspect_vulnerabilities_data.py`**  
    Aggregates and displays differences in contracts, allowing manual inspection.
  - **`scripts/utils/bug_prompts.py`**  
    Contains templates for common smart contract vulnerabilities.

## Get Started

All scripts support command-line arguments for flexible configuration. Use `--help` with any script to see available options:

```bash
python scripts/<script_name>.py --help
```

### 1. Setup

#### 1.1 Clone the Repository

Clone this repository and navigate to its directory:

```bash
git clone https://github.com/unboundedmarket/smart-contract-vulnerabilities.git
cd smart-contract-vulnerabilities
```

#### 1.2 Install Dependencies

This project requires Python 3.8 or higher. Install the required packages:

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `openai` - For GPT-4o API calls to generate vulnerabilities
- `tiktoken` - For token counting
- `torch` - For model evaluation
- `transformers` - For loading and evaluating language models
- `tqdm` - For progress bars

**Note:** If you only need data processing scripts (filter, postprocess, prepare, split, inspect), you can install a minimal set:
```bash
pip install openai tiktoken  # For vulnerability generation only
```

For model evaluation, you'll need the full set of dependencies.

#### 1.3 Configure OpenAI API Key

To use the vulnerability generation script, you need an OpenAI API key. You can configure it in two ways:

**Option 1: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="sk-your-actual-api-key-here"
```

Add this to your `~/.bashrc`, `~/.zshrc`, or run it in your terminal session.

**Option 2: Create a secret.py file**
```bash
cp scripts/secret.py.example scripts/secret.py
```

Then edit `scripts/secret.py` and add your OpenAI API key:
```python
OPENAIKEY = "sk-your-actual-api-key-here"
```

**Note:** The `secret.py` file is ignored by git and should never be committed.

#### 1.4 Clone Smart Contracts Dataset

Clone the external smart contracts repository and pull the data:

```bash
git clone https://github.com/unboundedmarket/cardano-smart-contracts.git
cd cardano-smart-contracts
bash scripts/pull_and_update_data.sh
cd ..
```

### 2. Filter Data

The script `scripts/filter_data.py` filters out contracts based on predefined keywords (e.g., utility functions, test cases). Run the following command:

```bash
python scripts/filter_data.py
```

**Command-line options:**
- `--input-dir`: Input directory containing smart contracts (default: `cardano-smart-contracts/data`)
- `--output-file`: Output JSONL file path (default: `data/filtered_data.jsonl`)

Example with custom paths:
```bash
python scripts/filter_data.py --input-dir /path/to/contracts --output-file my_data/filtered.jsonl
```

The script will create a dataset in JSON Lines format within the `data/` directory. Each entry includes:
- The contract code.
- Its original file path.
- The language used.

### 3. Generate Vulnerabilities

To introduce vulnerabilities into the contracts, adjust the prompts in `scripts/utils/bug_prompts.py` as desired. These prompts define the types of bugs to introduce. For reference, see [Common Plutus Security Vulnerabilities](https://www.mlabs.city/blog/common-plutus-security-vulnerabilities).

Run the following command to generate buggy contracts and explanations:

```bash
python scripts/create_vulnerabilities_data.py
```

**Command-line options:**
- `--input-file`: Input JSONL file with filtered contracts (default: `data/filtered_data.jsonl`)
- `--output-file`: Output JSONL file for vulnerabilities data (default: `data/vulnerabilities_data.jsonl`)

This script uses GPT-4o to:
1. Augment contracts with specified bugs.
2. Generate detailed explanations for the introduced vulnerabilities.

### 4. Postprocess Data

To clean up the dataset by removing entries where bug or explanation generation failed, run:

```bash
python scripts/postprocess_vulnerabilities_data.py
```

**Command-line options:**
- `--input-file`: Input vulnerabilities JSONL file (default: `data/vulnerabilities_data.jsonl`)
- `--output-file`: Output file for valid entries (default: `data/postprocessed/postprocessed_good.jsonl`)
- `--removed-dir`: Directory for removed entries (default: `data/postprocessed/removed`)

### 5. Inspect Data

Manually inspect the bugs and their explanations using the following command:

```bash
python scripts/inspect_vulnerabilities_data.py
```

**Command-line options:**
- `--input-file`: Input postprocessed JSONL file (default: `data/postprocessed/postprocessed_good.jsonl`)
- `--output-diffs`: Save diffs to files (flag, default: False)
- `--output-dir`: Output directory for diff files (default: `diffs`)

Example to save diffs:
```bash
python scripts/inspect_vulnerabilities_data.py --output-diffs
```

This script aggregates all augmentations for a given contract, showing:
- The difference between the original contract code and the modified contract code with vulnerabilities.
- Generated explanation.

Manually review and adjust the dataset as needed.

### 6. Extend the Dataset

You can easily extend the dataset by:
1. Adding new repositories to the `cardano-smart-contracts` dataset:
   - Add repository paths to `cardano-smart-contracts/repositories.csv`.
   - Re-run all scripts to incorporate new data.
2. Adding new bug prompts:
   - Edit or add entries in `scripts/utils/bug_prompts.py`.
   - Re-run `python scripts/create_vulnerabilities_data.py`.

The script will detect existing prompts and only extend the dataset with new ones.

### 7. Prepare Training Data

Given the processed dataset, you can adjust the format for training by running:

```bash
python scripts/prepare_training_data.py
```

**Command-line options:**
- `--input-file`: Input postprocessed JSONL file (default: `data/postprocessed/postprocessed_good.jsonl`)
- `--output-file`: Output formatted dataset JSONL file (default: `data/training/formatted_dataset.jsonl`)

### 8. Split Dataset

To split the dataset into training and test sets, run:

```bash
python scripts/split_data.py
```

**Command-line options:**
- `--input-file`: Input formatted dataset JSONL file (default: `data/training/formatted_dataset.jsonl`)
- `--train-file`: Output training dataset JSONL file (default: `data/training/train_dataset.jsonl`)
- `--test-file`: Output test dataset JSONL file (default: `data/training/test_dataset.jsonl`)
- `--split-ratio`: Ratio of training data (default: 0.9)
- `--seed`: Random seed for reproducibility (default: 42)

### 9. Fine-Tuning

You can now fine-tune your model of choice using the dataset located at `data/training/train_dataset.jsonl`.

We used the [OpenLLaMA 3B v2 model](https://huggingface.co/openlm-research/open_llama_3b_v2) and fine-tuned it using [Axolotl](https://github.com/axolotl-ai-cloud/axolotl).

Our fine-tuned model is available on Hugging Face:  
👉 [unboundedmarket/vulnerabilities-openllama-3b](https://huggingface.co/unboundedmarket/vulnerabilities-openllama-3b)

### 10. Evaluation

After fine-tuning, you can evaluate the model by running:

```bash
python scripts/evaluate.py
```

**Command-line options:**
- `--model-name`: Model name on Hugging Face (default: `vulnerabilities-openllama-3b`)
- `--hf-account`: Hugging Face account name (default: `unboundedmarket`)
- `--test-file`: Test dataset JSONL file (default: `data/training/test_dataset.jsonl`)
- `--output-dir`: Output directory for evaluation results (default: `results`)

Example with a different model:
```bash
python scripts/evaluate.py --model-name my-model --hf-account myaccount
```

## Reports & Additional Information

To view the evaluation results, see:  
`results/vulnerabilities-openllama-3b_evaluation_results.json`

A detailed reserach report about smart contract vulnerability scanning can be found [here](/reports/1200174_Vulnerability_Scanner.pdf).

To read more about our fine-tuning approach, check out our detailed write-up [here](/reports/1200174_M3_Fine_Tuning_Vulnerability_Scanner.pdf).


## Acknowledgments

This project is funded by Project Catalyst ([1200174](https://milestones.projectcatalyst.io/projects/1200174/milestones)).
We are very grateful for the support from the Cardano community in developing the vulnerability scanner for Cardano smart contracts.