# from fastapi import FastAPI
# from app.models.pcos_model import PCOSModel
# from app.models.schemas import PCOSInput, PCOSOutput

# from fastapi import APIRouter, HTTPException, Query
# from app.models.hormone_model import HormoneModel
# from app.schemas.hormones import HormoneOutput

# app = FastAPI(title="PCOS Detection API")
# model = PCOSModel()

# @app.post("/predict", response_model=PCOSOutput)
# async def predict_pcos(input_data: PCOSInput):
#     """Endpoint for PCOS risk prediction"""
#     return model.predict(input_data)


# router = APIRouter(prefix="/hormones", tags=["hormones"])
# model = HormoneModel()

# @router.get("/estimate", response_model=HormoneOutput)
# async def estimate_hormones(
#     age: int = Query(..., gt=0, description="User's age"),
#     avg_cycle_length: int = Query(..., gt=0, description="Average menstrual cycle length"),
#     day: int = Query(..., gt=0, description="Day in menstrual cycle")
# ):
#     if day > avg_cycle_length + 7:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Day {day} is too large for average cycle length of {avg_cycle_length}"
#         )
    
#     return model.predict(age, avg_cycle_length, day)

from fastapi import FastAPI, APIRouter, HTTPException, Query
from app.models.pcos_model import PCOSModel
from app.models.schemas import PCOSInput, PCOSOutput
from app.models.hormone_model import HormoneModel
from app.schemas.hormones import HormoneOutput
from app.routers import cycles
app = FastAPI(title="PCOS Detection API")
pcos_model = PCOSModel()
hormone_model = HormoneModel()

@app.post("/predict", response_model=PCOSOutput)
async def predict_pcos(input_data: PCOSInput):
    return pcos_model.predict(input_data)

router = APIRouter(prefix="/hormones", tags=["hormones"])

@router.get("/estimate", response_model=HormoneOutput)
async def estimate_hormones(
    age: int = Query(..., gt=0, description="User's age"),
    avg_cycle_length: int = Query(..., gt=0, description="Average menstrual cycle length"),
    day: int = Query(..., gt=0, description="Day in menstrual cycle")
):
    if day > avg_cycle_length + 7:
        raise HTTPException(
            status_code=400,
            detail=f"Day {day} is too large for average cycle length of {avg_cycle_length}"
        )
    
    return hormone_model.predict(age, avg_cycle_length, day)

# Register router here
app.include_router(cycles.router)
app.include_router(router)
