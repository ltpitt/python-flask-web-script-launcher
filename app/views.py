from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from app.init_app import app, db
from app.models import UserProfileForm

# Imports for Calendar
from flask_wtf import Form
from wtforms import DateField
from datetime import date

# The Home page is accessible to anyone
@app.route('/')
def home_page():
    return render_template('pages/home_page.html')


# The User page is accessible to authenticated users (users that have logged in)
@app.route('/user', methods=['post','get'])
@login_required  # Limits access to authenticated users
def user_page():
    form = DateForm()
    if form.validate_on_submit():
        return form.dt.data.strftime('%x')
    return render_template('pages/user_page.html', form=form)

# The Admin page is accessible to users with the 'admin' role
@app.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')


@app.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('home_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html',
                           form=form)


class DateForm(Form):
    dt = DateField('Pick a Date', format="%m/%d/%Y")





