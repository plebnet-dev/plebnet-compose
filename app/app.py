import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine, text
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

def setup_database(engine):
    logging.info('initializing database')
    with engine.connect() as conn:
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    connections FLOAT
                );
            """))
            conn.execute(text("""
                INSERT INTO nodes (name, connections)
                VALUES
                ('smash', 20),
                ('hello', 30),
                ('jessica', 40),
                ('bitcarrot', 10)
                ON CONFLICT DO NOTHING;
            """))
        except Exception as e:
            logging.error(f"Database error: {e}")


setup_database(engine)

# Execute a query and load the result into a pandas DataFrame
query = "SELECT * FROM nodes;"
df = pd.read_sql_query(query, engine)


# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Insert new data"),
    dcc.Input(id='column1-input', type='text', placeholder='Enter value for name'),
    dcc.Input(id='column2-input', type='number', placeholder='Enter value for connections'),
    html.Button('Submit', id='submit-button'),
    dcc.Graph(
        id='example-graph',
        figure=px.scatter(df, x='name', y='connections')
    )
])


@app.callback(
    Output('example-graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('column1-input', 'value'), State('column2-input', 'value')]
)
def update_database(n, col1_value, col2_value):
    if n is None:
        return dash.no_update  # Don't update the graph on initial load
    logging.info(f'updating db with {col1_value}, {col2_value}')
    with engine.connect() as conn:
        try:
            query = text(f"""
                INSERT INTO nodes (name, connections)
                VALUES
                ('{col1_value}', {col2_value})
                ON CONFLICT DO NOTHING;
            """)
            conn.execute(query)
            logging.info(query)
            logging.info('complete')
        except Exception as e:
            logging.error(f"Database error: {e}")
            return dash.no_update  # Don't update the graph if there's an error

    # Fetch updated data and refresh the graph
    try:
        query = "SELECT * FROM nodes;"
        df = pd.read_sql_query(query, engine)
        logging.info('fetched new dataframe')
    except Exception as e:
        logging.error(f"Database error: {e}")
        return dash.no_update  # Don't update the graph if there's an error
    logging.info('returning new plot')
    logging.info(df)
    return px.scatter(df, x='name', y='connections', title=str(datetime.datetime.now()))


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)



