import pytest
import numpy as np
from app.models.pcos_model import PCOSModel
from app.models.schemas import PCOSInput

@pytest.fixture
def sample_input():
    return PCOSInput(
        age=25.0,
        cycle_regularity=1,
        cycle_length=35.0,
        bmi=26.5,
        weight_gain=1,
        hair_growth=1,
        pimples=1,
        hair_loss=0,
        skin_darkening=1,
        fast_food=1,
        exercise=0
    )

@pytest.fixture
def model():
    return PCOSModel()

def test_model_prediction(model, sample_input):
    """Test that the model returns valid predictions"""
    result = model.predict(sample_input)
    
    assert result['risk_level'] in ['high', 'medium', 'low']
    assert 0 <= result['probability'] <= 1
    assert isinstance(result['message'], str)
    assert isinstance(result['show_doctor'], bool)

def test_input_validation(model):
    """Test that invalid inputs are handled properly"""
    with pytest.raises(ValueError):
        model.predict("invalid input")

def test_model_loading(model):
    """Test that model and scaler are properly loaded"""
    assert model.model is not None
    assert model.scaler is not None

def test_output_structure(model, sample_input):
    """Test that output structure is correct"""
    result = model.predict(sample_input)
    required_keys = {'risk_level', 'probability', 'message', 'show_doctor'}
    assert all(key in result for key in required_keys)