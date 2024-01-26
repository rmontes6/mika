# Import necessary libraries 
from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import main_app

# Connect to your app pages
from pages import expenses_sheet, savings_sheet, summary_sheet

# Connect the navbar to the index
from components import navbar

# Define the navbar
nav = navbar.Navbar()

# Define the index page layout
main_app.app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[]), 
])

# Create the callback to handle mutlipage inputs
@main_app.app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/incomesheet':
        return savings_sheet.layout
    if pathname == '/expensesheet':
        return expenses_sheet.layout
    if pathname == '/summarysheet':
        return summary_sheet.layout
    else: # if redirected to unknown link
        return summary_sheet.layout

# Run the app on localhost:8050
if __name__ == '__main__':
    main_app.app.run_server(debug=True)
