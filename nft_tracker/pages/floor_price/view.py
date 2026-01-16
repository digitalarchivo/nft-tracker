import dash
from dash import html, dcc
import os

APP_TITLE = "Strategy Token mNAV Tracker"

# Assets folder path relative to this package
ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../assets')
ASSETS_PATH = os.path.abspath(ASSETS_PATH)  # Normalize path

app = dash.Dash(
    __name__,
    assets_folder=ASSETS_PATH,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&family=Fraunces:ital,wght@0,400;0,500;0,600;1,400&display=swap"
    ]
)

layout = html.Div(
    className='page-container',
    children=[
        # Header
        html.Header(
            className='header',
            children=[
                html.Div(
                    className='header-left',
                    children=[
                        html.H1('Strategy Token mNAV Tracker'),
                        html.Div(
                            className='subtitle',
                            children='"Strategy tokens transform illiquid NFTs into perpetual DeFi engines, the intersection of collectibles and programmable finance."'
                        )
                    ]
                ),
                html.Div(
                    className='header-right',
                    children=[
                        html.Div(
                            className='logo-container',
                            children=[
                                html.Div(
                                    className='logo',
                                    children='C'
                                ),
                                html.Div(
                                    className='company-info',
                                    children=html.Span('Cartography Capital', className='company-name')
                                )
                            ]
                        ),
                        html.Div(
                            className='date-box',
                            children=html.Span(id='currentDate', className='date')
                        )
                    ]
                )
            ]
        ),
        
        # Key Statistics Row
        html.Div(
            className='key-stats-row',
            children=[
                html.Div(
                    className='key-stats-box',
                    children=[
                        html.Div('Key Statistics', className='key-stats-header'),
                        html.Div(
                            className='key-stats-grid',
                            children=[
                                html.Div(
                                    className='key-stat',
                                    children=[
                                        html.Div(id='totalStrategies', className='key-stat-value', children='—'),
                                        html.Div('Strategies', className='key-stat-label')
                                    ]
                                ),
                                html.Div(
                                    className='key-stat',
                                    children=[
                                        html.Div(id='totalMarketCap', className='key-stat-value', children='—'),
                                        html.Div('Total FD MCap', className='key-stat-label')
                                    ]
                                ),
                                html.Div(
                                    className='key-stat',
                                    children=[
                                        html.Div(id='totalNftValue', className='key-stat-value', children='—'),
                                        html.Div('Total NFT Value', className='key-stat-label')
                                    ]
                                ),
                                html.Div(
                                    className='key-stat',
                                    children=[
                                        html.Div(id='categoryMnav', className='key-stat-value', children='—'),
                                        html.Div('Category mNAV', className='key-stat-label')
                                    ]
                                ),
                                html.Div(
                                    className='key-stat',
                                    children=[
                                        html.Div(id='avgMnav', className='key-stat-value', children='—'),
                                        html.Div('Avg mNAV', className='key-stat-label')
                                    ]
                                ),
                                html.Div(
                                    className='key-stat',
                                    children=[
                                        html.Div(id='ethPrice', className='key-stat-value', children='—'),
                                        html.Div('ETH Price', className='key-stat-label')
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='risk-box',
                    children=[
                        html.Div('Category Signal', className='risk-header'),
                        html.Div(
                            className='risk-bar',
                            children=[
                                html.Div(
                                    className='risk-level',
                                    children=[
                                        html.Div(className='risk-block sell'),
                                        html.Div(className='risk-block neutral active'),
                                        html.Div(className='risk-block buy')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='risk-labels',
                            children=[
                                html.Span('Sell'),
                                html.Span('Neutral'),
                                html.Span('Buy')
                            ]
                        ),
                        html.Div(
                            className='risk-description',
                            children='Strategy tokens carry medium-high risk due to NFT market volatility, smart contract risk, and liquidity constraints.'
                        )
                    ]
                )
            ]
        ),
        
        # Status Bar
        html.Div(
            className='status-bar',
            children=[
                html.Div(
                    className='status-indicator',
                    children=[
                        html.Div(id='statusDot', className='status-dot'),
                        html.Span(id='statusText', children='Initializing...')
                    ]
                ),
                html.Button('↻ Refresh', id='refreshBtn', className='refresh-btn', n_clicks=0)
            ]
        ),
        
        # Error Message
        html.Div(id='errorMessage', className='error-message', style={'display': 'none'}),
        
        # NFT Strategy Tokens Table
        html.Div(
            className='table-section',
            children=[
                html.Div(
                    className='table-header',
                    children=[
                        html.Span('01', className='section-tag'),
                        html.Span('NFT Strategy Token mNAV Analysis', className='section-title')
                    ]
                ),
                html.Div(id='strategyTable')
            ]
        ),
        
        # Bitcoin Treasury Table
        html.Div(
            className='table-section',
            children=[
                html.Div(
                    className='table-header',
                    children=[
                        html.Span('02', className='section-tag'),
                        html.Span('Bitcoin Treasury Companies (Comparison)', className='section-title')
                    ]
                ),
                html.Div(id='btcTable')
            ]
        ),
        
        # Methodology Notes
        html.Div(
            className='notes-section',
            children=[
                html.Div('Methodology Notes', className='notes-header'),
                html.Div(
                    className='notes-content',
                    children=[
                        html.P([
                            html.Strong('mNAV (Market NAV Multiple)'),
                            ' = FD Market Cap ÷ Market Value of Underlying Assets'
                        ]),
                        html.P([
                            html.Strong('Market Value'),
                            ' = Holdings × Floor/Spot Price'
                        ]),
                        html.P([
                            html.Strong('Signal Logic:'),
                            ' ',
                            html.Code('BUY'),
                            ' mNAV < 1.0x | ',
                            html.Code('SELL'),
                            ' mNAV > 5.0x | ',
                            html.Code('HOLD'),
                            ' 1.0x–5.0x'
                        ]),
                        html.P([
                            html.Strong('Data Sources:'),
                            ' ',
                            html.Code('CoinGecko API'),
                            ' for token/NFT prices, ',
                            html.Code('On-chain contract reads'),
                            ' for holdings'
                        ])
                    ]
                )
            ]
        ),
        
        # Footer
        html.Footer(
            className='footer',
            children=[
                html.Div(
                    className='footer-left',
                    children='© 2026 Cartography Capital. Data for informational purposes only. Not financial advice.'
                ),
                html.Div(
                    className='footer-links',
                    children=[
                        html.A('TokenStrategy', href='https://tokenstrategy.app/', target='_blank'),
                        html.A('DefiLlama', href='https://defillama.com/protocol/tokenworks', target='_blank'),
                        html.A('@token_works', href='https://twitter.com/token_works', target='_blank')
                    ]
                )
            ]
        ),
        
        # Store component to trigger initial load
        dcc.Store(id='data-store', data={'trigger': 0}),
        
        # Interval component for auto-refresh
        dcc.Interval(
            id='interval-component',
            interval=300000,  # 5 minutes
            n_intervals=0
        )
    ]
)
