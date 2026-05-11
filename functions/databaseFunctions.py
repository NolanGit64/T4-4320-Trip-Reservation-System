import sqlite3
import click
from flask import g, current_app

DB_PATH = "db/reservations.db"
DB_SCHEMA = "db/schema.sql"

def create_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def get_db():
    if "db" not in g:
        g.db = create_connection()
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    connection = create_connection()
    with open(DB_SCHEMA, "r") as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

@click.command("init-db")
def init_db_command():
    """Wipe and recreate tables from schema.sql."""
    init_db()
    click.echo("Initialized the database.")

def register(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_reservations():
    db = get_db()
    reservations = db.execute("SELECT * FROM reservations").fetchall()
    return reservations

def get_seats_taken():
    db = get_db()
    # returns coordinate pairs of all seats taken in the format (row, column)
    seats_taken = db.execute("SELECT seatRow, seatColumn FROM reservations").fetchall()
    return seats_taken

def is_seat_taken(row, column):
    db = get_db()
    row_found = db.execute(
        "SELECT 1 FROM reservations WHERE seatRow = ? AND seatColumn = ?",
        (row, column),
    ).fetchone()
    return row_found is not None

def add_reservation(passenger_name, row, column, eticket):
    db = get_db()
    db.execute(
        "INSERT INTO reservations (passengerName, seatRow, seatColumn, eTicketNumber) "
        "VALUES (?, ?, ?, ?)",
        (passenger_name, row, column, eticket),
    )
    db.commit()

def delete_reservation(reservation_id):
    db = get_db()
    db.execute(
        "DELETE FROM reservations WHERE id = ?",
        (reservation_id,)
    )
    db.commit()

def validate_admin(username, password):
    db = get_db()
    admin = db.execute(
        "SELECT * FROM admins WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    return admin
