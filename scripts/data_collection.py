import pandas as pd
import numpy as np
import os

def generate_mock_data(output_path):
    np.random.seed(42)
    sales_data = pd.DataFrame({
        "date": pd.date_range(start="2023-01-01", end="2023-12-31", freq="D"),
        "region_id": np.random.randint(1, 5, 365),
        "product_id": np.random.randint(1, 10, 365),
        "price": np.random.uniform(5, 100, 365),
        "sales": np.random.randint(1, 50, 365)
    })
    os.makedirs(output_path, exist_ok=True)
    sales_data.to_csv(f"{output_path}/sales_data.csv", index=False)
    print("Mock data generated and saved.")

if __name__ == "__main__":
    generate_mock_data("data/raw")
