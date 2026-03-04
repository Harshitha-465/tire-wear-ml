import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
import joblib

# ---------------- LOAD DATA ----------------
df = pd.read_csv("tire_wear_data.csv")

# Separate features and target
X = df.drop("tire_wear", axis=1)
y = df["tire_wear"]

# ---------------- FEATURE GROUPS ----------------

# Numerical features (need scaling)
numeric_features = [
    "avg_speed",
    "distance_driven",
    "braking_frequency",
    "vehicle_load",
    "tire_pressure",
    "tire_age_months",
    "ambient_temperature",
]

# Ordinal features (already encoded, keep as-is)
ordinal_features = [
    "road_condition",   # 1=Poor, 2=Average, 3=Good
    "vehicle_type",     # 0=Sedan, 1=SUV, 2=Truck
    "driving_style",    # 0=Smooth, 1=Normal, 2=Aggressive
]

# ---------------- PREPROCESSOR ----------------
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("ord", "passthrough", ordinal_features),
    ],
    remainder="drop"
)

# ---------------- FIT & TRANSFORM ----------------
X_processed = preprocessor.fit_transform(X)

# Convert to DataFrame (for inspection / debugging)
processed_feature_names = numeric_features + ordinal_features
X_processed_df = pd.DataFrame(
    X_processed,
    columns=processed_feature_names
)

# Add target back
X_processed_df["tire_wear"] = y.values

# ---------------- SAVE OUTPUTS ----------------
X_processed_df.to_csv("tire_wear_processed.csv", index=False)
joblib.dump(preprocessor, "preprocessor.pkl")

print("✅ Preprocessing completed successfully")
print("📁 Saved files:")
print(" - tire_wear_processed.csv")
print(" - preprocessor.pkl")