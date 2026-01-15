import pandas as pd
from utils.api import get_response, PUB_URL, use_demo
from datetime import datetime

# Strategy Token Configuration
STRATEGIES = [
    {'id': 'punkstrategy', 'name': 'PunkStrategy', 'tokenSymbol': 'PNKSTR', 
     'coingeckoTokenId': 'punkstrategy', 'coingeckoNftId': 'cryptopunks', 'holdingsPlaceholder': 37},
    {'id': 'baycstrategy', 'name': 'BAYCStrategy', 'tokenSymbol': 'BAYSTR', 
     'coingeckoNftId': 'bored-ape-yacht-club', 'holdingsPlaceholder': 12},
    {'id': 'azukistrategy', 'name': 'AzukiStrategy', 'tokenSymbol': 'AZUKISTR', 
     'coingeckoNftId': 'azuki', 'holdingsPlaceholder': 8},
    {'id': 'moonbirdsstrategy', 'name': 'MoonbirdsStrategy', 'tokenSymbol': 'MOONSTR', 
     'coingeckoNftId': 'moonbirds', 'holdingsPlaceholder': 5},
    {'id': 'puddystrategy', 'name': 'PudgyStrategy', 'tokenSymbol': 'PUDGSTR', 
     'coingeckoNftId': 'pudgy-penguins', 'holdingsPlaceholder': 15},
    {'id': 'chimpersstrategy', 'name': 'ChimpersStrategy', 'tokenSymbol': 'CHMPSTR', 
     'coingeckoNftId': 'chimpers', 'holdingsPlaceholder': 22},
    {'id': 'vibestrategy', 'name': 'VibesStrategy', 'tokenSymbol': 'VIBESTR', 
     'coingeckoNftId': 'vibes', 'holdingsPlaceholder': 18},
    {'id': 'meebitsstrategy', 'name': 'MeebitsStrategy', 'tokenSymbol': 'MEEBSTR', 
     'coingeckoNftId': 'meebits', 'holdingsPlaceholder': 10}
]

# Bitcoin Treasury Companies
BTC_TREASURY_COMPANIES = [
    {'id': 'strategy', 'name': 'Strategy', 'ticker': 'MSTR', 'btcHoldings': 450000, 'marketCapPlaceholder': 80000000000}
]

# List of NFT collections to track
NFT_COLLECTIONS = [
    'cryptopunks',
    'bored-ape-yacht-club',
    'azuki',
    'moonbirds',
    'pudgy-penguins',
    'chimpers',
    'vibes',
    'meebits'
]

def get_nft_markets(order_by, num_entries):
    """
    Fetch market data for tracked NFT collections.
    Note: Demo keys don't support /nfts/markets endpoint,
    so we fetch individual NFT data instead.
    """
    nft_all = []

    for nft_id in NFT_COLLECTIONS[:num_entries]:
        nft_data = get_response(f"/nfts/{nft_id}", use_demo, {}, PUB_URL)
        
        if nft_data and "floor_price" in nft_data:
            temp_dict = dict(
                id = nft_data.get("id", nft_id),
                asset_platform_id = nft_data.get("asset_platform_id", ""),
                floor_price_native = nft_data.get("floor_price", {}).get("native_currency", 0),
                floor_price_usd = nft_data.get("floor_price", {}).get("usd", 0),
                market_cap_usd = nft_data.get("market_cap", {}).get("usd", 0),
                volume_24h_usd = nft_data.get("volume_24h", {}).get("usd", 0),
                floor_price_change = nft_data.get("floor_price_in_usd_24h_percentage_change", 0)
            )
            nft_all.append(temp_dict)
    
    if not nft_all:
        return pd.DataFrame(columns=['id', 'asset_platform_id', 'floor_price_native', 
                                    'floor_price_usd', 'market_cap_usd', 'volume_24h_usd', 'floor_price_change'])
    
    df = pd.DataFrame(nft_all)
    
    # Sort by the specified order (basic sorting since we don't have the full markets endpoint)
    if 'volume' in order_by:
        df = df.sort_values('volume_24h_usd', ascending='asc' in order_by)
    elif 'market_cap' in order_by:
        df = df.sort_values('market_cap_usd', ascending='asc' in order_by)
    
    return df

