import pandas as pd
import hashlib

def dataset_signature(path):
    df = pd.read_parquet(path)
    
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    
    dataset_hash = hashlib.md5(
        pd.util.hash_pandas_object(df, index=True).values
    ).hexdigest()
    
    print("Dataset hash:", dataset_hash)

if __name__ == "__main__":
    dataset_signature("data/processed/v3/test.parquet")