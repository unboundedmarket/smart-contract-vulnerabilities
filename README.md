# Smart Contract Vulnerabilities

This repository contains the code and tools to create a dataset of Cardano smart contracts with various vulnerabilities. The dataset can be used for analysis, education, or training machine learning models to detect vulnerabilities.

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

### 1. Setup

Clone this repository and navigate to its directory:

```bash
git clone https://github.com/unboundedmarket/smart-contract-vulnerabilities.git
cd smart-contract-vulnerabilities
```

Clone the external smart contracts repository and pull the data:

```bash
git clone https://github.com/unboundedmarket/cardano-smart-contracts.git
cd cardano-smart-contracts
bash scripts/pull_and_update_data.sh
cd ..
```

### 2. Filter Data

The script `scripts/filter_data.py` filters out contracts based on predefined keywords (e.g., utility functions, test cases). Modify the keywords in the script if needed. Then, run the following command:

```bash
python scripts/filter_data.py
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

This script uses GPT-4o to:
1. Augment contracts with specified bugs.
2. Generate detailed explanations for the introduced vulnerabilities.

### 4. Postprocess Data

To clean up the dataset by removing entries where bug or explanation generation failed, run:

```bash
python scripts/postprocess_vulnerabilities_data.py
```

### 5. Inspect Data

Manually inspect the bugs and their explanations using the following command:

```bash
python scripts/inspect_vulnerabilities_data.py
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

`python scripts/prepare_training_data.py`

### 8. Split Dataset

To split the dataset into training and test sets, run:

`python scripts/split_data.py`

### 9. Fine-Tuning

You can now fine-tune your model of choice using the dataset located at `data/training/train_dataset.jsonl`.

We used the [OpenLLaMA 3B v2 model](https://huggingface.co/openlm-research/open_llama_3b_v2) and fine-tuned it using [Axolotl](https://github.com/axolotl-ai-cloud/axolotl).

Our fine-tuned model is available on Hugging Face:  
👉 [unboundedmarket/vulnerabilities-openllama-3b](https://huggingface.co/unboundedmarket/vulnerabilities-openllama-3b)

### 10. Evaluation

After fine-tuning, you can evaluate the model by running:

`python scripts/evaluate.py`

## Additional Information

To view the evaluation results, see:  
`results/vulnerabilities-openllama-3b_evaluation_results.json`

To read more about our fine-tuning approach, check out our detailed write-up [here](https://drive.google.com/file/d/1_L0TezkXa7Gw0-Ya0OQ9X5O46iVLDXyn/view?usp=sharing).
