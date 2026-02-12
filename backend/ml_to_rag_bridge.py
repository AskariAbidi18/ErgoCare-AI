def map_score_to_risk(score: float) -> str:
    """
    Converts 0-100 index into Low/Moderate/High
    """
    if score < 35:
        return "Low"
    elif score < 70:
        return "Moderate"
    return "High"


def map_pain_to_discomfort(pain: float) -> str:
    """
    Converts 0-5 pain scale into qualitative discomfort labels.
    """
    if pain <= 1:
        return "No"
    elif pain <= 3:
        return "Sometimes"
    return "Yes"


def build_rag_user_data(ml_output: dict) -> dict:
    indices = ml_output["risk_indices"]

    posture_risk = map_score_to_risk(indices["posture_risk_index"])
    vision_risk = map_score_to_risk(indices["visual_strain_index"])
    cognitive_risk = map_score_to_risk(indices["cognitive_load_index"])

    # discomfort estimation from index/pain drivers
    # (you can refine later)
    neck_discomfort = map_pain_to_discomfort(ml_output.get("raw", {}).get("neck_pain", 0))
    back_discomfort = map_pain_to_discomfort(ml_output.get("raw", {}).get("lower_back_pain", 0))
    eye_strain = map_pain_to_discomfort(ml_output.get("raw", {}).get("eye_strain", 0))

    stress_level = cognitive_risk

    # sitting duration: derive from index if raw not stored
    sitting_hours = ml_output.get("raw", {}).get("sitting_hours", None)

    if sitting_hours is None:
        # fallback estimate
        sitting_hours = 6

    return {
        "posture_risk": posture_risk,
        "vision_risk": vision_risk,
        "cognitive_risk": cognitive_risk,
        "sitting_hours": sitting_hours,
        "neck_discomfort": neck_discomfort,
        "back_discomfort": back_discomfort,
        "eye_strain": eye_strain,
        "stress_level": stress_level
    }
