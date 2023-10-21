import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from sqlalchemy import create_engine, text, MetaData
import logging
from datetime import datetime
from dash.exceptions import PreventUpdate  # Import PreventUpdate


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
                connections INT
            );
        """))
        conn.commit()
        logging.info("Table nodes initialized.")

initialize_db()

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


def update_dropdown_options_value(pathname, db_update_trigger):
    query = "SELECT name FROM nodes;"
    df = pd.read_sql_query(query, engine)
    if df.empty:
    	options = []
    	value = 'hello'
    else:
    	options = [{'label': name, 'value': name} for name in df['name']]
    	value = options[0]['value']
    return options, value


def update_input_name(selected_name):
    return selected_name



def update_connections_value(input_name):
    if not input_name:
        raise PreventUpdate  # Raise PreventUpdate if input_name is None or empty

    query = text("SELECT connections FROM nodes WHERE name = :name")
    with engine.connect() as conn:
        result = conn.execute(query, {"name": input_name}).fetchone()
    if result:
        return result[0]
    else:
        raise PreventUpdate

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

def update_database(n_clicks, input_name, connections_value):
    if n_clicks is None:
        raise PreventUpdate  # Prevent update on initial load

    if not input_name or connections_value is None:
        return  # Optionally, add some error handling here

    update_db(input_name, connections_value)

    # Return a unique value to trigger the graph change
    return str(datetime.utcnow())

def update_graph(pathname, db_update_trigger):
    if pathname is None and db_update_trigger is None:
        raise PreventUpdate  # Prevent update on initial load without a db update

    return get_db_graph()
