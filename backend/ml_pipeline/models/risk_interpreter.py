from typing import Dict, List


# -----------------------------
# Thresholds (domain-tuned v1)
# -----------------------------

DOMAIN_THRESHOLDS = {
    "posture_risk_index": 65,
    "visual_strain_index": 65,
    "cognitive_load_index": 65,
    "msk_risk_index": 65,
    "lifestyle_risk_index": 65
}


LABEL_MAP = {
    0: "Low",
    1: "Moderate",
    2: "High"
}


def interpret_risk(inference_output: Dict) -> Dict:
    """
    Converts model inference output into structured
    risk interpretation for RAG consumption.
    """

    predicted_label = inference_output["predicted_label"]
    probabilities = inference_output["probabilities"]
    indices = inference_output["risk_indices"]
    # Identify high-risk domains
    
    high_domains: List[str] = []
    moderate_domains: List[str] = []

    for domain, threshold in DOMAIN_THRESHOLDS.items():
        value = indices[domain]

        if value >= threshold:
            high_domains.append(domain.replace("_risk_index", ""))
        elif value >= (threshold - 15):
            moderate_domains.append(domain.replace("_risk_index", ""))
    # Identify primary driver (highest index)
    
    primary_driver = max(
        indices,
        key=lambda k: indices[k] if "risk_index" in k else -1
    ).replace("_risk_index", "")
    # Confidence level

    confidence = max(probabilities.values())

    if confidence >= 0.85:
        confidence_level = "Very High"
    elif confidence >= 0.65:
        confidence_level = "High"
    elif confidence >= 0.45:
        confidence_level = "Moderate"
    else:
        confidence_level = "Low"
    # Final structured output

    interpretation = {
        "overall_risk_level": LABEL_MAP[predicted_label],
        "confidence_score": float(confidence),
        "confidence_level": confidence_level,
        "primary_risk_driver": primary_driver,
        "high_risk_domains": high_domains,
        "moderate_risk_domains": moderate_domains
    }

    return interpretation

if __name__ == "__main__":
    from ml_pipeline.models.inference import predict_single
    import pandas as pd

    sample = pd.read_csv("ml_pipeline/data/synthetic/synthetic.csv").iloc[0].to_dict()
    print("Sample input:", sample)
    output = predict_single(sample)

    result = interpret_risk(output)
    print(result)
