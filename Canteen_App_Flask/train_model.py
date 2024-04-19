import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load data from CSV
data = pd.read_csv("Canteen_App_Flask\canteen_data.csv")

# Preprocess data (handle categorical features)
labelencoder = LabelEncoder()
data["Menu_Item"] = labelencoder.fit_transform(data["Menu_Item"])
data["Category"] = labelencoder.fit_transform(data["Category"])
# Feature engineering (you can add more features based on your data)
data["Day of Week"] = pd.to_datetime(data["date"]).dt.dayofweek

# Define target variable
X=data[['Category', 'Menu_Item', 'Price', 'Quantity']]
y=data['Total Item Price']


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regression model (you can experiment with other models)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model for later use
import pickle

with open("demand_forecasting_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model training complete!")