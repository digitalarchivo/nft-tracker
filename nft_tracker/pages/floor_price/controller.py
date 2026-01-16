from nft_tracker.pages.floor_price.view import app
from dash.dependencies import Input, Output
from dash import html
from nft_tracker.pages.floor_price.model import (
    create_strategy_table,
    create_btc_table,
    calculate_metrics,
    format_currency,
    format_mnav,
    get_current_date
)
from nft_tracker.utils.data import (
    get_all_strategies_data,
    get_btc_treasury_data
)

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
    """Update all data when refresh button is clicked or interval fires"""
    try:
        strategies_data, eth_price, btc_price = get_all_strategies_data()
        btc_treasury_data = get_btc_treasury_data(btc_price)
        
        metrics = calculate_metrics(strategies_data)
        
        strategy_table = create_strategy_table(strategies_data)
        btc_table = create_btc_table(btc_treasury_data, btc_price)
        
        from datetime import datetime
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

@app.callback(
    Output('statusDot', 'className', allow_duplicate=True),
    Output('statusText', 'children', allow_duplicate=True),
    Input('refreshBtn', 'n_clicks'),
    prevent_initial_call=True
)
def set_loading_status(n_clicks):
    """Set loading status when refresh button is clicked"""
    if n_clicks:
        return 'status-dot loading', 'Fetching data...'
    return 'status-dot', 'Ready'
