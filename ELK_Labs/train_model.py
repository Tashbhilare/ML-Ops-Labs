import logging
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/training.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Starting MBTA The RIDE reliability model training")

# Load data
df = pd.read_csv("data/MBTA_The_RIDE_Reliabilit.csv")
logging.info(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Feature engineering
df["trip_date"] = pd.to_datetime(df["trip_date"], utc=True)
df["otp_rate"] = df["ontime_trip_count"] / df["trip_count"]
df["day_of_week"] = df["trip_date"].dt.dayofweek
df["month"] = df["trip_date"].dt.month
df["year"] = df["trip_date"].dt.year
df["day_of_year"] = df["trip_date"].dt.dayofyear

# Drop nulls
df = df.dropna()
logging.info(f"After cleaning: {df.shape[0]} rows remaining")

# Log basic stats
logging.info(f"Average OTP rate: {df['otp_rate'].mean():.4f}")
logging.info(f"Min OTP rate: {df['otp_rate'].min():.4f}")
logging.info(f"Max OTP rate: {df['otp_rate'].max():.4f}")

low_otp = df[df["otp_rate"] < 0.85]
if len(low_otp) > 0:
    logging.warning(f"Low OTP days detected: {len(low_otp)} days below 85% on-time rate")

# Features and target
features = ["day_of_week", "month", "year", "day_of_year"]
X = df[features]
y = df["otp_rate"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
logging.info(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")

# Train
model = LinearRegression()
model.fit(X_train, y_train)
logging.info("Model training complete")

# Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

logging.info(f"MSE: {mse:.6f}")
logging.info(f"RMSE: {rmse:.6f}")
logging.info(f"R2 Score: {r2:.4f}")

if r2 < 0.3:
    logging.warning(f"Low R2 score: {r2:.4f} - temporal features alone may not explain OTP variance")

# Log coefficients
for name, coef in zip(features, model.coef_):
    logging.info(f"Coefficient - {name}: {coef:.6f}")

logging.info(f"Intercept: {model.intercept_:.6f}")
logging.info("Training pipeline complete")

print("Done. Check logs/training.log")
