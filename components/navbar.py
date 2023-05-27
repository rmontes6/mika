from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
def Navbar():
    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Summary Sheet", href="/summarysheet")),
                dbc.NavItem(dbc.NavLink("Income Sheet", href="/incomesheet")),
                dbc.NavItem(dbc.NavLink("Expense Sheet", href="/expensesheet")),
            ] ,
            brand="Income & Expense Analysis App",
            brand_href="/summarysheet",
            color="#0460A9",
            dark=True,
        ), 
    ])
    return layout
