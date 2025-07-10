import numpy as np

class HormoneModel:
    def predict(self, age: int, avg_cycle_length: int, day: int) -> dict:
        """Hormone estimation model"""
        # Normalize inputs
        normalized_age = (age - 15) / (45 - 15)  # Assuming age range 15-45
        normalized_cycle = (avg_cycle_length - 21) / (35 - 21)  # Assuming cycle range 21-35
        normalized_day = (day - 1) / (avg_cycle_length - 1)  # Normalize day within cycle
        
        # Hormone level calculations
        estrogen = 0.5 + 0.5 * np.sin(2 * np.pi * normalized_day)
        progesterone = 0.3 + 0.7 * np.sin(2 * np.pi * normalized_day - np.pi/2)
        fsh = 0.4 + 0.6 * np.sin(2 * np.pi * normalized_day + np.pi/4)
        lh = 0.2 + 0.8 * np.sin(2 * np.pi * normalized_day + np.pi/2)
        
        # Adjust based on age and cycle length
        age_factor = 1.0 - 0.5 * normalized_age
        cycle_factor = 0.8 + 0.2 * normalized_cycle
        
        return {
            'estrogen': max(0, min(1, estrogen * age_factor * cycle_factor)),
            'progesterone': max(0, min(1, progesterone * age_factor * cycle_factor)),
            'fsh': max(0, min(1, fsh * age_factor)),
            'lh': max(0, min(1, lh * age_factor)),
            'day': day,
            'age': age,
            'avg_cycle_length': avg_cycle_length
        }