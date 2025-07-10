from pydantic import BaseModel

class HormoneInput(BaseModel):
    age: int
    avg_cycle_length: int
    day: int

class HormoneOutput(HormoneInput):
    estrogen: float
    progesterone: float
    fsh: float
    lh: float