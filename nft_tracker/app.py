from pages.floor_price.view import app, layout
from pages.floor_price.controller import *

app.layout = layout

if __name__ == '__main__':
    app.run(port=8050, debug=False)