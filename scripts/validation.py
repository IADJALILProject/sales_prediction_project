from sklearn.metrics import mean_absolute_error
import pickle
import pandas as pd

def validate_model(input_file, model_path):
    data = pd.read_csv(input_file)
    X = data[['price', 'sales_per_price', 'is_weekend']]
    y = data['sales']

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    print(f"Model MAE: {mae}")

if __name__ == "__main__":
    validate_model("data/processed/featured_data.csv", "scripts/models/model.pkl")
