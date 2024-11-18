import pandas as pd

def clean_data(input_file, output_file):
    data = pd.read_csv(input_file)
    data.fillna({'sales': 0}, inplace=True)
    data.drop_duplicates(inplace=True)
    data.to_csv(output_file, index=False)
    print("Data cleaned and saved.")

if __name__ == "__main__":
    clean_data("data/processed/merged_data.csv", "data/processed/cleaned_data.csv")
