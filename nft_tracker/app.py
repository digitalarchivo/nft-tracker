# nft_tracker/app.py

from nft_tracker.pages.floor_price.view import app, layout
from nft_tracker.pages.floor_price.controller import *

# Set layout
app.layout = layout

# Expose Flask server for Vercel
server = app.server

if __name__ == "__main__":
    # Local development only
    app.run_server(host="0.0.0.0", port=8050, debug=False)