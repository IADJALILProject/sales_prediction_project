import os

if __name__ == "__main__":
    os.system("python scripts/data_collection.py")
    os.system("python scripts/data_preparation.py")
    os.system("python scripts/data_cleaning.py")
    os.system("python scripts/feature_engineering.py")
    os.system("python scripts/modeling.py")
    os.system("python scripts/validation.py")
    os.system("python scripts/dashboard.py")