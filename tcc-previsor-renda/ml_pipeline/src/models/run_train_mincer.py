from ml_pipeline.src.models.train_mincer_v1 import train_mincer_v1

train_mincer_v1(
    train_path="data/processed/v8/train.parquet",
    model_output_path="artifacts/mincer_v1/model.joblib",
    smearing_output_path="artifacts/mincer_v1/smearing.joblib",
)