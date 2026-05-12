from flask import current_app as app
from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash
from .forms import *
from functions import databaseFunctions


main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        if request.form.get("menu_option") == "admin":
            return redirect(url_for('main.admin'))
        if request.form.get("menu_option") == "reservations":
            return redirect(url_for('main.reservations'))
        else:
            flash("Invalid menu option, try again.")
            return render_template('index.html')
        
@main_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    try:
        form = LoginForm()
        delete_form = DeleteForm()
        username = None
        password = None
        admin = None
        delete_id = None
        if request.method == "POST":
            if request.form.get('username') and request.form.get('password'):
                username = request.form.get('username')
                password = request.form.get('password')
                admin = databaseFunctions.validate_admin(username, password)
            elif request.form.get('delete_id'):
                delete_id = request.form.get('delete_id')
            
            if admin or delete_id:

                if delete_id:
                    databaseFunctions.delete_reservation(delete_id)
                    flash(f"Reservation {delete_id} deleted.")
                
                reservations = databaseFunctions.get_reservations()
                seating_chart_matrix = _build_chart()
                total_sales = get_sales()
                return render_template('admin.html', form=form, delete_form=delete_form, reservations=reservations, seating_chart_matrix=seating_chart_matrix, total_sales=total_sales)
            else:
                return render_template('admin.html', form=form, err="Invalid username or password.")
        
        return render_template('admin.html', form=form)

    except Exception as e:
        flash("ERROR: unexpected login failure")
        print(f"{e}")
        return redirect(url_for('main.index'))

def _build_chart():
    taken = {(r["seatRow"], r["seatColumn"]) for r in databaseFunctions.get_seats_taken()}
    return [
        ["X" if (row, col) in taken else "O" for col in range(COLUMNS)]
        for row in range(ROWS)
    ]

def get_sales():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)] #   Returns a 12 x 4 matrix of prices
    sales = 0
    for reservation in {(r["seatRow"], r["seatColumn"]) for r in databaseFunctions.get_seats_taken()}:
        sales += cost_matrix[reservation[0]][reservation[1]]
    print(sales)
    return sales

def generate_ticket(s1,s2):
    result = ""
    total = max(len(s1), len(s2))
    for i in range(total):
        if i < len(s1):
            result += s1[i]
        if i < len(s2):
            result += s2[i]
    return result

@main_bp.route('/reservations', methods=['GET', 'POST'])
def reservations():
    form = ReservationForm()

    if form.validate_on_submit():
        row = int(form.row.data) 
        column = int(form.column.data)
        passenger_name = f"{form.first_name.data}"

        if databaseFunctions.is_seat_taken(row, column):
            flash(f"Seat (row {row + 1}, seat {column + 1}) is already taken. Choose another.")
        else:
            eticket = generate_ticket(form.first_name.data, "INFOTC4320")
            databaseFunctions.add_reservation(passenger_name, row, column, eticket)
            flash(f"Congratulations {passenger_name}! Row {row + 1}, Seat {column + 1}, is now reserved for you. Enjoy your trip!\nE-Ticket: {eticket}")
            return redirect(url_for('main.reservations'))

    chart = _build_chart()
    return render_template('reservations.html', form=form, chart=chart)


