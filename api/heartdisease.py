from flask import Flask, request, jsonify
from flask import Blueprint
from flask_restful import Api, Resource
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the heart disease dataset
heart_disease_data = pd.read_csv('/home/jared/vscode/JaredsBlogBE/data/DatasetHeartDisease.csv')  # Update path to your heart disease dataset

# Clean the data (if necessary)
# For simplicity, assume the data is already clean

# Split data into features (X) and target variable (y)
X = heart_disease_data[['age', 'sex', 'chest pain type', 'resting bps', 'cholesterol', 'fasting blood sugar',
                        'resting ecg', 'max heart rate', 'exercise angina', 'oldpeak', 'ST slope']]
y = heart_disease_data['target']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the logistic regression model
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train_scaled, y_train)

# Create Blueprint for Heart Disease API
heart_disease_api = Blueprint('heart_disease_api', __name__, url_prefix='/api/heart_disease')
api = Api(heart_disease_api)

class HeartDiseaseAPI(Resource):
    def predict_heart_disease(self, data):
        try:
            # Prepare data for prediction
            input_data = pd.DataFrame([data])
            input_data_scaled = scaler.transform(input_data)

            # Predict the outcome
            prediction = logreg.predict(input_data_scaled)

            return {'Prediction': int(prediction[0])}  # Assuming 1 for heart disease, 0 for no heart disease

        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            data = request.json
            result = self.predict_heart_disease(data)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})

api.add_resource(HeartDiseaseAPI, '/predict')