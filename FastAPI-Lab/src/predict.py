"""
Prediction function for housing price model
"""
import joblib
import numpy as np

def predict_price(data_dict):
    """
    Predict housing price based on input features
    
    Args:
        data_dict (dict): Dictionary with keys matching feature names
        
    Returns:
        float: Predicted house price
    """
    model = joblib.load("../model/housing_model.pkl")
    
    # Convert dictionary to array in correct order
    # Order: MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude
    X = np.array([[
        data_dict['MedInc'],
        data_dict['HouseAge'],
        data_dict['AveRooms'],
        data_dict['AveBedrms'],
        data_dict['Population'],
        data_dict['AveOccup'],
        data_dict['Latitude'],
        data_dict['Longitude']
    ]])
    
    prediction = model.predict(X)
    return float(prediction[0])
