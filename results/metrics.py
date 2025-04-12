import json
from sklearn.metrics import precision_score, recall_score, f1_score

# Load both files
with open("results/open_llama_3b_v2_evaluation_results.json", "r") as f1, \
     open("results/vulnerabilities-openllama-3b_evaluation_results.json", "r") as f2:
    baseline = json.load(f1)
    fine_tuned = json.load(f2)

# Extract predictions and true labels
all_predictions = baseline["predictions"]
y_true = [p["true_label"] for p in all_predictions]
y_pred = [p["predicted_label"] for p in all_predictions]

precision = precision_score(y_true, y_pred, average="weighted", zero_division=0)
recall = recall_score(y_true, y_pred, average="weighted", zero_division=0)
f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

print("Baseline model metrics:")
print(precision, recall, f1)

all_predictions = fine_tuned["predictions"]
y_true = [p["true_label"] for p in all_predictions]
y_pred = [p["predicted_label"] for p in all_predictions]

precision = precision_score(y_true, y_pred, average="weighted", zero_division=0)
recall = recall_score(y_true, y_pred, average="weighted", zero_division=0)
f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

print("Fine-tuned model metrics:")
print(precision, recall, f1)
