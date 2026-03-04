import joblib
import pandas as pd

# Load trained model
model = joblib.load("tire_wear_model.pkl")

# Feature names (same order as training data)
features = [
    "avg_speed",
    "distance_driven",
    "braking_frequency",
    "vehicle_load",
    "tire_pressure",
    "tire_age_months",
    "ambient_temperature",
    "road_condition",
    "vehicle_type",
    "driving_style"
]

# Feature importance ranking
ranking = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("Feature Ranking:")
print(ranking)
