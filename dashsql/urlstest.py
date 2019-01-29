import dash
import dash_core_components as dcc
import dash_html_components as html
import dash, random, datetime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from sqlalchemy.orm import sessionmaker
from models import Title, db_connect, create_table, Domain, Subdomain

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



columns= [
    'domain_name',
    'subdomain_name',
    'title',
    'status',
    'response_len',
    'updated_on',
    # 'info',
]

engine = db_connect()
create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

query = session.query(Domain.domain_name, Subdomain.subdomain_name, Title.title,\
                        Title.status, Title.response_len, Title.updated_on).filter_by(domain_id=1).order_by(Domain.domain_name, Subdomain.subdomain_name)
query = query.join(Title).outerjoin(Subdomain)
data = []
for q in query:
    data.append(q._asdict())

page_1_layout = html.Div([
    dash_table.DataTable(
        id='datatable',
        columns=[{"name": i, "id": i} for i in columns],
        data=data,),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),

])

query = session.query(Domain.domain_name, Subdomain.subdomain_name, Title.title,\
                        Title.status, Title.response_len, Title.updated_on).filter_by(domain_id=2).order_by(Domain.domain_name, Subdomain.subdomain_name)
query = query.join(Title).outerjoin(Subdomain)
data = []
for q in query:
    data.append(q._asdict())


page_2_layout = html.Div([
    dash_table.DataTable(
        id='datatable2',
        columns=[{"name": i, "id": i} for i in columns],
        data=data,),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)