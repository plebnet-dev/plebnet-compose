# callbacks.py

import os
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from dash import callback_context, html
import logging
from datetime import datetime
import hashlib

from sql_commands import update_db, delete_db, \
    print_existing_tables, fetch_db_data, update_connections_value, \
    update_color_value, NODES_QUERY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def update_dropdown_options_value(pathname, db_update_trigger):
    """Update dropdown options and value based on DB data and update trigger."""
    # Fetch data from the database using the predefined query
    df = fetch_db_data(NODES_QUERY)  
    if df.empty:
        options = []  # Set empty options if data is empty
        value = 'hello'
        return options, value

    # Fetch options from db
    names = list(df['name'])
    options = [{'label': name, 'value': name} for name in names]  # Build options from names

    # Update the value based on db update trigger
    if db_update_trigger is not None:
        trigger_name = db_update_trigger.split(',')[-1]
        if trigger_name in names:
            value = trigger_name
        else:
            value = names[0]
    else:
        value = names[0]
    return options, value

def update_input_name(selected_name):
    """Return the selected name as is. This function acts as a passthrough."""
    return selected_name



def update_db_table(pathname, db_update_trigger):
    query = "SELECT * FROM nodes;"
    df = fetch_db_data(query).sort_values('connections', ascending=False)
    
    if df.empty:
        return []  # return an empty list if there's no data

    # Convert DataFrame to a list of dictionaries for DataTable
    data = df.to_dict('records')
    return data


def get_db_graph():
    """Generate and return a bar graph showing node connections from the DB with a log scale on the y-axis."""
    try:
        query = "SELECT * FROM nodes;"
        # Fetch data from the database and sort it based on connections
        df = fetch_db_data(query).sort_values('connections', ascending=False)
        try:
            # Generate a color for each name
            colors = df['color']
        except:
            logging.error(df.columns)
            raise
        # Create a bar graph using Plotly with a log scale on the y-axis
        fig = go.Figure(data=[go.Bar(x=df['name'], y=df['connections'], marker=dict(color=colors))])

        # Update layout for dark theme and set y-axis to log scale
        fig.update_layout(
            uirevision=1,
            xaxis=dict(
                title='node name',
                title_font=dict(color='white'),  # Set x-axis title color to white
                tickfont=dict(color='white'),  # Set x-axis tick labels color to white
            ),
            yaxis=dict(
                title='number of connections (log scale)',  # Update y-axis title
                title_font=dict(color='white'),  # Set y-axis title color to white
                tickfont=dict(color='white'),  # Set y-axis tick labels color to white
                type='log',  # Set y-axis scale to log
            ),
            plot_bgcolor='#2c2c2c',  # Set plot background color to #2c2c2c
            paper_bgcolor='#2c2c2c',  # Set paper background color to #2c2c2c
            title=dict(
                text='LN node connections',
                font=dict(
                    color='white'  # Set title color to white
                )
            ),
            font=dict(
                color='white'  # Set global font color to white
            )
        )

        return fig

    except Exception as e:
        logging.error(f"Database error: {e}")
        return dash.no_update

def update_or_delete_entry(submit_n, delete_n, input_name, connections_value, color_value):
    """Update or delete an entry in the DB based on user interaction."""
    ctx = callback_context  # Get callback context to identify which button was pressed

    if not ctx.triggered:
        raise PreventUpdate  # Prevent update on initial load

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]  # Extract button ID from the context

    # Update the database if submit button was pressed and necessary input is provided
    if button_id == 'submit-button' and input_name and connections_value is not None:
        update_db(input_name, connections_value, color_value)
    # Delete from the database if delete button was pressed and input name is provided
    elif button_id == 'delete-button' and input_name:
        delete_db(input_name)
    else:
        return  # Optionally, add some error handling here

    # Return the current UTC timestamp as a string
    # this gets stored in a hidden div
    # input_name will be parsed to set the value of the dropdown
    return str(datetime.utcnow()) + ',' + input_name

def update_graph(pathname, db_update_trigger):
    """Update the graph based on the pathname and db update trigger."""
    ctx = callback_context  # Get the callback context to check the triggered inputs

    # Prevent update on initial load or if db_update_trigger is None
    if not ctx.triggered and db_update_trigger is None:
        raise PreventUpdate

    return get_db_graph()  # Return the updated graph

