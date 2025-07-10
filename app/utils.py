import logging
from pathlib import Path
from typing import Dict, Any

def setup_logging():
    """Configure basic logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def validate_data_path(data_path: Path) -> bool:
    """Validate that the data file exists and is accessible"""
    if not data_path.exists():
        logging.error(f"Data file not found at {data_path}")
        return False
    if not data_path.is_file():
        logging.error(f"Data path is not a file: {data_path}")
        return False
    return True

def clean_input_data(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean and validate input data before prediction"""
    # Convert all numeric values to float
    numeric_fields = ['age', 'cycle_length', 'bmi']
    for field in numeric_fields:
        if field in input_data:
            try:
                input_data[field] = float(input_data[field])
            except (ValueError, TypeError):
                logging.warning(f"Invalid value for {field}, setting to 0")
                input_data[field] = 0.0
    
    # Ensure binary fields are 0 or 1
    binary_fields = [
        'cycle_regularity', 'weight_gain', 'hair_growth',
        'pimples', 'hair_loss', 'skin_darkening',
        'fast_food', 'exercise'
    ]
    for field in binary_fields:
        if field in input_data:
            input_data[field] = 1 if input_data[field] in [1, '1', True, 'true'] else 0
    
    return input_data