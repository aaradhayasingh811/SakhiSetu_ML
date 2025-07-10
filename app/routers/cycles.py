from fastapi import APIRouter, HTTPException
from app.models.cycle_model import CycleModel
from app.schemas.cycles import CycleInput, CycleDatePrediction
from datetime import datetime

router = APIRouter(prefix="/cycles", tags=["menstrual_cycle"])
model = CycleModel()

@router.post("/predict-next-cycle", response_model=CycleDatePrediction)
async def predict_next_cycle(input_data: CycleInput):
    """
    Predict next menstrual cycle date with ±3 day probability window
    
    Parameters:
    - last_cycle_date: The first day of the last menstrual period (YYYY-MM-DD)
    - All other parameters same as before
    
    Returns:
    - predicted_date: Most likely next cycle start date
    - earliest_likely_date: 3 days before predicted date
    - latest_likely_date: 3 days after predicted date
    - confidence: Estimated confidence in the prediction window
    """
    try:
        # Convert to dict and ensure date is string for the model
        input_dict = input_data.dict()
        input_dict['last_cycle_date'] = input_dict['last_cycle_date'].isoformat()
        
        _, prediction = model.predict_next_cycle(input_dict)
        return prediction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))