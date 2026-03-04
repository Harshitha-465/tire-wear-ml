import numpy as np
import pandas as pd

np.random.seed(42)
n = 1200

data = {
    "avg_speed": np.random.randint(30, 120, n),
    "distance_driven": np.random.randint(1000, 50000, n),
    "road_condition": np.random.choice([1, 2, 3], n),  # 1=Poor,3=Good
    "braking_frequency": np.random.randint(1, 10, n),
    "vehicle_load": np.random.randint(200, 900, n),
    "tire_pressure": np.random.uniform(28, 36, n),
    "tire_age_months": np.random.randint(1, 48, n),
    "vehicle_type": np.random.choice([1, 2, 3], n),
    "ambient_temperature": np.random.randint(10, 45, n),
    "driving_style": np.random.choice([1, 2, 3], n),
}

df = pd.DataFrame(data)

# 🧠 Improved wear logic (LOW base)
raw_wear = (
    0.00015 * df["distance_driven"]
    + 0.015 * df["avg_speed"]
    + 0.4 * df["braking_frequency"]
    + 0.001 * df["vehicle_load"]
    - 2.5 * df["road_condition"]
    + 0.2 * abs(df["tire_pressure"] - 32)
    + 0.04 * df["tire_age_months"]
    + 0.4 * df["vehicle_type"]
    + 0.02 * df["ambient_temperature"]
    + 0.8 * df["driving_style"]
    + np.random.normal(0, 0.8, n)
)

# ✅ Normalize to 0–10
raw_wear = np.clip(raw_wear, 0, None)
df["tire_wear"] = 10 * (raw_wear - raw_wear.min()) / (raw_wear.max() - raw_wear.min())

df.to_csv("tire_wear_data.csv", index=False)
print("✅ Dataset generated with normalized wear (0–10)")
