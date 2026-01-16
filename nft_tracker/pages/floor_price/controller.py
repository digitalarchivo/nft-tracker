import os
import sys
import time
from functools import lru_cache
from datetime import datetime

from dash.dependencies import Input, Output
from dash import html

# ----------------------------------------
# Ensure absolute imports work
# ----------------------------------------
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if BASE_PATH not in sys.path:
    sys.path.insert(0, BASE_PATH)

from nft_tracker.pages.floor_price.view import app
from nft_tracker.pages.floor_price.model import (
    create_strategy_table,
    create_btc_table,
    calculate_metrics,
    format_currency,
    format_mnav,
    get_current_date
)
from nft_tracker.utils.data import get_all_strategies_data, get_btc_treasury_data

# ---------------------------
# Caching to reduce API calls
# ---------------------------
@lru_cache(maxsize=1)
def get_cached_data(ttl_seconds=30):
    """
    Cache NFT + BTC data for ttl_seconds.
    Returns: strategies_data, eth_price, btc_price, btc_treasury_data, timestamp
    """
    strategies_data, eth_price, btc_price = get_all_strategies_data()
    btc_treasury_data = get_btc_treasury_data(btc_price)
    timestamp = time.time()
    return strategies_data, eth_price, btc_price, btc_treasury_data, timestamp

# ---------------------------
# Main update callback
# ---------------------------
@app.callback(
    [
        Output('currentDate', 'children'),
        Output('totalStrategies', 'children'),
        Output('totalMarketCap', 'children'),
        Output('totalNftValue', 'children'),
        Output('categoryMnav', 'children'),
        Output('avgMnav', 'children'),
        Output('ethPrice', 'children'),
        Output('strategyTable', 'children'),
        Output('btcTable', 'children'),
        Output('statusDot', 'className'),
        Output('statusText', 'children'),
        Output('errorMessage', 'children'),
        Output('errorMessage', 'style')
    ],
    [
        Input('refreshBtn', 'n_clicks'),
        Input('interval-component', 'n_intervals'),
        Input('data-store', 'data')
    ]
)
def update_all(refresh_clicks, n_intervals, data_store):
    """Update all NFT + BTC data."""
    try:
        strategies_data, eth_price, btc_price, btc_treasury_data, _ = get_cached_data()
        metrics = calculate_metrics(strategies_data)
        
        strategy_table = create_strategy_table(strategies_data)
        btc_table = create_btc_table(btc_treasury_data, btc_price)
        
        update_time = datetime.now().strftime('%H:%M:%S')
        
        return (
            get_current_date(),
            metrics['totalStrategies'],
            format_currency(metrics['totalMarketCap']),
            format_currency(metrics['totalNftValue']),
            format_mnav(metrics['categoryMnav']),
            format_mnav(metrics['avgMnav']),
            format_currency(eth_price),
            strategy_table,
            btc_table,
            'status-dot',
            f'Updated: {update_time}',
            '',
            {'display': 'none'}
        )
    except Exception as e:
        return (
            get_current_date(),
            '—', '—', '—', '—', '—', '—',
            html.Div('Error loading data', className='empty-state'),
            html.Div('Error loading data', className='empty-state'),
            'status-dot error',
            'Failed to fetch data',
            f'Error: {str(e)}',
            {'display': 'block'}
        )

# ---------------------------
# Loading status callback
# ---------------------------
@app.callback(
    Output('statusDot', 'className', allow_duplicate=True),
    Output('statusText', 'children', allow_duplicate=True),
    Input('refreshBtn', 'n_clicks'),
    prevent_initial_call=True
)
def set_loading_status(n_clicks):
    """Set loading indicator when refresh clicked."""
    if n_clicks:
        return 'status-dot loading', 'Fetching data...'
    return 'status-dot', 'Ready'
