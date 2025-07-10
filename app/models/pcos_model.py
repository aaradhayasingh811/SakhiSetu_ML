import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from pathlib import Path

class PCOSModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load trained model and scaler"""
        try:
            self.model = joblib.load(Path(__file__).parent / 'pcos_rf_model.pkl')
            self.scaler = joblib.load(Path(__file__).parent / 'pcos_scaler.pkl')
        except:
            self.train_model()
    
    def train_model(self):
        """Train and save new model"""
        data_path = Path(__file__).parent.parent.parent / 'data' / 'pcos_detection.csv'
        df = pd.read_csv(data_path)
        
        # Preprocessing (same as your code)
        df = df.drop(columns=["Sl. No", "Patient File No.", "Unnamed: 44"], errors='ignore')
        df["II    beta-HCG(mIU/mL)"] = pd.to_numeric(df["II    beta-HCG(mIU/mL)"], errors='coerce')
        df["AMH(ng/mL)"] = pd.to_numeric(df["AMH(ng/mL)"], errors='coerce')

        features = [
            ' Age (yrs)', 'Cycle(R/I)', 'Cycle length(days)', 'BMI',
            'Weight gain(Y/N)', 'hair growth(Y/N)', 'Pimples(Y/N)',
            'Hair loss(Y/N)', 'Skin darkening (Y/N)', 'Fast food (Y/N)',
            'Reg.Exercise(Y/N)'
        ]
        target = 'PCOS (Y/N)'

        if df["Cycle(R/I)"].dtype == object:
            df["Cycle(R/I)"] = df["Cycle(R/I)"].map({'R': 0, 'I': 1})

        df = df[features + [target]].dropna()
        X = df[features]
        y = df[target]

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        # Train model (same as your code)
        sm = SMOTE(random_state=42)
        X_sm, y_sm = sm.fit_resample(X_scaled, y)
        
        self.model = RandomForestClassifier(class_weight='balanced', random_state=42)
        self.model.fit(X_sm, y_sm)
        
        # Save model
        joblib.dump(self.model, Path(__file__).parent / 'pcos_rf_model.pkl')
        joblib.dump(self.scaler, Path(__file__).parent / 'pcos_scaler.pkl')
    
    def predict(self, input_data):
        """Make prediction from input data"""
        input_array = np.array([
            input_data.age,
            input_data.cycle_regularity,
            input_data.cycle_length,
            input_data.bmi,
            input_data.weight_gain,
            input_data.hair_growth,
            input_data.pimples,
            input_data.hair_loss,
            input_data.skin_darkening,
            input_data.fast_food,
            input_data.exercise
        ]).reshape(1, -1)
        
        scaled_input = self.scaler.transform(input_array)
        proba = self.model.predict_proba(scaled_input)[0][1]
        
        risk_level = "high" if proba >= 0.7 else "medium" if proba >= 0.4 else "low"
        
        return {
            "risk_level": risk_level,
            "probability": float(proba),
            "message": self._get_message(risk_level),
            "show_doctor": risk_level == "high"
        }
    
    def _get_message(self, risk_level):
        messages = {
            "high": "High PCOS risk detected. Please consult a healthcare provider.",
            "medium": "Moderate PCOS risk. Consider lifestyle changes.",
            "low": "Low PCOS risk detected."
        }
        return messages[risk_level]