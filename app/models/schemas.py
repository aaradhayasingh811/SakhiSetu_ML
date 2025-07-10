from pydantic import BaseModel

class PCOSInput(BaseModel):
    age: float
    cycle_regularity: int
    cycle_length: float
    bmi: float
    weight_gain: int
    hair_growth: int
    pimples: int
    hair_loss: int
    skin_darkening: int
    fast_food: int
    exercise: int

class PCOSOutput(BaseModel):
    risk_level: str
    probability: float
    message: str
    show_doctor: bool