import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from sqlalchemy import create_engine, text, MetaData
import logging
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



# Fetch environment variables
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']

# create connection
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def initialize_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS nodes (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                connections FLOAT
            );
        """))
        conn.commit()
        logging.info("Table nodes initialized.")



def update_db(name, connections):
    with engine.connect() as conn:
        trans = conn.begin()  # Begin a transaction
        try:
            query = text(f"""
                INSERT INTO nodes (name, connections)
                VALUES
                ('{name}', {connections})
                ON CONFLICT (name) DO UPDATE SET connections = EXCLUDED.connections;
            """)
            conn.execute(query)
            trans.commit()  # Commit the transaction
        except Exception as e:
            trans.rollback()  # Rollback the transaction in case of error
            logging.error(f"Database error: {e}")

def setup_database():
    logging.info('inserting rows into database')
    for name, connections in [
        ('smash', 20),
        ('hello', 30),
        ('jessica', 2),
        ('bitkarrot', 3),
        ]:
        update_db(name, connections)

def name_to_color(name):
    return f'#{hash(name) % 0xFFFFFF:06x}'


def get_db_graph():
    try:
        query = "SELECT * FROM nodes;"
        df = pd.read_sql_query(query, engine).sort_values('connections', ascending=False)
        colors = [name_to_color(name) for name in df['name']]
        fig = go.Figure(data=[go.Bar(x=df['name'], y=df['connections'], marker=dict(color=colors))])
        return fig
    except Exception as e:
        logging.error(f"Database error: {e}")
        return dash.no_update


def delete_db(name):
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            query = text(f"DELETE FROM nodes WHERE name = '{name}';")
            conn.execute(query)
            trans.commit()
        except Exception as e:
            trans.rollback()
            logging.error(f"Database error: {e}")


# Create a Dash app
app = dash.Dash(__name__)

# may be needed for iframe embedding
app.server.config.update({
    'SEND_FILE_MAX_AGE_DEFAULT': 0,
    "X_FRAME_OPTIONS": "SAMEORIGIN"
})

app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    ),
    html.H1("Insert new data"),
    dcc.Dropdown(id='name-dropdown'),
    dcc.Input(id='column1-input', type='text', placeholder='Enter value for name'),
    dcc.Input(id='column2-input', type='number', placeholder='Enter value for connections'),
    html.Button('Submit', id='submit-button'),
    html.Button('Delete', id='delete-button'),
    dcc.Graph(id='example-graph', figure=get_db_graph())
])



@app.callback(
    Output('name-dropdown', 'options'),
    [Input('interval-component', 'n_intervals')]
)
def update_dropdown(n):
    query = "SELECT name FROM nodes;"
    df = pd.read_sql_query(query, engine)
    if df.empty:
        return []
    return [{'label': name, 'value': name} for name in df['name']]

@app.callback(
    Output('column1-input', 'value'),
    [Input('name-dropdown', 'value')]
)
def update_name_input(selected_name):
    return selected_name


@app.callback(
    Output('example-graph', 'figure'),
    [Input('submit-button', 'n_clicks'),
     Input('delete-button', 'n_clicks')],
    [State('name-dropdown', 'value'),
     State('column2-input', 'value')]
)
def update_database(submit_n, delete_n, name, connections):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'submit-button':
        update_db(name, connections)
    elif button_id == 'delete-button':
        delete_db(name)

    return get_db_graph()


@app.callback(
    Output('name-dropdown', 'value'),  # You can choose what to update
    Input('delete-button', 'n_clicks'),
    State('name-dropdown', 'value')
)
def delete_entry(n, selected_name):
    if n is None:
        return dash.no_update
    with engine.connect() as conn:
        query = text(f"DELETE FROM nodes WHERE name='{selected_name}';")
        conn.execute(query)
    return None  # Reset the dropdown


def print_existing_tables():
    # Create a MetaData object and reflect the database
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Get the table names
    table_names = metadata.tables.keys()

    logging.info(f"Existing tables: {len(table_names)}")
    for table_name in table_names:
        logging.info(f" {table_name}")

        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, engine)
        logging.info(f'fetched {table_name}')
        logging.info(df)

if __name__ == '__main__':
    initialize_db()
    # Call this right after initialize_db() to check if the table exists
    print_existing_tables()

    setup_database()  # Move this line after initialize_db()

    logging.info('database initialized')
    app.run_server(debug=True, host='0.0.0.0', port=8050)


