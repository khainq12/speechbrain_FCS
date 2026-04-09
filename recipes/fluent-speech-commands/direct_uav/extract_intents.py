import pandas as pd
import re

csv_path = "../direct/results/BPE51/1986/save/train.csv"
df = pd.read_csv(csv_path)

unique_intents = set()

for sem in df['semantics']:
    match = re.findall(r'"action:"\s*"([^"]+)"\s*\|\s*"object":\s*"([^"]+)"\s*\|\s*"location":\s*"([^"]+)"', sem)
    if match:
        unique_intents.add(match[0])

print(f"Tìm thấy {len(unique_intents)} intents duy nhất trong FSC:\n")
for action, obj, loc in sorted(list(unique_intents)):
    print(f'    ("{action}", "{obj}", "{loc}"): {"# TODO:Mapped_UAV_Dict_Here"},')