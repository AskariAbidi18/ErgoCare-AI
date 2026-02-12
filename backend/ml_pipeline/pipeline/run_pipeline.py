import pandas as pd

from ml_pipeline.preprocessing.encoder import encode
from ml_pipeline.features.feature_builder import build_features
from ml_pipeline.labels.risk_labeler import label_risk


def main():
    print("Loading synthetic data...")
    df = pd.read_csv("ml_pipeline/data/synthetic/synthetic.csv")

    print("Encoding raw responses...")
    encoded = encode(df)

    print("Building ergonomic features...")
    features = build_features(encoded)

    print("Labelling ergonomic risk...")
    labels = label_risk(features)

    # --------------------------------------------------
    # Sanity checks
    # --------------------------------------------------

    print("\n--- FEATURE SAMPLE ---")
    print(features.head())

    print("\n--- FEATURE STATS ---")
    print(features.describe())

    print("\n--- RISK LABEL DISTRIBUTION ---")
    print(labels.value_counts().sort_index())

    print("\n--- FULL OUTPUT SAMPLE ---")
    output = features.copy()
    output["risk_label"] = labels
    print(output.head())


if __name__ == "__main__":
    main()
