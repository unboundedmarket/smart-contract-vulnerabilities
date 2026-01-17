import json
import math
import os
import argparse
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description="Evaluate a fine-tuned model on smart contract vulnerability detection."
)
parser.add_argument(
    "--model-name",
    default="vulnerabilities-openllama-3b",
    help="Model name on Hugging Face (default: vulnerabilities-openllama-3b)"
)
parser.add_argument(
    "--hf-account",
    default="unboundedmarket",
    help="Hugging Face account name (default: unboundedmarket)"
)
parser.add_argument(
    "--test-file",
    default="data/training/test_dataset.jsonl",
    help="Test dataset JSONL file (default: data/training/test_dataset.jsonl)"
)
parser.add_argument(
    "--output-dir",
    default="results",
    help="Output directory for evaluation results (default: results)"
)
args = parser.parse_args()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load fine-tuned model and tokenizer from Hugging Face Hub
model_name_or_path = f"{args.hf_account}/{args.model_name}"

if not os.path.exists(args.test_file):
    print(f"Error: Test file '{args.test_file}' does not exist.")
    exit(1)

os.makedirs(args.output_dir, exist_ok=True)

model = LlamaForCausalLM.from_pretrained(model_name_or_path)
tokenizer = LlamaTokenizer.from_pretrained(model_name_or_path)
model.to(device)
model.eval()

with open(args.test_file, "r") as f:
    test_data = [json.loads(line) for line in f]

predictions_list = []
total_loss = 0.0
correct_count = 0

for sample in tqdm(test_data, desc="Evaluating"):
    prompt = sample["instruction"]
    input_text = sample["input"]
    output_text = sample["output"]
    true_label = sample["label"]
    
    prompt_input = "### Instruction:\n" + prompt + "\n\n### Input:\n" + input_text +"\n\n### Response:\n"
    full_text = prompt_input + output_text
    
    encodings = tokenizer(full_text, return_tensors="pt")
    input_ids = encodings.input_ids.to(device)
    
    prompt_enc = tokenizer(prompt_input, return_tensors="pt")
    prompt_length = prompt_enc.input_ids.shape[1]
    
    labels = input_ids.clone()
    labels[:, :prompt_length] = -100
    
    with torch.no_grad():
        outputs = model(input_ids, labels=labels)
        loss = outputs.loss
    total_loss += loss.item()
    
    gen_encodings = tokenizer(prompt_input, return_tensors="pt").to(device)
    generated_ids = model.generate(
        **gen_encodings,
        max_length=gen_encodings.input_ids.shape[1] + 100,
        do_sample=False
    )
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    if generated_text.startswith(prompt_input):
        predicted_output = generated_text[len(prompt_input):].strip()
    else:
        predicted_output = generated_text.strip()

    print("Output: ", predicted_output)
    if "no bug" in generated_text.lower() or "no bugs" in generated_text.lower():
        pred_label = "no_bug"
    else:
        pred_label = "bug"
    
    is_correct = (pred_label == true_label)
    if is_correct:
        correct_count += 1
    
    predictions_list.append({
        "prompt": prompt,
        "input_text": input_text,
        "output_text": output_text,
        "predicted_output": predicted_output,
        "predicted_label": pred_label,
        "true_label": true_label,
        "loss": loss.item(),
        "correct": is_correct
    })

accuracy = correct_count / len(test_data)
average_loss = total_loss / len(test_data)
perplexity = math.exp(average_loss)

evaluation_results = {
    "metrics": {
        "bug_detection_accuracy": accuracy,
        "average_loss": average_loss,
        "perplexity": perplexity
    },
    "predictions": predictions_list
}


output_results_file = os.path.join(args.output_dir, f"{args.model_name}_evaluation_results.json")
with open(output_results_file, "w") as fout:
    json.dump(evaluation_results, fout, indent=4)

print(f"Evaluation results saved to {output_results_file}")
print(f"Bug Detection Accuracy: {accuracy:.4f}")
print(f"Average Loss: {average_loss:.4f}")
print(f"Perplexity: {perplexity:.4f}")
