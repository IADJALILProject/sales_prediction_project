import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

def eda(input_file, output_path):
    # Chargement des données
    data = pd.read_csv(input_file)
    os.makedirs(output_path, exist_ok=True)

    # Conversion de la colonne date
    data['date'] = pd.to_datetime(data['date'])
    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.year
    data['day_of_week'] = data['date'].dt.day_name()
    data['sales_per_price'] = data['sales'] / data['price']

    ### 1. Distribution des ventes
    plt.figure(figsize=(10, 6))
    sns.histplot(data['sales'], kde=True, bins=30, color="blue")
    plt.title('Distribution des ventes')
    plt.xlabel('Ventes')
    plt.ylabel('Fréquence')
    plt.savefig(f"{output_path}/sales_distribution.png")
    plt.close()

    ### 2. Distribution des prix
    plt.figure(figsize=(10, 6))
    sns.histplot(data['price'], kde=True, bins=30, color="orange")
    plt.title('Distribution des prix')
    plt.xlabel('Prix')
    plt.ylabel('Fréquence')
    plt.savefig(f"{output_path}/price_distribution.png")
    plt.close()

    ### 3. Boxplot des ventes par région
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x='region_name', y='sales', palette="Set2")
    plt.title('Répartition des ventes par région')
    plt.xlabel('Région')
    plt.ylabel('Ventes')
    plt.savefig(f"{output_path}/sales_by_region_boxplot.png")
    plt.close()

    ### 4. Ventes moyennes par jour de la semaine
    sales_by_day = data.groupby('day_of_week')['sales'].mean().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )
    plt.figure(figsize=(10, 6))
    sns.barplot(x=sales_by_day.index, y=sales_by_day.values, palette="coolwarm")
    plt.title('Ventes moyennes par jour de la semaine')
    plt.xlabel('Jour de la semaine')
    plt.ylabel('Ventes moyennes')
    plt.savefig(f"{output_path}/sales_by_day_of_week.png")
    plt.close()

    ### 5. Tendance des ventes mensuelles
    monthly_sales = data.groupby(['year', 'month'])['sales'].sum().reset_index()
    monthly_sales['month_year'] = pd.to_datetime(monthly_sales[['year', 'month']].assign(day=1))
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_sales, x='month_year', y='sales', marker="o", color="green")
    plt.title('Tendance des ventes mensuelles')
    plt.xlabel('Mois')
    plt.ylabel('Ventes totales')
    plt.savefig(f"{output_path}/monthly_sales_trend.png")
    plt.close()

    ### 6. Ventes cumulées dans le temps
    data['cumulative_sales'] = data['sales'].cumsum()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='date', y='cumulative_sales', color="darkred")
    plt.title('Ventes cumulées au fil du temps')
    plt.xlabel('Date')
    plt.ylabel('Ventes cumulées')
    plt.savefig(f"{output_path}/cumulative_sales_trend.png")
    plt.close()

    ### 7. Matrice de corrélation
    numeric_data = data.select_dtypes(include=['float64', 'int64'])
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title('Matrice de corrélation')
    plt.savefig(f"{output_path}/correlation_heatmap.png")
    plt.close()

    ### 8. Scatterplot : Ventes vs Prix
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='price', y='sales', hue='region_name', alpha=0.8)
    plt.title('Prix vs Ventes, coloré par région')
    plt.xlabel('Prix')
    plt.ylabel('Ventes')
    plt.savefig(f"{output_path}/price_vs_sales_scatterplot.png")
    plt.close()

    ### 9. Ventes totales par produit
    product_sales = data.groupby('product_name')['sales'].sum().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(data=product_sales, x='sales', y='product_name', palette="viridis")
    plt.title('Ventes totales par produit')
    plt.xlabel('Ventes')
    plt.ylabel('Produit')
    plt.savefig(f"{output_path}/product_sales_barplot.png")
    plt.close()

    ### 10. Ventes par région et par produit (Subplots)
    region_sales = data.groupby('region_name')['sales'].sum().reset_index()
    product_sales = data.groupby('product_name')['sales'].sum().reset_index()
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    sns.barplot(data=region_sales, x='region_name', y='sales', ax=axes[0], palette="Set2")
    axes[0].set_title('Ventes totales par région')
    axes[0].set_xlabel('Région')
    axes[0].set_ylabel('Ventes')

    sns.barplot(data=product_sales, x='sales', y='product_name', ax=axes[1], palette="viridis")
    axes[1].set_title('Ventes totales par produit')
    axes[1].set_xlabel('Ventes')
    axes[1].set_ylabel('Produit')

    plt.tight_layout()
    plt.savefig(f"{output_path}/sales_by_region_and_product.png")
    plt.close()

    ### 11. Pairplot des variables numériques
    sns.pairplot(numeric_data, diag_kind="kde", corner=True)
    plt.savefig(f"{output_path}/numeric_pairplot.png")
    plt.close()

    ### 12. Distribution des ratios (Ventes/Prix)
    plt.figure(figsize=(10, 6))
    sns.histplot(data['sales_per_price'], kde=True, bins=30, color="purple")
    plt.title('Distribution des ratios ventes/prix')
    plt.xlabel('Ventes par unité de prix')
    plt.ylabel('Fréquence')
    plt.savefig(f"{output_path}/sales_per_price_distribution.png")
    plt.close()

    ### 13. Ventes par jour de la semaine et par région (Heatmap)
    sales_heatmap = data.groupby(['day_of_week', 'region_name'])['sales'].mean().unstack()
    plt.figure(figsize=(12, 6))
    sns.heatmap(sales_heatmap, annot=True, cmap="coolwarm", fmt=".1f")
    plt.title('Ventes moyennes par jour et par région')
    plt.xlabel('Région')
    plt.ylabel('Jour de la semaine')
    plt.savefig(f"{output_path}/sales_heatmap.png")
    plt.close()

    print("EDA enrichie terminée avec des visualisations variées sauvegardées.")

if __name__ == "__main__":
    eda("data/processed/featured_data.csv", "notebooks")
