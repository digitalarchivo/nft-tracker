# api/index.py
from nft_tracker.pages.floor_price.view import app  # your Dash app
app = app.server  # expose Flask server for Vercel
