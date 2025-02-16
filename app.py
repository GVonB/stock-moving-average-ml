# app.py
import dash
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from predictor import predict_ma_projection  # and any others you need

app = Dash(__name__)

default_ticker = 'GOOG'
start_date = (datetime.today() - timedelta(days=300)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

app.layout = html.Div([
    html.H1("Stock Price Candlestick Chart with MA Projection"),
    html.Div([
        html.Label("Enter Stock Ticker:"),
        dcc.Input(
            id='ticker-input',
            type='text',
            value=default_ticker,
            debounce=True
        ),
        html.Button('Submit', id='submit-button', n_clicks=0)
    ]),
    dcc.Graph(id='candlestick-chart'),
    html.Div(id='status-message', style={'color': 'red'})
])

@app.callback(
    [Output('candlestick-chart', 'figure'),
     Output('status-message', 'children')],
    [Input('submit-button', 'n_clicks')],
    [State('ticker-input', 'value')]
)
def update_chart(n_clicks, ticker):
    if not ticker:
        return {}, "Please enter a valid ticker symbol."
    
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            return {}, f"No data found for ticker '{ticker}'. Try another symbol."
        
        # Create candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )])
        
        fig.update_layout(
            title=f"{ticker.upper()} Stock Price Candlesticks",
            xaxis_title="Date",
            yaxis_title="Price (USD)"
        )
        
        ma_window = 150
        ma_target = 200  # TODO - Handle as user input
        days_needed, projection_df, error = predict_ma_projection(data, ma_window, ma_target, days_forward=30)
        
        if error:
            status = error
        else:
            status = f"Projected to hit target in {days_needed} days."
            # Add projection trace to the chart
            fig.add_trace(
                go.Scatter(
                    x=projection_df['Date'],
                    y=projection_df['Predicted_MA'],
                    mode='lines',
                    name='MA Projection',
                    line=dict(color='orange', dash='dash')
                )
            )
        
        return fig, status
    except Exception as e:
        return {}, f"Error fetching data or predicting: {e}"

if __name__ == '__main__':
    app.run_server(debug=True)