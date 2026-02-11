import random
import pandas as pd
from ml_pipeline.schema import form_schema as fs
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "synthetic")
os.makedirs(DATA_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(DATA_DIR, "synthetic.csv")

def generate_row():
    return {
        "consent": "Yes",
        "age_group": random.choice(fs.AGE_GROUPS),
        "department": "Computer Science / AIML",
        "designation": random.choice(fs.DESIGNATIONS),
        "experience_years": random.choice(["0-5", "6-10", "11-15", "15+"]),
        "marital_status": random.choice(
            ["Single", "Married", "Married with children"]
        ),
        "teaching_hours": random.randint(8, 20),
        "admin_hours": random.randint(4, 30),
        "weekend_work": random.choice(fs.WEEKEND_WORK),
        "role_overload": random.randint(1, 5),
        "publish_pressure": random.choice(["Yes", "No", "Somewhat"]),
        "workspace_setup": random.choice(fs.WORKSPACE_SETUP),
        "screen_position": random.choice(fs.SCREEN_POSITION),
        "feet_support": random.choice(fs.FEET_SUPPORT),
        "sitting_duration": random.choice(fs.SITTING_DURATION),
        "most_discomfort_activity": random.choice(
            ["Typing", "Manual grading / writing", "Standing"]
        ),
        "sleep_hours": random.choice(
            ["Less than 5 hours", "5 - 6 hours", "7 - 8 hours"]
        ),
        "physical_activity": random.choice(fs.PHYSICAL_ACTIVITY),
        "hydration": random.choice(
            ["Less than 1 litre", "1 - 2 litres", "More than 2 litres"]
        ),
        "commute_time": random.choice(
            ["Less than 30 mins", "30 - 60 mins", "1 - 2 hours", "More than 2 hours"]
        ),
        "neck_pain": random.randint(0, 5),
        "lower_back_pain": random.randint(0, 5),
        "wrist_pain": random.randint(0, 5),
        "shoulder_pain": random.randint(0, 5),
        "leg_pain": random.randint(0, 5),
        "eye_strain": random.randint(0, 5),
        "who5_q1": random.choice(fs.WHO5),
        "who5_q2": random.choice(fs.WHO5),
        "who5_q3": random.choice(fs.WHO5),
        "who5_q4": random.choice(fs.WHO5),
        "who5_q5": random.choice(fs.WHO5),
    }

def generate_dataset(n=500):
    rows = [generate_row() for _ in range(n)]
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate_dataset(500)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Synthetic dataset saved to {OUTPUT_PATH}")

