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

## Usage

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
