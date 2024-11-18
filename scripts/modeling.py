from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
import os

def train_model(input_file, output_path):
    data = pd.read_csv(input_file)
    X = data[['price', 'sales_per_price', 'is_weekend']]
    y = data['sales']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    os.makedirs(output_path, exist_ok=True)
    with open(f"{output_path}/model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Model trained and saved.")

if __name__ == "__main__":
    train_model("data/processed/featured_data.csv", "scripts/models")
