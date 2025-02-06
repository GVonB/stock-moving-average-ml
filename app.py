from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta

# Initialize the Dash app
app = Dash(__name__)

# Default stock ticker and date range
default_ticker = 'GOOG'
start_date = (datetime.today() - timedelta(days=300)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

# App layout
app.layout = html.Div([
    html.H1("Stock Price Candlestick Chart"),
    
    html.Div([
        html.Label("Enter Stock Ticker:"),
        dcc.Input(
            id='ticker-input',
            type='text',
            value=default_ticker,
            debounce=True  # update value only after user stops typing
        ),
        html.Button('Submit', id='submit-button', n_clicks=0)
    ]),
    
    dcc.Graph(id='candlestick-chart'),
    
    html.Div(id='status-message', style={'color': 'red'})
])

# Callback to update chart based on user input
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
        return fig, ""
    except Exception as e:
        return {}, f"Error fetching data: {e}"

if __name__ == '__main__':
    app.run_server(debug=True)