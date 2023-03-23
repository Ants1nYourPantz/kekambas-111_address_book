from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import AddressLog
from app.models import Addresses

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/address', methods=["GET", "POST"])
def address():
    form = AddressLog()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        print(first_name, last_name, phone_number, address)
        check_user = Addresses.query.filter((Addresses.phone_number == phone_number) | (Addresses.address == address)).all()
        if check_user:
            flash('A user with that username already exists.', 'warning')
            return redirect(url_for('address'))
        new_user = Addresses(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)
        flash(f"Your address has been successfully logged!", "success")
        return redirect(url_for('index'))
    return render_template('address.html', form=form)

