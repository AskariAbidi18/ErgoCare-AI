from ml_pipeline.pipeline.ml_pipeline import run_ml_pipeline
from rag_pipeline.rag.rag_pipeline import run_rag_pipeline
from ml_to_rag_bridge import build_rag_user_data


def run_full_pipeline(user_input: dict) -> dict:
    ml_output = run_ml_pipeline (user_input)

    # Convert ML output to format expected by RAG
    rag_user_data = build_rag_user_data(ml_output)

    rag_report = run_rag_pipeline(rag_user_data)

    return {
        "ml_output": ml_output,
        "rag_user_data": rag_user_data,
        "rag_report": rag_report
    }


if __name__ == "__main__":
    sample_input = {
        "consent": "Yes",
        "age_group": "41-50",
        "department": "Computer Science / AIML",
        "designation": "Professor",
        "experience_years": "11-15",
        "marital_status": "Single",
        "teaching_hours": 18,
        "admin_hours": 13,
        "weekend_work": "Always",
        "role_overload": 3,
        "publish_pressure": "No",
        "workspace_setup": "Adjustable Chair and Setup",
        "screen_position": "Above eye level",
        "feet_support": "Yes",
        "sitting_duration": "Less than 30 mins",
        "most_discomfort_activity": "Standing",
        "sleep_hours": "5 - 6 hours",
        "physical_activity": "Light Activity (Walking)",
        "hydration": "More than 2 litres",
        "commute_time": "More than 2 hours",
        "neck_pain": 5,
        "lower_back_pain": 1,
        "wrist_pain": 3,
        "shoulder_pain": 4,
        "leg_pain": 2,
        "eye_strain": 2,
        "who5_q1": "At no time",
        "who5_q2": "Most of the time",
        "who5_q3": "All of the time",
        "who5_q4": "Most of the time",
        "who5_q5": "Most of the time"
    }

    out = run_full_pipeline(sample_input)
    print(out["rag_report"])