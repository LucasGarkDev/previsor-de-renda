import joblib

def inspect_model(path):
    print(f"\n🔎 Inspecionando: {path}")
    
    obj = joblib.load(path)
    
    print("Tipo:", type(obj))
    
    if isinstance(obj, dict):
        print("Chaves disponíveis:")
        for key in obj.keys():
            print(" -", key)
        
        # Se tiver modelo dentro
        if "model" in obj:
            print("\nTipo do modelo interno:", type(obj["model"]))
    
    else:
        print("Objeto não é dict.")


if __name__ == "__main__":
    inspect_model("models/catboost_v5_global.joblib")