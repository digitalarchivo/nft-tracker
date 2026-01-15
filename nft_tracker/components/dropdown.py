from dash import dcc

def nft_dropdown():
    dropdown = dcc.Dropdown(id = 'NFT_ID',
    options = [
    {'label': 'CryptoPunks', 'value': 'cryptopunks'},
    {'label': 'Bored Ape Yacht Club', 'value': 'bored-ape-yacht-club'},
    {'label': 'Azuki', 'value': 'azuki'},
    {'label': 'Moonbirds', 'value': 'moonbirds'},
    {'label': 'Pudgy Penguins', 'value': 'pudgy-penguins'},
    {'label': 'Chimpers', 'value': 'chimpers'},
    {'label': 'Vibes', 'value': 'vibes'},
    {'label': 'Meebits', 'value': 'meebits'}
    ],
    value = 'cryptopunks')
    
    return dropdown

def orderby_dropdown():
    dropdown = dcc.Dropdown(id = 'ORDER_BY',
    options = [
    {'label': 'h24_volume_native_asc', 'value':'h24_volume_native_asc' },
    {'label': 'h24_volume_native_desc', 'value':'h24_volume_native_desc'},
    {'label': 'h24_volume_usd_asc', 'value':'h24_volume_usd_asc'},
    {'label': 'h24_volume_usd_desc', 'value':'h24_volume_usd_desc'},
    {'label': 'market_cap_usd_asc', 'value':'market_cap_usd_asc'},
    {'label': 'market_cap_usd_desc', 'value':'market_cap_usd_desc'}
    ],
    value = 'h24_volume_native_desc')
    
    return dropdown

def mode_dropdown():
    dropdown = dcc.Dropdown(id = 'MODE',
    options = [
    {'label': 'Market data', 'value':'market_data' },
    {'label': 'Historical floor price', 'value':'hist_floor_price'},
    {'label': 'Alert email', 'value':'alert_email'},
    ],
    value = 'market_data')
    
    return dropdown