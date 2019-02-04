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


def fix_columns(ld):
    column_names = {
        'traffic': 'Traffic',
        'fd': 'FD',
        'pkh': 'РКН',
        'uptime': 'UPTime',
        'speed_test': 'Speed Test',
        'serp_desktop': 'SERP Desktop',
        'serp_mobile': 'SERP Mobile',
        'links': 'Links',
        'content': 'Content',
        'robots': 'Robots',
        'y_alert': 'Y.Alert',
        'g_alert': 'G.Alert',
        'exp_date': 'Exp. Date',
        'pages': 'Pages',
        'y_index': 'Y.Index',
        'g_index': 'G.Index',
    }
    for d in ld:
        for key in d:
            if key in column_names:
                d[column_names[key]] = d.pop(key)
    return ld


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
        id='dashboard',
        columns=[{"name": i, "id": i} for i in columns],
        data=[],),
    dcc.Interval(
            id='interval-component',
            interval=1*5000, # in milliseconds
            n_intervals=0
    ),
],)


@app.callback(Output('dashboard', 'data'),
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
        current_data = q.Title.__dict__
        current_data['domain_name'] = q.domain_name
        current_data['subdomain_name'] = q.subdomain_name
        del current_data['_sa_instance_state']
        del current_data['domain_id']
        del current_data['subdomain_id']

        previous_data = session.query(Archive).filter_by(title_id=current_data['title_id'])\
                        .order_by(desc(Archive.updated_on)).first()
        if previous_data:
            previous_data = previous_data.__dict__
        else:
            previous_data = current_data

        def add_arrow(param):
            if current_data[param] < previous_data[param]:
                # Значение  сильно отличаетя от предыдущего.
                if current_data[param]/previous_data[param] < 0.5:
                    current_data[param] = str(current_data[param]) + ' ▼▼'
                else:
                    current_data[param] = str(current_data[param]) + ' ▼'
            elif current_data[param] > previous_data[param]:
                current_data[param] = str(current_data[param]) + ' ▲'

        add_arrow('traffic')
        add_arrow('fd')

        data.append(current_data)
    return fix_columns(data)


archive_page = html.Div([
    dash_table.DataTable(
        id='archivetable',
        columns=[{"name": i, "id": i} for i in columns],
        data=[],),
    dcc.Interval(
            id='interval-component',
            interval=1*5000, # in milliseconds
            n_intervals=0
    )
],)


@app.callback(Output('archivetable', 'data'),
              [Input('url', 'pathname'),
              Input('interval-component', 'n_intervals')])
def update_data(pathname, n):
    title_id = int(re.search(r'title_id=(.*)', pathname).group(1))

    query = session.query(
        Domain.domain_name,
        Subdomain.subdomain_name,
        Archive
    )
    # TODO: Error if there is no data in arhive?
    query = query.join(Title).outerjoin(Subdomain).join(Archive)
    query = query.filter(Archive.title_id == title_id)

    data = []
    for q in query:
        archive_data = q.Archive.__dict__
        archive_data['domain_name'] = q.domain_name
        archive_data['subdomain_name'] = q.subdomain_name
        del archive_data['_sa_instance_state']
        data.append(archive_data)
    return fix_columns(data)


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