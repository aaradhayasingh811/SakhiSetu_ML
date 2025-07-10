import joblib
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple
from sklearn.linear_model import LinearRegression

class CycleModel:
    def __init__(self):
        self.model_path = Path(__file__).parent.parent.parent / 'data' / 'menstrual_cycle_model.joblib'
        self.csv_path = Path(__file__).parent.parent.parent / 'data' / 'Menstural_cyclelength.csv'
        
        self.features = [
            'age', 'cycle_number', 'cycle_length',
            'prev_cycle_length', 'cycle_var',
            'start_day_of_year', 'days_since_last_cycle'
        ]
        self.target = 'cycle_length'  # Based on your uploaded file

        if not self.model_path.exists():
            print("🔄 Model file not found. Training a new one from CSV...")
            self._train_and_save_model()
        else:
            print(f"✅ Loading model from: {self.model_path}")
        
        self.model = joblib.load(self.model_path)

    def _train_and_save_model(self):
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Training CSV not found at: {self.csv_path}")

        df = pd.read_csv(self.csv_path)

        # Convert date columns
        df['cycle_start_date'] = pd.to_datetime(df['cycle_start_date'], errors='coerce')
        df = df.dropna(subset=['cycle_start_date', 'cycle_length'])

        # Sort by user and cycle
        df = df.sort_values(by=['new_id', 'cycle_start_date'])

        # Feature engineering
        df['prev_cycle_length'] = df.groupby('new_id')['cycle_length'].shift(1)
        df['days_since_last_cycle'] = df.groupby('new_id')['cycle_start_date'].diff().dt.days
        df['cycle_var'] = df.groupby('new_id')['cycle_length'].rolling(2).std().reset_index(0, drop=True)
        df['start_day_of_year'] = df['cycle_start_date'].dt.dayofyear

        # Remove rows with NaN after feature engineering
        df = df.dropna(subset=self.features)

        X = df[self.features]
        y = df[self.target]

        model = LinearRegression()
        model.fit(X, y)
        joblib.dump(model, self.model_path)
        print(f"✅ Model trained and saved at {self.model_path}")

    def predict_next_cycle(self, input_data: dict) -> Tuple[datetime, dict]:
        try:
            input_df = pd.DataFrame([input_data], columns=self.features)
            predicted_length = self.model.predict(input_df)[0]
            last_cycle_date = datetime.strptime(input_data['last_cycle_date'], '%Y-%m-%d')
            predicted_date = last_cycle_date + timedelta(days=predicted_length)

            probability_window = {
                'predicted_date': predicted_date.strftime('%Y-%m-%d'),
                'earliest_likely_date': (predicted_date - timedelta(days=3)).strftime('%Y-%m-%d'),
                'latest_likely_date': (predicted_date + timedelta(days=3)).strftime('%Y-%m-%d'),
                'confidence': 0.8
            }

            return predicted_date, probability_window

        except Exception as e:
            raise ValueError(f"Prediction error: {str(e)}")
