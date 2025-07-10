from pydantic import BaseModel
from datetime import date

class CycleInput(BaseModel):
    age: int
    cycle_number: int
    cycle_length: int
    prev_cycle_length: int
    cycle_var: float
    start_day_of_year: int
    days_since_last_cycle: int
    last_cycle_date: date

class CycleDatePrediction(BaseModel):
    predicted_date: str
    earliest_likely_date: str
    latest_likely_date: str
    confidence: float
    message: str = "Dates represent a ±3 day probability window with 80% confidence"
