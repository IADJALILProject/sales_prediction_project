
import pandas as pd
import os
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from bokeh.plotting import figure, show, output_file
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, HoverTool
import numpy as np

def eda_advanced(input_file, output_path):
    # Chargement des données
    data = pd.read_csv(input_file)
    os.makedirs(output_path, exist_ok=True)

    # Prétraitement
    data['date'] = pd.to_datetime(data['date'])
    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.year
    data['day_of_week'] = data['date'].dt.day_name()
    data['sales_per_price'] = data['sales'] / data['price']
    data['is_weekend'] = data['day_of_week'].isin(['Saturday', 'Sunday'])

    ### 1. Distribution des ventes (Plotly)
    fig = px.histogram(data, x="sales", nbins=30, title="Distribution des ventes", 
                       labels={"sales": "Ventes"}, color_discrete_sequence=["blue"])
    fig.write_html(f"{output_path}/plotly_sales_distribution.html")

    ### 2. Tendance des ventes dans le temps (Plotly)
    daily_sales = data.groupby('date')['sales'].sum().reset_index()
    fig = px.line(daily_sales, x="date", y="sales", title="Tendance des ventes quotidiennes",
                  labels={"sales": "Ventes", "date": "Date"})
    fig.write_html(f"{output_path}/plotly_daily_sales_trend.html")

    ### 3. Ventes moyennes par région (Plotly)
    region_sales = data.groupby('region_name')['sales'].mean().reset_index()
    fig = px.bar(region_sales, x="region_name", y="sales", color="region_name", 
                 title="Ventes moyennes par région", 
                 labels={"sales": "Ventes Moyennes", "region_name": "Région"})
    fig.write_html(f"{output_path}/plotly_region_sales.html")

    ### 4. Scatter plot : Prix vs Ventes, coloré par région (Plotly)
    fig = px.scatter(data, x="price", y="sales", color="region_name", size="sales",
                     title="Prix vs Ventes, coloré par région", 
                     labels={"price": "Prix", "sales": "Ventes", "region_name": "Région"})
    fig.write_html(f"{output_path}/plotly_price_vs_sales.html")

    ### 5. Heatmap des corrélations (Plotly)
    numeric_data = data.select_dtypes(include=['float64', 'int64'])
    corr = numeric_data.corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="coolwarm", 
                    title="Matrice de corrélation")
    fig.write_html(f"{output_path}/plotly_correlation_heatmap.html")

    ### 6. Pairplot interactif avec Bokeh
    source = ColumnDataSource(data)
    pairplot_output = f"{output_path}/bokeh_pairplot.html"
    output_file(pairplot_output)
    scatter_fig = figure(title="Scatter Plot Interactif : Ventes vs Prix", 
                          x_axis_label="Prix", y_axis_label="Ventes",
                          tools="pan,wheel_zoom,box_zoom,reset,save")
    scatter_fig.circle("price", "sales", size=10, source=source, color="navy", alpha=0.5)
    hover = HoverTool(tooltips=[("Prix", "@price"), ("Ventes", "@sales"), ("Région", "@region_name")])
    scatter_fig.add_tools(hover)
    export_png(scatter_fig, filename=f"{output_path}/bokeh_pairplot.png")
    show(scatter_fig)

    ### 7. Ventes mensuelles moyennes (Bokeh)
    monthly_sales = data.groupby('month')['sales'].mean().reset_index()
    monthly_sales['month_name'] = monthly_sales['month'].apply(lambda x: pd.Timestamp(2023, x, 1).strftime('%B'))
    monthly_source = ColumnDataSource(monthly_sales)
    monthly_fig = figure(x_range=monthly_sales['month_name'], title="Ventes moyennes par mois", 
                         x_axis_label="Mois", y_axis_label="Ventes Moyennes", 
                         tools="pan,wheel_zoom,box_zoom,reset,save")
    monthly_fig.vbar(x="month_name", top="sales", width=0.8, source=monthly_source, color="green", alpha=0.7)
    hover = HoverTool(tooltips=[("Mois", "@month_name"), ("Ventes Moyennes", "@sales")])
    monthly_fig.add_tools(hover)
    export_png(monthly_fig, filename=f"{output_path}/bokeh_monthly_sales.png")
    show(monthly_fig)

    ### 8. Boxplot des ventes par jour de la semaine (Plotly)
    fig = px.box(data, x="day_of_week", y="sales", color="day_of_week", 
                 title="Répartition des ventes par jour de la semaine", 
                 labels={"day_of_week": "Jour de la Semaine", "sales": "Ventes"})
    fig.write_html(f"{output_path}/plotly_sales_by_day_of_week.html")

    print("EDA avancée complétée avec succès. Graphiques interactifs générés.")

if __name__ == "__main__":
    eda_advanced("data/processed/featured_data.csv", "notebooks")