def get_nft_hist(nft_id, num_days, window_size):
    """
    Note: Historical market chart data requires Pro API subscription.
    With demo keys, we can only return current price data.
    This function will return an error message or current data only.
    """
    assert window_size <= num_days, "Window size is too big!"

    hist_params = {"days": num_days}
    hist_url = f"/nfts/{nft_id}/market_chart"
    
    nft_hist = get_response(hist_url, use_demo, hist_params, PUB_URL)
    
    # Check if the response indicates Pro API is required
    if not nft_hist or (isinstance(nft_hist, dict) and "status" in nft_hist and 
                       nft_hist.get("status", {}).get("error_code") == 10005):
        # Return current price data instead (as a single point)
        nft_data = get_response(f"/nfts/{nft_id}", use_demo, {}, PUB_URL)
        if nft_data and "floor_price" in nft_data:
            current_price = nft_data["floor_price"]["usd"]
            from datetime import datetime, timedelta
            
            # Create a minimal dataset with just current price
            # This is a workaround since demo keys don't support historical data
            now = datetime.now()
            times = [now - timedelta(days=i) for i in range(num_days, -1, -1)]
            prices = [current_price] * len(times)  # Repeat current price
            
            df_hist = pd.DataFrame({
                'Time': times,
                'Price_usd': prices
            })
            
            # Calculate SMA and EMA
            df_hist['SMA'] = df_hist['Price_usd'].rolling(window_size, min_periods=1).mean()
            df_hist['EMA'] = df_hist['Price_usd'].ewm(span=window_size, adjust=False).mean()
            
            return df_hist
        else:
            # Return empty dataframe if we can't get current data
            return pd.DataFrame(columns=['Time', 'Price_usd', 'SMA', 'EMA'])
    
    all_time, all_floor_price_usd = [], []

    if "floor_price_usd" in nft_hist:
        floor_price_usd = nft_hist["floor_price_usd"]

        for i in range(len(floor_price_usd)):
            time = floor_price_usd[i][0]
            all_time.append(time)
            
            price = floor_price_usd[i][1]
            all_floor_price_usd.append(price)

        df_hist = pd.DataFrame(list(zip(all_time, all_floor_price_usd)),
                               columns = ['Time', 'Price_usd'])

        df_hist["Time"] = pd.to_datetime(df_hist["Time"], unit = "ms")

        # Calculate SMA
        df_hist['SMA'] = df_hist['Price_usd'].rolling(window_size, min_periods=1).mean()

        # Calculate EMA
        df_hist['EMA'] = df_hist['Price_usd'].ewm(span = window_size, adjust=False).mean()
        
        return df_hist
    else:
        return pd.DataFrame(columns=['Time', 'Price_usd', 'SMA', 'EMA'])

def get_eth_btc_prices():
    """Fetch ETH and BTC prices"""
    try:
        params = {'ids': 'ethereum,bitcoin', 'vs_currencies': 'usd'}
        response = get_response('/simple/price', use_demo, params, PUB_URL)
        if response:
            eth_price = response.get('ethereum', {}).get('usd', 3200)
            btc_price = response.get('bitcoin', {}).get('usd', 100000)
            return eth_price, btc_price
    except:
        pass
    return 3200, 100000  # Fallback prices

def fetch_strategy_data(strategy, eth_price):
    """Fetch data for a single strategy token"""
    market_cap = None
    floor_price_eth = None
    
    # Try to fetch token market cap if coingeckoTokenId exists
    if strategy.get('coingeckoTokenId'):
        try:
            token_data = get_response(f"/coins/{strategy['coingeckoTokenId']}", use_demo, {}, PUB_URL)
            if token_data and 'market_data' in token_data:
                market_cap = token_data['market_data'].get('fully_diluted_valuation', {}).get('usd')
                if not market_cap:
                    market_cap = token_data['market_data'].get('market_cap', {}).get('usd')
        except:
            pass
    
    # Fetch NFT floor price
    if strategy.get('coingeckoNftId'):
        try:
            nft_data = get_response(f"/nfts/{strategy['coingeckoNftId']}", use_demo, {}, PUB_URL)
            if nft_data and 'floor_price' in nft_data:
                floor_price_eth = nft_data['floor_price'].get('native_currency')
        except:
            pass
    
    holdings = strategy.get('holdingsPlaceholder', 0)
    floor_price_usd = floor_price_eth * eth_price if floor_price_eth else None
    market_value_nfts = holdings * floor_price_usd if (holdings and floor_price_usd) else None
    mnav = market_cap / market_value_nfts if (market_cap and market_value_nfts and market_value_nfts > 0) else None
    
    return {
        'id': strategy['id'],
        'name': strategy['name'],
        'tokenSymbol': strategy['tokenSymbol'],
        'holdings': holdings,
        'floorPriceEth': floor_price_eth,
        'floorPriceUsd': floor_price_usd,
        'marketValueNfts': market_value_nfts,
        'marketCap': market_cap,
        'mNav': mnav
    }

def get_all_strategies_data():
    """Fetch data for all strategy tokens"""
    eth_price, btc_price = get_eth_btc_prices()
    strategies_data = []
    
    for strategy in STRATEGIES:
        strategy_data = fetch_strategy_data(strategy, eth_price)
        strategies_data.append(strategy_data)
    
    return strategies_data, eth_price, btc_price

def get_btc_treasury_data(btc_price):
    """Get BTC treasury company data"""
    btc_treasury_data = []
    for company in BTC_TREASURY_COMPANIES:
        btc_value = company['btcHoldings'] * btc_price
        mnav = company['marketCapPlaceholder'] / btc_value if btc_value > 0 else None
        btc_treasury_data.append({
            **company,
            'btcValue': btc_value,
            'mNav': mnav
        })
    return btc_treasury_data