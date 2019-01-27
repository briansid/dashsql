import dash, random, datetime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from sqlalchemy.orm import sessionmaker
from models import Title, db_connect, create_table, Domain, Subdomain

# columns= [column.key for column in Title.__table__.columns]
columns= ['domain_name',
 'subdomain_name',
 'title',
 'status',
 'response_len',
 'created_on',
 'updated_on',]

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css']

engine = db_connect()
create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.append_script({"external_url": "https://code.jquery.com/jquery-3.3.1.js"})

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable',
        columns=[{"name": i, "id": i} for i in columns],
        data=[],),
    dcc.Interval(
            id='interval-component',
            interval=1*5000, # in milliseconds
            n_intervals=0
    ),
    # html.Div(id='container', className="alert alert-danger")
],)


@app.callback(Output('datatable', 'data'),
              [Input('interval-component', 'n_intervals'),])
def update_metrics(n):
    # query = session.query(Title).order_by(Title.domain_id, Title.subdomain_id)
    
    query = session.query(Domain.domain_name, Subdomain.subdomain_name, Title.title,\
                        Title.status, Title.response_len, Title.created_on, Title.updated_on).order_by(Domain.domain_name, Subdomain.subdomain_name)
    query = query.join(Title).outerjoin(Subdomain)
    data = []
    for q in query:
        data.append(q._asdict())
    return data

# @app.callback(Output('container', 'children'),
#               [Input('datatable', 'data')])
# def alert(data):
#     alert_sites = []
#     for n, d in enumerate(data):
#         if d['PKH'] == "site" or d['PKH'] == "site 192.168.0.1":
#             alert_sites.append(d['Domain'])
#     return html.Div('PKH ALERT: %s' % ', '.join(alert_sites), style={'color': 'black'})

app.run_server()

# if __name__ == '__main__':
#     app.run_server(debug=True)