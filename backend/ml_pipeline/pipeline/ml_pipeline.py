from typing import Dict

from ml_pipeline.preprocessing.encoder import encode
from ml_pipeline.features.feature_builder import build_features
from ml_pipeline.models.inference import predict_single
from ml_pipeline.models.risk_interpreter import interpret_risk


def run_ml_pipeline(raw_input: Dict) -> Dict:
    """
    Main ML pipeline entry point.

    Input:
        raw_input: dict representing ONE faculty form response

    Output:
        Structured ML result for downstream systems (RAG / API / UI)
    """

    # --------------------------------------------------
    # Step 1: Run ML inference
    # --------------------------------------------------
    inference_output = predict_single(raw_input)

    # --------------------------------------------------
    # Step 2: Interpret risk semantically
    # --------------------------------------------------
    interpretation = interpret_risk(inference_output)

    # --------------------------------------------------
    # Step 3: Combine outputs
    # --------------------------------------------------
    result = {
        "prediction": {
            "risk_label": interpretation["overall_risk_level"],
            "confidence": interpretation["confidence_level"],
            "confidence_score": interpretation["confidence_score"]
        },
        "risk_drivers": {
            "primary": interpretation["primary_risk_driver"],
            "high_domains": interpretation["high_risk_domains"],
            "moderate_domains": interpretation["moderate_risk_domains"]
        },
        "risk_indices": inference_output["risk_indices"],
        "model_probabilities": inference_output["probabilities"]
    }

    return result

if __name__ == "__main__":
    import pandas as pd

    sample = pd.read_csv(
        "ml_pipeline/data/synthetic/synthetic.csv"
    ).iloc[0].to_dict()
    print("Sample input:", sample)
    output = run_ml_pipeline(sample)
    print(output)
