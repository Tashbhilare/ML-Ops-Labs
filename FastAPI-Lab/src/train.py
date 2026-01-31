"""
Train a Random Forest model on Boston Housing dataset
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def load_boston_data():
    """
    Load Boston Housing dataset
    Note: Using California Housing as Boston is deprecated in sklearn
    """
    from sklearn.datasets import fetch_california_housing
    
    print("Loading California Housing dataset...")
    data = fetch_california_housing()
    
    # Create DataFrame
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['PRICE'] = data.target
    
    print(f"Dataset shape: {df.shape}")
    print(f"Features: {list(data.feature_names)}")
    
    return df, data.feature_names

def train_model():
    """Train Random Forest model"""
    # Load data
    df, feature_names = load_boston_data()
    
    # Split features and target
    X = df.drop('PRICE', axis=1)
    y = df['PRICE']
    
    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\nTraining set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Train model
    print("\nTraining Random Forest Regressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n📊 Model Performance:")
    print(f"RMSE: ${rmse:.2f}")
    print(f"R² Score: {r2:.4f}")
    
    # Save model
    model_path = '../model/housing_model.pkl'
    joblib.dump(model, model_path)
    print(f"\n✅ Model saved to {model_path}")
    
    return model

if __name__ == "__main__":
    train_model()
