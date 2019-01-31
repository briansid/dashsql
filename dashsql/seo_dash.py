import dash, re
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from sqlalchemy.orm import sessionmaker
from models import Title, db_connect, create_table, Domain, Subdomain, Archive
from sqlalchemy import desc

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css']

engine = db_connect()
create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.append_script({"external_url": "https://code.jquery.com/jquery-3.3.1.js"})

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

columns = ['domain_name', 'subdomain_name']
columns += [column.key for column in Title.__table__.columns]
columns.remove('domain_id')
columns.remove('subdomain_id')


index_page = html.Div([
    dash_table.DataTable(
        id='datatable',
        columns=[{"name": i, "id": i} for i in columns],
        data=[],),
    dcc.Interval(
            id='interval-component',
            interval=1*5000, # in milliseconds
            n_intervals=0
    ),
],)


@app.callback(Output('datatable', 'data'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    query = session.query(Domain.domain_name, Subdomain.subdomain_name, Title)

    query = query.join(Title).outerjoin(Subdomain)

    query = query.order_by(
        Domain.domain_name,
        Subdomain.subdomain_name
    )

    data = []
    for q in query:
        qdict = q.Title.__dict__
        qdict['domain_name'] = q.domain_name
        qdict['subdomain_name'] = q.subdomain_name
        del qdict['_sa_instance_state']
        del qdict['domain_id']
        del qdict['subdomain_id']

        previous_data = session.query(Archive).filter_by(title_id=qdict['title_id'])\
                        .order_by(desc(Archive.updated_on)).first()

        if qdict['traffic'] < previous_data.traffic:
            qdict['traffic'] = str(qdict['traffic']) + ' ▼'
        elif qdict['traffic'] > previous_data.traffic:
            qdict['traffic'] = str(qdict['traffic']) + ' ▲'

        data.append(qdict)
    return data


archive_page = html.Div([
    dash_table.DataTable(
        id='archivetable',
        columns=[{"name": i, "id": i} for i in columns],
        data=[],),
],)


@app.callback(Output('archivetable', 'data'),
              [Input('url', 'pathname')])
def update_data(pathname):
    title_id = int(re.search(r'title_id=(.*)', pathname).group(1))

    query = session.query(
        Domain.domain_name,
        Subdomain.subdomain_name,
        Archive
    )

    query = query.join(Title).outerjoin(Subdomain).join(Archive)
    query = query.filter(Archive.title_id == title_id)

    data = []
    for q in query:
        qdict = q.Archive.__dict__
        qdict['domain_name'] = q.domain_name
        qdict['subdomain_name'] = q.subdomain_name
        del qdict['_sa_instance_state']
        data.append(qdict)
    return data


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname and pathname.startswith('/archive'):
        return archive_page
    else:
        return index_page


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