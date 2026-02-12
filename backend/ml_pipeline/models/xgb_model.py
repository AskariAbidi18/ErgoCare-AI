import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight

from xgboost import XGBClassifier

from ml_pipeline.preprocessing.encoder import encode
from ml_pipeline.features.feature_builder import build_features
from ml_pipeline.labels.risk_labeler import label_risk


def main():
    # --------------------------------------------------
    # Load data
    # --------------------------------------------------
    df = pd.read_csv("ml_pipeline/data/synthetic/synthetic.csv")

    # --------------------------------------------------
    # Pipeline
    # --------------------------------------------------
    encoded = encode(df)
    features = build_features(encoded)
    labels = label_risk(features)

    X = features.drop(columns=["overall_risk_index"])

    y = labels

    # --------------------------------------------------
    # Train / test split
    # --------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    # --------------------------------------------------
    # Handle class imbalance
    # --------------------------------------------------
    class_weights = compute_class_weight(
        class_weight="balanced",
        classes=np.unique(y_train),
        y=y_train
    )

    weight_map = dict(zip(np.unique(y_train), class_weights))
    sample_weights = y_train.map(weight_map)

    print("\nClass weights:", weight_map)

    # --------------------------------------------------
    # XGBoost model
    # --------------------------------------------------
    model = XGBClassifier(
        objective="multi:softprob",
        num_class=3,
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="mlogloss",
        random_state=42
    )

    # --------------------------------------------------
    # Train
    # --------------------------------------------------
    model.fit(
        X_train,
        y_train,
        sample_weight=sample_weights
    )

    # --------------------------------------------------
    # Evaluate
    # --------------------------------------------------
    y_pred = model.predict(X_test)

    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred, digits=3))

    print("\n--- Confusion Matrix ---")
    print(confusion_matrix(y_test, y_pred))

    # --------------------------------------------------
    # Feature importance
    # --------------------------------------------------
    importances = pd.Series(
        model.feature_importances_,
        index=X.columns
    ).sort_values(ascending=False)

    print("\n--- Feature Importance ---")
    print(importances)

    # --------------------------------------------------
    # Save model
    # --------------------------------------------------
    model.save_model("ml_pipeline/models/xgboost_risk_model.json")
    print("\nModel saved to ml_pipeline/models/xgboost_risk_model.json")


if __name__ == "__main__":
    main()
