PLUTUS_BUG_PROMPTS = [
    # Each prompt references a known vulnerability from the following list: https://www.mlabs.city/blog/common-plutus-security-vulnerabilities
    # 1. Other redeemer
    (
        "Introduce a bug that allows an unintended redeemer to be used to bypass checks that rely "
        "on a specific redeemer, effectively implementing the 'other-redeemer' vulnerability."
    ),
    # 2. Other token name
    (
        "Introduce a bug that does not properly restrict minted tokens to the intended token name, "
        "allowing arbitrary token names to be minted ('other-token-name')."
    ),
    # 3. Arbitrary datum
    (
        "Introduce a bug allowing arbitrary datum types or values to be locked by the validator, "
        "creating the 'arbitrary-datum' vulnerability."
    ),
    # 4. Unbounded datum
    (
        "Introduce a bug that fails to check the size or structure of the datum, causing a potential "
        "'unbounded-datum' vulnerability."
    ),
]

AIKEN_BUG_PROMPTS = [
    "Introduce a subtle logical error such as inverting a validation condition so that a condition that should fail now succeeds.",
    "Introduce a bug that improperly handles UTxO references, allowing consumption of funds that should remain locked.",
    "Introduce a bug that fails to restrict token names properly, allowing minting of unintended tokens.",
    "Introduce a bug that omits checks for datum sizes, potentially causing unbounded data scenarios.",
    "Introduce a bug that allows unintended redeemers to bypass certain critical validation logic.",
]

OPSHIN_BUG_PROMPTS = [
    "Introduce a logical error in the Python-based OpShin contract that inverts a key conditional check.",
    "Introduce a bug where the contract does not authenticate an input UTxO properly, allowing unauthorized spending.",
    "Introduce a bug that allows arbitrary token names to be minted or spent incorrectly.",
    "Introduce a bug that fails to limit the size of the datum or value locked, leading to resource exhaustion.",
    "Introduce a bug that misses certain checks on redeemers, allowing unintended actions.",
]

DEFAULT_NO_BUG_PROMPT = "no_bug"
