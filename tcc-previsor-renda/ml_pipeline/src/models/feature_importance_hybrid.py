from catboost import CatBoostRegressor


def show_feature_importance_hybrid():

    model = CatBoostRegressor()
    model.load_model("models/catboost_residual_v1.cbm")

    importance = model.get_feature_importance()
    features = model.feature_names_

    print("\n📊 Top 10 - Residual Model\n")

    data = list(zip(features, importance))
    data.sort(key=lambda x: x[1], reverse=True)

    for feat, imp in data[:10]:
        print(f"{feat} → {imp:.4f}")


if __name__ == "__main__":
    show_feature_importance_hybrid()