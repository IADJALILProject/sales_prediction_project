import pandas as pd

def add_features(input_file, output_file):
    data = pd.read_csv(input_file)
    data['sales_per_price'] = data['sales'] / data['price']
    data['is_weekend'] = pd.to_datetime(data['date']).dt.weekday >= 5
    data.to_csv(output_file, index=False)
    print("Features engineered and saved.")

if __name__ == "__main__":
    add_features("data/processed/cleaned_data.csv", "data/processed/featured_data.csv")
