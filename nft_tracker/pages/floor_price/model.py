from dash import html, dcc
from utils.data import get_all_strategies_data, get_btc_treasury_data
from datetime import datetime

def format_currency(value, decimals=0):
    """Format currency value"""
    if value is None:
        return '—'
    if value >= 1e9:
        return f'${value / 1e9:.2f}B'
    if value >= 1e6:
        return f'${value / 1e6:.2f}M'
    if value >= 1e3:
        return f'${value / 1e3:.1f}K'
    return f'${value:,.0f}' if decimals == 0 else f'${value:,.{decimals}f}'

def format_eth(value):
    """Format ETH value"""
    if value is None:
        return '—'
    return f'{value:.2f} Ξ'

def format_mnav(value):
    """Format mNAV value"""
    if value is None:
        return '—'
    return f'{value:.2f}x'

def format_btc(value):
    """Format BTC value"""
    if value is None:
        return '—'
    return f'{value:,.0f} ₿'

def get_signal(mnav, is_btc=False):
    """Get signal based on mNAV"""
    if mnav is None:
        return {'badge': html.Span('—', className='signal-na'), 'class': None}
    
    buy_threshold = 1.2 if is_btc else 1.0
    sell_threshold = 3.0 if is_btc else 5.0
    
    if mnav < buy_threshold:
        return {'badge': html.Span('Buy', className='signal-badge signal-buy'), 'class': 'discount'}
    elif mnav > sell_threshold:
        return {'badge': html.Span('Sell', className='signal-badge signal-sell'), 'class': 'premium'}
    else:
        return {'badge': html.Span('Hold', className='signal-badge signal-hold'), 'class': 'premium' if mnav >= 1 else 'discount'}

def create_strategy_table(strategies_data):
    """Create strategy tokens table"""
    if not strategies_data or len(strategies_data) == 0:
        return html.Div('Loading strategy data...', className='empty-state')
    
    # Sort by market cap
    sorted_data = sorted(
        [s for s in strategies_data if s.get('marketCap')],
        key=lambda x: x.get('marketCap', 0),
        reverse=True
    )
    
    # Add strategies without market cap at the end
    sorted_data.extend([s for s in strategies_data if not s.get('marketCap')])
    
    table_rows = []
    
    for s in sorted_data:
        mnav = s.get('mNav')
        signal_info = get_signal(mnav)
        mnav_class = 'mnav-premium' if mnav and mnav >= 1 else 'mnav-discount' if mnav else ''
        
        bar_width = min(100, (mnav / 20) * 100) if mnav else 0
        bar_class = 'premium' if mnav and mnav >= 1 else 'discount'
        
        table_rows.append(
            html.Tr([
                html.Td([
                    html.Span(s['name'], className='strategy-name'),
                    html.Span(s['tokenSymbol'], className='token-name')
                ]),
                html.Td(str(s.get('holdings', '—'))),
                html.Td(
                    format_eth(s.get('floorPriceEth')) if s.get('floorPriceEth') else html.Span('Pending', className='loading-cell'),
                    className='loading-cell' if not s.get('floorPriceEth') else ''
                ),
                html.Td(
                    format_currency(s.get('marketValueNfts')) if s.get('marketValueNfts') else html.Span('—', className='loading-cell'),
                    className='loading-cell' if not s.get('marketValueNfts') else ''
                ),
                html.Td(
                    format_currency(s.get('marketCap')) if s.get('marketCap') else html.Span('Pending', className='loading-cell'),
                    className='loading-cell' if not s.get('marketCap') else ''
                ),
                html.Td([
                    html.Div(
                        className='mnav-bar-container',
                        children=[
                            html.Div(
                                className='mnav-bar',
                                children=html.Div(
                                    className=f'mnav-bar-fill {bar_class}',
                                    style={'width': f'{bar_width}%'}
                                )
                            ),
                            html.Span(
                                format_mnav(mnav),
                                className=f'mnav-cell {mnav_class}'
                            )
                        ]
                    )
                ])
            ])
        )
    
    return html.Table(
        className='data-table',
        children=[
            html.Thead([
                html.Tr([
                    html.Th('Strategy Name'),
                    html.Th('NFT Holdings'),
                    html.Th('Floor Price'),
                    html.Th('Market Value of NFTs'),
                    html.Th('FD Market Cap'),
                    html.Th('mNAV')
                ])
            ]),
            html.Tbody(table_rows)
        ]
    )

def create_btc_table(btc_treasury_data, btc_price):
    """Create BTC treasury table"""
    if not btc_treasury_data or len(btc_treasury_data) == 0:
        return html.Div('Loading BTC treasury data...', className='empty-state')
    
    table_rows = []
    
    for company in btc_treasury_data:
        mnav = company.get('mNav')
        signal_info = get_signal(mnav, is_btc=True)
        mnav_class = 'mnav-premium' if mnav and mnav >= 1 else 'mnav-discount' if mnav else ''
        
        bar_width = min(100, (mnav / 5) * 100) if mnav else 0
        bar_class = 'premium' if mnav and mnav >= 1 else 'discount'
        
        table_rows.append(
            html.Tr([
                html.Td([
                    html.Span(company['name'], className='strategy-name'),
                    html.Span(company['ticker'], className='token-name')
                ]),
                html.Td(format_btc(company.get('btcHoldings'))),
                html.Td(format_currency(btc_price)),
                html.Td(format_currency(company.get('btcValue'))),
                html.Td(format_currency(company.get('marketCapPlaceholder'))),
                html.Td([
                    html.Div(
                        className='mnav-bar-container',
                        children=[
                            html.Div(
                                className='mnav-bar',
                                children=html.Div(
                                    className=f'mnav-bar-fill {bar_class}',
                                    style={'width': f'{bar_width}%'}
                                )
                            ),
                            html.Span(
                                format_mnav(mnav),
                                className=f'mnav-cell {mnav_class}'
                            )
                        ]
                    )
                ]),
                html.Td(signal_info['badge']),
                html.Td()
            ])
        )
    
    return html.Table(
        className='data-table',
        children=[
            html.Thead([
                html.Tr([
                    html.Th('Company Name'),
                    html.Th('BTC Holdings'),
                    html.Th('BTC Price'),
                    html.Th('Market Value of BTC'),
                    html.Th('FD Valuation'),
                    html.Th('mNAV'),
                    html.Th('Signal'),
                    html.Th()
                ])
            ]),
            html.Tbody(table_rows)
        ]
    )

def calculate_metrics(strategies_data):
    """Calculate aggregate metrics"""
    valid_data = [s for s in strategies_data if s.get('marketCap')]
    
    total_strategies = len(strategies_data)
    total_mcap = sum(s.get('marketCap', 0) for s in valid_data)
    total_nft_value = sum(s.get('marketValueNfts', 0) for s in strategies_data if s.get('marketValueNfts'))
    
    category_mnav = total_mcap / total_nft_value if (total_mcap and total_nft_value and total_nft_value > 0) else None
    
    valid_mnavs = [s.get('mNav') for s in strategies_data if s.get('mNav') is not None]
    avg_mnav = sum(valid_mnavs) / len(valid_mnavs) if valid_mnavs else None
    
    return {
        'totalStrategies': total_strategies,
        'totalMarketCap': total_mcap,
        'totalNftValue': total_nft_value,
        'categoryMnav': category_mnav,
        'avgMnav': avg_mnav
    }

def get_current_date():
    """Get current date formatted"""
    now = datetime.now()
    return now.strftime('%b %Y')
