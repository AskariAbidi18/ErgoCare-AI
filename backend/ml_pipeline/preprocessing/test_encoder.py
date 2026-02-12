import pandas as pd
from ml_pipeline.preprocessing.encoder import encode

df = pd.read_csv("ml_pipeline/data/synthetic/synthetic.csv")
encoded = encode(df)

print(encoded.head())
print(encoded.dtypes)
