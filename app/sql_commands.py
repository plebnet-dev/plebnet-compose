# sql_commands.py

import pandas as pd
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, text, MetaData
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Fetch environment variables for database connection
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']

connection_string = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
# Create an engine for connecting to the PostgreSQL database
engine = create_engine(
    connection_string,
    pool_size=10,  # Adjust pool_size and max_overflow to your needs
    max_overflow=20
)
logging.info(f"connecting to db at: {connection_string.replace(DB_PASS,'****')}")

# Create a new session factory bound to the engine
SessionFactory = sessionmaker(bind=engine)
# Create a scoped session to ensure thread-safety
db_session = scoped_session(SessionFactory)

NODES_QUERY = text("SELECT name FROM nodes;")  # Predefined query to fetch node names

def initialize_db():
    """Initialize the database by creating the 'nodes' table if it doesn't exist."""
    session = db_session()  # Get a new session
    try:
        # Execute a raw SQL query to create the 'nodes' table
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS nodes (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                connections INT
            );
        """))
        session.commit()  # Commit the transaction
        logging.info("Table nodes initialized.")
    except Exception as e:
        session.rollback()  # Rollback the transaction in case of error
        raise  # Re-raise the exception to propagate the error
    finally:
        db_session.remove()  # Ensure the session is closed when done

def update_db(name, connections):
    """Update the database with a new node or update an existing node's connections."""
    session = db_session()  # Get a new session
    try:
        # Execute a raw SQL query to insert/update a node
        query = text("""
            INSERT INTO nodes (name, connections)
            VALUES
            (:name, :connections)
            ON CONFLICT (name) DO UPDATE SET connections = EXCLUDED.connections;
        """)
        session.execute(query, {"name": name, "connections": connections})  # Parameterized query for safety
        session.commit()  # Commit the transaction
    except Exception as e:
        session.rollback()  # Rollback the transaction in case of error
        logging.error(f"Database error: {e}")
    finally:
        db_session.remove()  # Ensure the session is closed when done

def delete_db(name):
    """Delete a node from the database by its name."""
    session = db_session()  # Get a new session
    try:
        # Execute a raw SQL query to delete a node
        query = text("DELETE FROM nodes WHERE name = :name")
        session.execute(query, {"name": name})  # Parameterized query for safety
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Database error: {e}")
    finally:
        db_session.remove()  # Ensure the session is closed when done

def setup_database():
    """Sample code for initializing the DB with rows."""
    logging.info('inserting rows into database')
    # List of sample nodes to insert into the database
    for name, connections in [
        ('smash', 20),
        ('hello', 30),
        ('jessica', 2),
        ('bitkarrot', 3),
        ]:
        update_db(name, connections)  # Insert/update each node

def print_existing_tables():
    """Print the existing tables and their rows in the database."""
    session = db_session()  # Get a new session
    try:
        # Reflect the database metadata to discover existing tables
        metadata = MetaData()
        metadata.reflect(bind=session.bind)
        table_names = metadata.tables.keys()  # Get the table names

        logging.info(f"Existing tables: {len(table_names)}")
        for table_name in table_names:
            logging.info(f" {table_name}")
            query = text(f"SELECT * FROM {table_name};")
            df = pd.read_sql_query(query, session.bind)  # Execute the query and fetch data into a DataFrame
            logging.info(f'fetched {table_name}')
            logging.info(df)
    finally:
        db_session.remove()  # Ensure the session is closed when done

def fetch_db_data(query):
    """Fetch data from the database using a given query."""
    session = db_session()  # Get a new session
    try:
        df = pd.read_sql_query(query, session.bind)  # Execute the query and fetch data into a DataFrame
        return df
    finally:
        db_session.remove()  # Ensure the session is closed when done

def update_connections_value(input_name):
    """Fetch the connections value of a node by its name."""
    if not input_name:
        return "No input name provided"  # Return early if no input_name provided

    query = text("SELECT connections FROM nodes WHERE name = :name")
    session = db_session()  # Get a new session
    try:
        result = session.execute(query, {"name": input_name}).fetchone()
        if result:
            return result[0]
        else:
            return "No result found"  # Return a message if no result found
    finally:
        db_session.remove()  # Close the session when done

