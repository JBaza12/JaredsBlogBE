from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Define the Blueprint for the Heart Disease API
heart_disease_api = Blueprint('heart_disease_api', __name__, url_prefix='/api/heart_disease')
api = Api(heart_disease_api)

class HeartDiseaseAPI(Resource):
    def __init__(self):
        # Load the heart disease dataset
        heart_data = pd.read_csv('/home/jared/vscode/JaredsBlogBE/data/DatasetHeartDisease.csv')

        # Perform data preprocessing
        X = heart_data.drop('target', axis=1)
        y = heart_data['target']
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        # Initialize the Random Forest classifier
        self.rf_classifier = RandomForestClassifier()

        # Train the classifier
        self.rf_classifier.fit(X_scaled, y)

    def predict_heart_disease(self, data):
        try:
            # Create a DataFrame from the input data
            input_data = pd.DataFrame([data])

            # Scale the input data using the same scaler used during training
            input_scaled = self.scaler.transform(input_data)

            # Predict the likelihood of heart disease
            prediction = self.rf_classifier.predict_proba(input_scaled)[:, 1]

            return {'Likelihood of Heart Disease': prediction[0]}
        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            data = request.json
            result = self.predict_heart_disease(data)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})

# Add the HeartDiseaseAPI resource to the API
api.add_resource(HeartDiseaseAPI, '/predict')
