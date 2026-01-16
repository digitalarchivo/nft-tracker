# api/index.py
from nft_tracker.pages.floor_price.view import app  # Use the Dash app instance from your view

# Vercel looks for this variable
app = app.server if hasattr(app, 'server') else app
