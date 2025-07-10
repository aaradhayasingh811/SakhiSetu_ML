# SakhiSaathi ML

SakhiSaathi ML is a machine learning-powered API suite for menstrual health analytics. It provides predictive models for menstrual cycle forecasting, PCOS (Polycystic Ovary Syndrome) risk assessment, and hormone level estimation, enabling users and developers to build intelligent period tracking and health applications.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Data](#data)
- [Model Training](#model-training)
- [Evaluation](#evaluation)
- [Results](#results)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Project Overview

SakhiSaathi ML leverages Python, FastAPI, scikit-learn, pandas, and related libraries to deliver robust machine learning models for menstrual health. The project includes:

- **Menstrual Cycle Prediction:** Forecasts the next cycle date and provides a probability window.
- **PCOS Risk Detection:** Predicts the risk of PCOS using clinical and lifestyle features.
- **Hormone Level Estimation:** Estimates key hormone levels (estrogen, progesterone, FSH, LH) across the menstrual cycle.

---

## Features

- RESTful API built with FastAPI
- Menstrual cycle date prediction with confidence intervals
- PCOS risk scoring using Random Forest and SMOTE for class balancing
- Hormone level estimation using mathematical models
- Data validation and preprocessing utilities
- Modular codebase for easy extension
- Automated unit tests with pytest

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/SakhiSaathi-ML.git
   cd SakhiSaathi-ML
   ```

2. **Create a virtual environment (recommended):**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

---

## Usage

1. **Prepare your data:**  
   Place your datasets (e.g., `pcos_detection.csv`, `Menstural_cyclelength.csv`) in the `data/` directory.

2. **Run the API server:**
   ```sh
   uvicorn app.main:app --reload
   ```

3. **Access the interactive API docs:**  
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

4. **Example API requests:**  
   Use the `/predict`, `/cycles/predict-next-cycle`, and `/hormones/estimate` endpoints as described below.

---

## API Endpoints

### 1. PCOS Risk Prediction

- **POST** `/predict`
- **Input:**  
  JSON body matching the `PCOSInput` schema (age, cycle_regularity, cycle_length, bmi, weight_gain, etc.)
- **Output:**  
  PCOS risk level, probability, message, and doctor recommendation.

### 2. Menstrual Cycle Prediction

- **POST** `/cycles/predict-next-cycle`
- **Input:**  
  JSON body matching the `CycleInput` schema (age, cycle_number, cycle_length, prev_cycle_length, etc.)
- **Output:**  
  Predicted next cycle date, earliest/latest likely dates, and confidence.

### 3. Hormone Level Estimation

- **GET** `/hormones/estimate`
- **Query Parameters:**  
  `age`, `avg_cycle_length`, `day`
- **Output:**  
  Estimated levels of estrogen, progesterone, FSH, and LH.

---

## Project Structure

```
ml/
├── app/
│   ├── main.py            # FastAPI application entry point
│   ├── utils.py           # Utility functions (logging, data validation)
│   ├── models/
│   │   ├── pcos_model.py      # PCOS risk model
│   │   ├── cycle_model.py     # Menstrual cycle prediction model
│   │   ├── hormone_model.py   # Hormone estimation model
│   │   └── schemas.py         # Pydantic schemas for PCOS
│   ├── routers/
│   │   └── cycles.py          # API router for cycle prediction
│   ├── schemas/
│   │   ├── cycles.py          # Schemas for cycle prediction
│   │   └── hormones.py        # Schemas for hormone estimation
├── data/                   # Raw and processed data files
├── models/                 # Saved model files (pkl, joblib)
├── results/                # Output and evaluation results
├── tests/                  # Unit tests (pytest)
│   └── test_pcos_model.py
├── requirements.txt        # Python dependencies
└── Readme.md               # Project documentation
```

---

## Data

- **Source:**  
  - `pcos_detection.csv`: Clinical and lifestyle data for PCOS risk modeling.
  - `Menstural_cyclelength.csv`: User cycle history for cycle prediction.

- **Format:**  
  - PCOS: Includes features like age, BMI, cycle regularity, symptoms (hair growth, pimples, etc.), and target label.
  - Cycle: Includes user ID, cycle start dates, cycle lengths.

- **Preprocessing:**  
  - PCOS: Dropping irrelevant columns, converting categorical to numeric, handling missing values, scaling features.
  - Cycle: Feature engineering for previous cycle length, days since last cycle, cycle variance, and date conversions.

---

## Model Training

### PCOS Model

- **Algorithm:** Random Forest Classifier
- **Preprocessing:** StandardScaler, SMOTE for class balancing
- **Features:** Age, cycle regularity, cycle length, BMI, weight gain, hair growth, pimples, hair loss, skin darkening, fast food, exercise
- **Target:** PCOS (Y/N)
- **Training Procedure:**  
  - Data cleaning and feature selection  
  - Scaling and balancing  
  - Model training and serialization with joblib

### Cycle Model

- **Algorithm:** Linear Regression
- **Features:** Age, cycle number, cycle length, previous cycle length, cycle variance, start day of year, days since last cycle
- **Target:** Cycle length
- **Training Procedure:**  
  - Feature engineering from user cycle history  
  - Model training and serialization

### Hormone Model

- **Algorithm:** Mathematical sinusoidal model based on cycle day, age, and cycle length

---

## Evaluation

- **PCOS Model:**
  - **Metrics:** Accuracy, F1-score, probability calibration
  - **Validation:** Train/test split, SMOTE for class imbalance

- **Cycle Model:**
  - **Metrics:** Mean Absolute Error (MAE), confidence window
  - **Validation:** Hold-out validation

- **Hormone Model:**
  - **Metrics:** Not applicable (mathematical model)

---

## Results

- **PCOS Model:**  
  - Returns risk level (`high`, `medium`, `low`) and probability for each input.
  - Example:  
    ```json
    {
      "risk_level": "medium",
      "probability": 0.53,
      "message": "Moderate PCOS risk. Consider lifestyle changes.",
      "show_doctor": false
    }
    ```

- **Cycle Model:**  
  - Predicts next cycle date with ±3 day window and 80% confidence.

- **Hormone Model:**  
  - Estimates normalized hormone levels for any day in the cycle.

---

## Testing

- Unit tests are provided in the `tests/` directory.
- To run tests:
  ```sh
  pytest tests/
  ```

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For questions or feedback, please contact [aaradhayasingh811@gmail.com].