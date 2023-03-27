from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import AddressLog, LoginForm, SignUpForm
from app.models import Addresses, User
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    if current_user.is_authenticated:
        user_id = current_user.id
        user_addresses = Addresses.query.filter_by(user_id=user_id).all()
        return render_template('base.html', addresses=user_addresses)
    else:
        return render_template('base.html')




@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        check_user = db.session.execute(db.select(User).filter((User.username == username) | (User.email == email))).scalars().all()
        if check_user:
            flash("A user with that username and/or email already exists", "warning")
            return redirect(url_for('signup'))
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        flash(f"Thank you {new_user.username} for signing up!", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username, password)
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f'You have successfully logged in as {username}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect(url_for('index'))


@app.route('/address', methods=["GET", "POST"])
@login_required
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
            flash('This address has already been added.', 'warning')
            return redirect(url_for('address'))
        new_user = Addresses(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, user_id=current_user.id)
        flash(f"Your address has been successfully logged!", "success")
        return redirect(url_for('index'))
    return render_template('address.html', form=form)


@app.route('/edit/<id>', methods=["GET", "POST"])
@login_required
def edit_address(id):
    form = AddressLog()
    address_to_edit = Addresses.query.get(id)

    if form.validate_on_submit():
        address_to_edit.first_name = form.first_name.data
        address_to_edit.last_name = form.last_name.data
        address_to_edit.phone_number = form.phone_number.data
        address_to_edit.address = form.address.data
        db.session.commit()
        flash(f"{address_to_edit.first_name} has been edited!", "success")
        return redirect(url_for('index'))

    form.first_name.data = address_to_edit.first_name
    form.last_name.data = address_to_edit.last_name
    form.phone_number.data = address_to_edit.phone_number
    form.address.data = address_to_edit.address
    return render_template('edit.html', form=form, post=address_to_edit)


@app.route('/delete/<id>')
@login_required
def delete_address(id):
    address_to_delete = Addresses.query.get(id)
    if address_to_delete.author != current_user:
        flash("You do not have permission to delete this post", "danger")
        return redirect(url_for('index'))

    db.session.delete(address_to_delete)
    db.session.commit()
    flash(f"{address_to_delete.first_name} has been deleted", "info")
    return redirect(url_for('index'))
