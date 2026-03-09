import joblib
import pandas as pd


def show_feature_importance():

    obj = joblib.load("models/catboost_v5_global.joblib")

    model = obj["model"]

    importance = model.get_feature_importance()

    feature_names = model.feature_names_

    df_importance = pd.DataFrame({
        "feature": feature_names,
        "importance": importance
    }).sort_values(by="importance", ascending=False)

    print("\n📊 Top 10 Variáveis Mais Importantes:\n")
    print(df_importance.head(10))


if __name__ == "__main__":
    show_feature_importance()