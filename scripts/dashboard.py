import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Chargement des données
data = pd.read_csv("data/processed/featured_data.csv")
data['date'] = pd.to_datetime(data['date'])

# Ajout des colonnes nécessaires
data['day_of_week'] = data['date'].dt.day_name()
data['month_year'] = data['date'].dt.to_period('M').astype(str)

# Initialisation de l'application Dash
app = Dash(__name__)

# Mise en page du tableau de bord
app.layout = html.Div([
    html.H1("Tableau de Bord des Ventes", style={"text-align": "center"}),

    html.Div([
        html.Label("Sélectionnez une région :"),
        dcc.Dropdown(
            id="region-dropdown",
            options=[{"label": region, "value": region} for region in data['region_name'].unique()],
            value=None,
            placeholder="Toutes les régions",
        ),
    ], style={"width": "40%", "margin": "0 auto"}),

    dcc.Graph(id="sales-trend-graph"),
    dcc.Graph(id="sales-by-product-graph"),
    dcc.Graph(id="sales-heatmap"),
])

# Callbacks pour les interactions
@app.callback(
    [Output("sales-trend-graph", "figure"),
     Output("sales-by-product-graph", "figure"),
     Output("sales-heatmap", "figure")],
    [Input("region-dropdown", "value")]
)
def update_dashboard(selected_region):
    # Filtrer les données selon la région
    filtered_data = data if not selected_region else data[data['region_name'] == selected_region]

    if filtered_data.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Pas de données disponibles pour cette sélection.")
        return empty_fig, empty_fig, empty_fig

    # Graphique des tendances de ventes
    trend_data = filtered_data.groupby('month_year')['sales'].sum().reset_index()
    trend_fig = px.line(
        trend_data, x="month_year", y="sales", title="Tendance des Ventes Mensuelles",
        labels={"month_year": "Mois", "sales": "Ventes"}
    )

    # Graphique des ventes par produit
    product_data = filtered_data.groupby('product_name')['sales'].sum().reset_index().sort_values(by="sales", ascending=False)
    product_fig = px.bar(
        product_data, x="sales", y="product_name", orientation='h', title="Ventes par Produit",
        labels={"sales": "Ventes", "product_name": "Produit"}
    )

    # Heatmap des ventes par jour et par région
    if 'day_of_week' in filtered_data.columns and 'region_name' in filtered_data.columns:
        heatmap_data = filtered_data.groupby(['day_of_week', 'region_name'])['sales'].mean().unstack()
        heatmap_fig = px.imshow(
            heatmap_data, color_continuous_scale="Viridis", title="Ventes Moyennes par Jour et Région",
            labels=dict(x="Région", y="Jour de la Semaine", color="Ventes Moyennes")
        )
    else:
        heatmap_fig = go.Figure()
        heatmap_fig.update_layout(title="Pas de données pour cette région")

    return trend_fig, product_fig, heatmap_fig

# Lancement de l'application Dash
if __name__ == "__main__":
    app.run_server(debug=True)

