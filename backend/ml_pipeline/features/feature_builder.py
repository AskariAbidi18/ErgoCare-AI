import pandas as pd


# -------------------------
# Utility helpers
# -------------------------

def clamp(series: pd.Series, low=0.0, high=1.0) -> pd.Series:
    """Clamp values between low and high."""
    return series.clip(lower=low, upper=high)


def scale_0_100(series: pd.Series) -> pd.Series:
    """Clamp to [0,1] and scale to [0,100]."""
    return clamp(series, 0.0, 1.0) * 100


# -------------------------
# Feature documentation
# -------------------------

FEATURE_DOCS = {
    "posture_risk_index": "Posture-related ergonomic risk (0-100) based on sitting duration, workspace setup, screen position, feet support, and neck/back pain.",
    "visual_strain_index": "Visual strain risk (0-100) based on eye strain, screen position, and sitting duration.",
    "cognitive_load_index": "Cognitive stress risk (0-100) based on workload, weekend work, role overload, publish pressure, and inverse WHO-5 wellbeing.",
    "msk_risk_index": "Musculoskeletal discomfort risk (0-100) based on multi-region pain and primary discomfort activity.",
    "lifestyle_risk_index": "Lifestyle-based risk modifier (0-100) based on sleep, hydration, physical activity, and commute time.",
    "overall_risk_index": "Final combined ergonomic risk score (0-100) aggregating posture, cognitive, visual, MSK, and lifestyle indices."
}


# -------------------------
# Feature Builder
# -------------------------

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds ergonomic features and composite risk indices.

    Input:
        Encoded dataframe (output of preprocessing.encoder.encode)

    Output:
        Dataframe containing ONLY final ML-ready features:
        - posture_risk_index
        - visual_strain_index
        - cognitive_load_index
        - msk_risk_index
        - lifestyle_risk_index
        - overall_risk_index
    """

    df = df.copy()
    features = pd.DataFrame(index=df.index)

    # --------------------------------------------------
    # WHO-5 (psychological wellbeing → stress proxy)
    # --------------------------------------------------

    who_cols = ["who5_q1", "who5_q2", "who5_q3", "who5_q4", "who5_q5"]
    who5_total = df[who_cols].sum(axis=1)              # 0–25
    who5_normalized = who5_total / 25.0                # 0–1
    who5_stress_inverse = 1.0 - who5_normalized        # higher = worse wellbeing


    # --------------------------------------------------
    # Pain / MSD aggregation
    # --------------------------------------------------

    pain_cols = [
        "neck_pain",
        "lower_back_pain",
        "wrist_pain",
        "shoulder_pain",
        "leg_pain",
        "eye_strain"
    ]

    pain_avg = df[pain_cols].mean(axis=1) / 5.0        # normalize to 0–1


    # --------------------------------------------------
    # Workload features
    # --------------------------------------------------

    workload_hours_total = df["teaching_hours"] + df["admin_hours"]

    MAX_WORKLOAD = 50.0  # heuristic upper bound
    workload_hours_normalized = clamp(workload_hours_total / MAX_WORKLOAD)

    weekend_norm = df["weekend_work"] / 4.0
    overload_norm = (df["role_overload"] - 1) / 4.0
    publish_norm = df["publish_pressure"] / 2.0


    # --------------------------------------------------
    # Posture Risk Index
    # --------------------------------------------------

    sitting_norm = df["sitting_duration"] / 3.0
    workspace_norm = df["workspace_setup"] / 4.0
    screen_norm = df["screen_position"] / 2.0
    feet_norm = df["feet_support"] / 3.0

    neck_back_norm = (df["neck_pain"] + df["lower_back_pain"]) / 10.0

    posture_risk = (
        0.25 * sitting_norm +
        0.25 * workspace_norm +
        0.15 * screen_norm +
        0.10 * feet_norm +
        0.25 * neck_back_norm
    )

    features["posture_risk_index"] = scale_0_100(posture_risk)


    # --------------------------------------------------
    # Visual Strain Index
    # --------------------------------------------------

    eye_norm = df["eye_strain"] / 5.0

    visual_risk = (
        0.40 * eye_norm +
        0.30 * screen_norm +
        0.30 * sitting_norm
    )

    features["visual_strain_index"] = scale_0_100(visual_risk)


    # --------------------------------------------------
    # Cognitive Load Index
    # --------------------------------------------------

    cognitive_risk = (
        0.30 * workload_hours_normalized +
        0.20 * weekend_norm +
        0.20 * overload_norm +
        0.15 * publish_norm +
        0.15 * who5_stress_inverse
    )

    features["cognitive_load_index"] = scale_0_100(cognitive_risk)


    # --------------------------------------------------
    # Musculoskeletal Risk Index
    # --------------------------------------------------

    activity_norm = df["most_discomfort_activity"] / 2.0
    msk_avg = df[
        ["neck_pain", "lower_back_pain", "wrist_pain", "shoulder_pain", "leg_pain"]
    ].mean(axis=1) / 5.0

    msk_risk = (
        0.80 * msk_avg +
        0.20 * activity_norm
    )

    features["msk_risk_index"] = scale_0_100(msk_risk)


    # --------------------------------------------------
    # Lifestyle Risk Index
    # --------------------------------------------------

    sleep_norm = df["sleep_hours"] / 3.0
    hydration_norm = df["hydration"] / 2.0
    activity_life_norm = df["physical_activity"] / 3.0
    commute_norm = df["commute_time"] / 3.0

    lifestyle_risk = (
        0.30 * (1.0 - sleep_norm) +
        0.20 * (1.0 - hydration_norm) +
        0.30 * (1.0 - activity_life_norm) +
        0.20 * commute_norm
    )

    features["lifestyle_risk_index"] = scale_0_100(lifestyle_risk)


    # --------------------------------------------------
    # Overall Ergonomic Risk Index
    # --------------------------------------------------
    # v1 heuristic weights (domain-driven, explainable):
    # posture:   30%
    # cognitive: 25%
    # visual:    20%
    # MSK:       20%
    # lifestyle: 5%

    overall_risk = (
        0.30 * (features["posture_risk_index"] / 100.0) +
        0.25 * (features["cognitive_load_index"] / 100.0) +
        0.20 * (features["visual_strain_index"] / 100.0) +
        0.20 * (features["msk_risk_index"] / 100.0) +
        0.05 * (features["lifestyle_risk_index"] / 100.0)
    )

    features["overall_risk_index"] = scale_0_100(overall_risk)

    return features
