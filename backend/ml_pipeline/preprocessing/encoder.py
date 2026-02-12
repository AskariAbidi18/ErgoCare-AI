import pandas as pd

#ondinal mapping for all categorical features

WEEKEND_WORK_MAP = {
    "Never" : 0,
    "Rarely" : 1,
    "Sometimes" : 2,
    "Often" : 3,
    "Always" : 4
}

ROLE_OVERLOAD_MAP = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5
}

SITTING_DURATION_MAP = {
    "Less than 30 mins": 0,
    "30 - 60 mins": 1,
    "1 - 2 hours": 2,
    "More than 2 hours": 3
}

WHO5_MAP = {
    "All of the time": 5,
    "Most of the time": 4,
    "More than half of the time": 3,
    "Less than half of the time": 2,
    "Some of the time": 1,
    "At no time": 0
}

SLEEP_MAP = {
    "Less than 5 hours": 0,
    "5 - 6 hours": 1,
    "7 - 8 hours": 2,
    "More than 8 hours": 3
}

PHYSICAL_ACTIVITY_MAP = {
    "Sedentary": 0,
    "Light Activity (Walking)": 1,
    "Moderate Activity": 2,
    "Active": 3
}

COMMUTE_MAP = {
    "Less than 30 mins": 0,
    "30 - 60 mins": 1,
    "1 - 2 hours": 2,
    "More than 2 hours": 3
}

PUBLISH_PRESSURE_MAP = {
    "No": 0,
    "Somewhat": 1,
    "Yes": 2
}

WORKSPACE_SETUP_MAP = {
    "Adjustable Chair and Setup": 0,
    "Fixed Chair and Desk": 1,
    "Standing Desk": 2,
    "Laboratory Stool": 3,
    "Couch / Bed": 4
}

SCREEN_POSITION_MAP = {
    "At eye level": 0,
    "Below eye level": 1,
    "Above eye level": 2
}

FEET_SUPPORT_MAP = {
    "Yes": 0,
    "Only when wearing footwear": 1,
    "No": 2,
    "Feet dangle": 3
}

DISCOMFORT_ACTIVITY_MAP = {
    "Typing": 0,
    "Manual grading / writing": 1,
    "Standing": 2
}

HYDRATION_MAP = {
    "Less than 1 litre": 0,
    "1 - 2 litres": 1,
    "More than 2 litres": 2
}

#encoder 

def encode(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Ordinal encodings
    df["weekend_work"] = df["weekend_work"].map(WEEKEND_WORK_MAP)
    df["role_overload"] = df["role_overload"].astype(int)
    df["sitting_duration"] = df["sitting_duration"].map(SITTING_DURATION_MAP)
    df["sleep_hours"] = df["sleep_hours"].map(SLEEP_MAP)
    df["physical_activity"] = df["physical_activity"].map(PHYSICAL_ACTIVITY_MAP)
    df["commute_time"] = df["commute_time"].map(COMMUTE_MAP)
    df["publish_pressure"] = df["publish_pressure"].map(PUBLISH_PRESSURE_MAP)
    df["workspace_setup"] = df["workspace_setup"].map(WORKSPACE_SETUP_MAP)
    df["screen_position"] = df["screen_position"].map(SCREEN_POSITION_MAP)
    df["feet_support"] = df["feet_support"].map(FEET_SUPPORT_MAP)
    df["most_discomfort_activity"] = df["most_discomfort_activity"].map(DISCOMFORT_ACTIVITY_MAP)
    df["hydration"] = df["hydration"].map(HYDRATION_MAP)


    # Pain scales (already numeric but ensure type)
    pain_cols = [
        "neck_pain",
        "lower_back_pain",
        "wrist_pain",
        "shoulder_pain",
        "leg_pain",
        "eye_strain"
    ]
    df[pain_cols] = df[pain_cols].astype(int)

    # WHO-5 encoding
    for q in ["who5_q1", "who5_q2", "who5_q3", "who5_q4", "who5_q5"]:
        df[q] = df[q].map(WHO5_MAP)

    return df