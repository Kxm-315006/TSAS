import os
import numpy as np
import pandas as pd

print("▶ TSAS raw data generation started...")

os.makedirs("data/raw", exist_ok=True)

np.random.seed(42)
samples = 2000
data = []

for i in range(samples):
    distance = np.random.uniform(50, 1000)
    speed = np.random.uniform(0, 60)
    direction = np.random.choice([0, 1])
    intent = np.random.uniform(0, 1)
    signal = np.random.uniform(0.4, 1.0)

    if distance < 200 and speed > 40 and intent > 0.7:
        severity = "Critical"
    elif distance < 400 and speed > 30 and intent > 0.5:
        severity = "High"
    elif distance < 700 or intent > 0.3:
        severity = "Medium"
    else:
        severity = "Low"

    data.append([distance, speed, direction, intent, signal, severity])

df = pd.DataFrame(
    data,
    columns=["distance", "speed", "direction", "intent", "signal", "severity"]
)

output_path = "data/raw/tsas_raw_data.csv"
df.to_csv(output_path, index=False)

print(f"✅ TSAS raw data generated: {output_path}")
print(f"📊 Samples: {len(df)}")
