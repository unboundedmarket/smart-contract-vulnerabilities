PLUTUS_BUG_PROMPTS = [
    # 1. Other redeemer
    "Introduce a bug that allows an unintended redeemer to be used to bypass checks that rely on a specific redeemer.",
    # 2. Other token name
    "Introduce a bug that does not restrict minted tokens to the intended token name, allowing arbitrary tokens to be minted.",
    # 3. Arbitrary datum
    "Introduce a bug allowing arbitrary datum values to be accepted without validation.",
    # 4. Unbounded datum
    "Introduce a bug that does not check the size or structure of the datum, allowing very large data.",
    # 5. Double satisfaction
    "Introduce a bug where two outputs are unintentionally spendable by the same validator condition, allowing double spending.",
    # 6. Incomplete value spent check
    "Introduce a bug that fails to check the full amount or type of value spent in the transaction.",
    # 7. Insecure minting policy
    "Introduce a bug where the minting policy allows minting under overly broad or insecure conditions.",
    # 8. Token duplication
    "Introduce a bug where tokens can be duplicated by replaying the same transaction or misusing the minting policy.",
    # 9. Wrong UTxO assumption
    "Introduce a bug that assumes a specific input or output UTxO exists without checking it explicitly.",
    # 10. Hardcoded assumptions
    "Introduce a bug that relies on hardcoded addresses or values that may change and invalidate the contract's logic.",
    # 11. Missing Signer Validation
    "Introduce a bug that fails to verify the presence of a required signer, allowing unauthorized transactions.",
    # 12. Incorrect Time Validation
    "Introduce a bug that incorrectly handles time range validation, permitting execution outside the intended range.",
    # 13. Incorrect Output Value
    "Introduce a bug that incorrectly calculates or checks output values, allowing unexpected spending or minting.",
    # 14. Unrestricted Script Context
    "Introduce a bug that neglects to fully inspect the script context, allowing transactions to pass unintended checks.",
    # 15. Insufficient Output Checks
    "Introduce a bug that doesn't verify outputs correctly, allowing spending without proper output conditions.",
    # 16. Missing Datum Hash Check
    "Introduce a bug that fails to match datum hashes, allowing manipulation or reuse of datums.",
    # 17. Wrong Comparison Operator
    "Introduce a bug by using the wrong comparison operator (e.g., `<=` instead of `<`), leading to off-by-one errors.",
    # 18. Missing Fee Enforcement
    "Introduce a bug that does not enforce transaction fee checks, allowing transactions with insufficient fees.",
    # 19. Improper Token Burning Logic
    "Introduce a bug allowing tokens to remain unburned when they should have been explicitly burned.",
    # 20. Incorrect List or Map Handling
    "Introduce a bug causing incorrect indexing or accessing of list or map elements, leading to logic errors."
]


AIKEN_BUG_PROMPTS = [
    "Introduce a logical bug by inverting a condition (e.g., using `if not` instead of `if`).",
    "Introduce a bug that skips checking the presence of required UTxOs.",
    "Introduce a bug that allows unrestricted token minting by omitting token name validation.",
    "Introduce a bug that accepts datum without enforcing size or structural constraints.",
    "Introduce a bug that allows redeemer values not intended for that branch of logic.",
    "Introduce a bug by using equality (`==`) where inequality (`!=`) was intended in a critical check.",
    "Introduce a bug that fails to validate the spending script hash, allowing incorrect script usage.",
    "Introduce a bug that neglects to verify that the correct signer (pubkey) is present in the transaction.",
    "Introduce a bug that checks the wrong field of the redeemer or datum, leading to logic mismatch.",
    "Introduce a bug that misuses the time range constraints (`valid_from`, `valid_to`), allowing invalid execution timing.",
    "Introduce a bug causing off-by-one errors in list indexing or loops.",
    "Introduce a bug allowing unauthorized access by omitting critical signature checks.",
    "Introduce a bug where numeric overflows or underflows are possible due to missing bounds checks.",
    "Introduce a bug incorrectly validating the number or type of inputs or outputs in transactions.",
    "Introduce a bug that fails to correctly handle negative values or unexpected numeric inputs.",
    "Introduce a bug where transaction deadlines are incorrectly interpreted or validated.",
    "Introduce a bug allowing replay attacks due to missing uniqueness checks on transaction IDs.",
    "Introduce a bug that incorrectly handles optional fields, causing unintended acceptance of invalid data.",
    "Introduce a bug causing incorrect reference or datum hash validation, allowing misuse of datums.",
    "Introduce a bug by improperly sequencing validation checks, allowing premature success of validation.",
]


OPSHIN_BUG_PROMPTS = [
    "Introduce a bug where a condition check is inverted (e.g., `if not valid:` instead of `if valid:`).",
    "Introduce a bug where required input UTxOs are not authenticated, allowing unauthorized spending.",
    "Introduce a bug that allows any token name to be minted, bypassing intended minting restrictions.",
    "Introduce a bug that ignores checks on datum size or type, accepting arbitrary input.",
    "Introduce a bug that lets any redeemer bypass logic meant for a specific redeemer.",
    "Introduce a bug by using hardcoded values that could become invalid (e.g., a fixed address or token name).",
    "Introduce a bug that mishandles loop conditions, causing infinite loops or missed validations.",
    "Introduce a bug where list or dictionary access is not properly checked, causing key errors or logic failure.",
    "Introduce a bug where transaction signatures are not verified, allowing unsigned transactions to pass.",
    "Introduce a bug that misuses PlutusTx constraint builders, failing to constrain outputs properly.",
    "Introduce a bug that allows arithmetic overflow due to missing numeric validation.",
    "Introduce a bug skipping essential checks on transaction output amounts, enabling incorrect spending.",
    "Introduce a bug that incorrectly implements deadline or time constraints, causing incorrect transaction validity.",
    "Introduce a bug where conditions using `and` or `or` operators are incorrectly grouped, causing logical errors.",
    "Introduce a bug that mishandles input UTxO validation logic, allowing unintended UTxOs to be spent.",
    "Introduce a bug causing data serialization/deserialization errors due to incorrect handling of structured data.",
    "Introduce a bug incorrectly handling optional datum fields, leading to logic bypass or errors.",
    "Introduce a bug neglecting to enforce strict token burning rules, causing tokens to persist unintentionally.",
    "Introduce a bug allowing replay transactions due to missing checks on unique identifiers or transaction metadata.",
    "Introduce a bug mismanaging execution budget constraints, allowing overly expensive scripts to execute without checks.",
]

DEFAULT_NO_BUG_PROMPT = "no_bug"
