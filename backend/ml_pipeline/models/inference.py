import pandas as pd
from xgboost import XGBClassifier

from ml_pipeline.preprocessing.encoder import encode
from ml_pipeline.features.feature_builder import build_features


MODEL_PATH = "ml_pipeline/models/xgboost_risk_model.json"


def load_model():
    model = XGBClassifier()
    model.load_model(MODEL_PATH)
    return model


def predict_single(raw_input: dict) -> dict:
    """
    Takes one faculty response (raw form dict),
    returns prediction + probabilities + risk indices.
    """

    # Convert dict to DataFrame
    df = pd.DataFrame([raw_input])

    # Encode
    encoded = encode(df)

    # Feature engineering
    features = build_features(encoded)

    # Load model
    model = load_model()

    # Drop overall_risk_index (we did not train on it)
    X = features.drop(columns=["overall_risk_index"])

    # Predict
    pred_label = int(model.predict(X)[0])

    probs = model.predict_proba(X)[0]

    result = {
        "predicted_label": pred_label,
        "probabilities": {
            "low": float(probs[0]),
            "moderate": float(probs[1]),
            "high": float(probs[2])
        },
        "risk_indices": {
            "posture_risk_index": float(features["posture_risk_index"].iloc[0]),
            "visual_strain_index": float(features["visual_strain_index"].iloc[0]),
            "cognitive_load_index": float(features["cognitive_load_index"].iloc[0]),
            "msk_risk_index": float(features["msk_risk_index"].iloc[0]),
            "lifestyle_risk_index": float(features["lifestyle_risk_index"].iloc[0]),
            "overall_risk_index": float(features["overall_risk_index"].iloc[0])
        }
    }

    return result

if __name__ == "__main__":
    sample = pd.read_csv("ml_pipeline/data/synthetic/synthetic.csv").iloc[0].to_dict()
    print("Sample input:", sample)
    output = predict_single(sample)
    print(output)
