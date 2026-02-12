import pandas as pd

# Risk classes:
# 0 → Low
# 1 → Moderate
# 2 → High

def label_risk(features: pd.DataFrame) -> pd.Series:
    """
    Assign ergonomic risk labels based on overall_risk_index.

    Input:
        DataFrame returned by feature_builder.build_features()

    Output:
        pd.Series named 'risk_label'
    """

    if "overall_risk_index" not in features.columns:
        raise ValueError("overall_risk_index not found in features")

    scores = features["overall_risk_index"]

    labels = pd.Series(0, index=features.index, dtype="int64")

    labels[scores < 45] = 0
    labels[(scores >= 45) & (scores < 65)] = 1
    labels[scores >= 65] = 2

    labels.name = "risk_label"
    return labels
