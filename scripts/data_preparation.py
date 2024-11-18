import pandas as pd
import os

def prepare_data(input_path, output_path):
    sales_data = pd.read_csv(f"{input_path}/sales_data.csv")
    
    # Mock region and product data
    region_data = pd.DataFrame({
        "region_id": [1, 2, 3, 4],
        "region_name": ["North", "South", "East", "West"]
    })
    product_data = pd.DataFrame({
        "product_id": range(1, 10),
        "product_name": [f"Product_{i}" for i in range(1, 10)]
    })

    # Merge data
    merged_data = pd.merge(sales_data, region_data, on="region_id", how="left")
    merged_data = pd.merge(merged_data, product_data, on="product_id", how="left")
    os.makedirs(output_path, exist_ok=True)
    merged_data.to_csv(f"{output_path}/merged_data.csv", index=False)
    print("Data prepared and saved.")

if __name__ == "__main__":
    prepare_data("data/raw", "data/processed")
