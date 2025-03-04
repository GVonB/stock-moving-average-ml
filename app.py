# app.py
import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from predictor import predict_ma_projection

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Stock Moving Average Analysis"
server = app.server

default_ticker = 'NVDA'
default_ma_target = 150
start_date = (datetime.today() - timedelta(days=300)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1("Stock Price Moving Average Projection", className="custom-title mt-3 text-center text-white"), 
            width=12
        )
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Stock Ticker:", className="text-white"),
            dbc.Input(id="ticker-input", type="text", value=default_ticker)
        ], width=6),
        dbc.Col([
            dbc.Label("Target Moving Average:", className="text-white"),
            dbc.Input(id="ma-target-input", type="number", value=default_ma_target)
        ], width=6)
    ], className="my-3"),
    dbc.Row(
        dbc.Col(
            dbc.Button("Submit", id="submit-button", color="primary", className="mb-3 w-100"),
            width=12
        )
    ),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id="candlestick-chart"),
            width=12
        )
    ),
    dbc.Row(
        dbc.Col(
            html.Div(id="status-message", className="text-center text-danger my-2"),
            width=12
        )
    )
], fluid=False)

@app.callback(
    [Output('candlestick-chart', 'figure'),
     Output('status-message', 'children')],
    [Input('submit-button', 'n_clicks')],
    [State('ticker-input', 'value'),
     State('ma-target-input', 'value')]
)
def update_chart(n_clicks, ticker, ma_target):
    if not ticker:
        return {}, "Please enter a valid ticker symbol."
    
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            return {}, f"No data found for ticker '{ticker}'. Try another symbol."
        
        # Flatten columns if they are multi-indexed
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)
        
        # Define parameters for moving average projection
        ma_window = 150
        default_days_forward = 30

        # Get projection data
        days_needed, projection_df, error = predict_ma_projection(data, ma_window, ma_target, default_days_forward)

        if days_needed is not None and days_needed > default_days_forward:
            days_forward = int(round(days_needed))
            days_needed, projection_df, error = predict_ma_projection(data, ma_window, ma_target, days_forward)
        else:
            days_forward = default_days_forward

        if error:
            status_component = dbc.Alert(error, color="danger", className="mt-3")
        else:
            status_component = dbc.Alert(f"Projected to hit target in {days_needed} days.", color="info", className="mt-3")

        # Create a blank figure
        fig = go.Figure()

        # Add projection trace if available
        if projection_df is not None and not projection_df.empty:
            fig.add_trace(
                go.Scatter(
                    x=projection_df['Date'],
                    y=projection_df['Predicted_MA'],
                    mode='lines',
                    name='MA Projection',
                    line=dict(color='orange', dash='dash')
                )
            )

        # Add candlestick trace with explicit styling
        candlestick_trace = go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Historical',
            increasing=dict(line=dict(color='green')),
            decreasing=dict(line=dict(color='red'))
        )
        fig.add_trace(candlestick_trace)

        # Update layout and axes
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='#121212',
            plot_bgcolor='#121212',
            font_color='white',
            title=f"{ticker.upper()} Stock Price Over Time",
            xaxis_title="Date",
            yaxis_title="Price (USD)"
        )
        fig.update_xaxes(type='date')

        # Optionally update the y-axis range based on both traces
        y_min_hist = data['Low'].min().item()
        y_max_hist = data['High'].max().item()
        if projection_df is not None and not projection_df.empty:
            y_min_proj = projection_df['Predicted_MA'].min()
            y_max_proj = projection_df['Predicted_MA'].max()
            y_min = min(y_min_hist, y_min_proj) * 0.95
            y_max = max(y_max_hist, y_max_proj) * 1.05
        else:
            y_min = y_min_hist * 0.95
            y_max = y_max_hist * 1.05
        fig.update_yaxes(range=[y_min, y_max])
        
        return fig, status_component
    except Exception as e:
        return {}, f"Error fetching data or predicting: {e}"
    
if __name__ == '__main__':
    app.run_server(debug=True)