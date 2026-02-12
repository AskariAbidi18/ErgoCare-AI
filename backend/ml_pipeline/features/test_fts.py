import pandas as pd
from ml_pipeline.preprocessing.encoder import encode
from ml_pipeline.features.feature_builder import build_fts

df = pd.read_csv("ml_pipeline/data/synthetic/synthetic.csv")

encoded = encode(df)
featured = build_fts(encoded)

print(featured[[
    "posture_risk_index",
    "visual_strain_index",
    "cognitive_load_index",
    "msk_risk_index",
    "lifestyle_risk_index",
    "overall_risk_index"
]].head())

print("\nDtypes:\n", featured.dtypes)
print("\nNull count:\n", featured.isnull().sum())   