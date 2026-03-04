from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import joblib

df = pd.read_csv("tire_wear_processed.csv")

X = df.drop("tire_wear", axis=1)
y = df["tire_wear"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

param_grid = {
    "n_estimators": [150, 200],
    "max_depth": [10, 15, None],
    "min_samples_split": [2, 5],
}

rf = RandomForestRegressor(random_state=42)

grid = GridSearchCV(
    rf,
    param_grid,
    cv=5,
    scoring="neg_mean_absolute_error",
    n_jobs=-1
)

grid.fit(X_train, y_train)

best_model = grid.best_estimator_

y_pred = best_model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, y_pred))
print("R2:", r2_score(y_test, y_pred))

joblib.dump(best_model, "tire_wear_model.pkl")
print("✅ Optimized model saved")
