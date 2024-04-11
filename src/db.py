import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  #Return row that behave like  dicts.

    return g.db

#Check if a g.db was set.
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#Function to run SQL commands
def init_db():
    db = get_db()  # Get the database connection.

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db') # Define a command line command.
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)  # Call function when cleaning up after returning the response.
    app.cli.add_command(init_db_command) # Adds new command