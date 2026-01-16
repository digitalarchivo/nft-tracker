from pages.floor_price.view import app, layout
from pages.floor_price.controller import *

app.layout = layout

# 🔹 Vercel needs this
server = app.server

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)
