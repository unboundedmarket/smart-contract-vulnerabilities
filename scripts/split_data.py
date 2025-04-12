import json
import random
random.seed(42)

input_file = "data/training/formatted_dataset.jsonl"
train_file = "data/training/train_dataset.jsonl"
test_file = "data/training/test_dataset.jsonl"

with open(input_file, "r") as fin:
    data_list = [json.loads(line) for line in fin]

random.shuffle(data_list)

split_index = int(0.9 * len(data_list))
train_data = data_list[:split_index]
test_data = data_list[split_index:]

with open(train_file, "w") as fout:
    for record in train_data:
        fout.write(json.dumps(record) + "\n")

with open(test_file, "w") as fout:
    for record in test_data:
        fout.write(json.dumps(record) + "\n")
