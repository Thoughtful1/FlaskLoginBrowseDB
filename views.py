from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from models import students, User


@app.route('/')
def show_all():

    if session.get('logged_in'):
        return render_template('show_all.html', message="Logged in!", students=students.query.all())
    else:
        flash("Enter User credentials")
        return render_template('login.html', message="Sign in to proceed!")
        # return render_template('show_all.html', students=students.query.all())


@app.route('/delete/<int:pid>', methods=['POST'])
def delete(pid):

    p = students.query.get(pid)
    flash('Student {0} deleted'.format(p.name), 'success')
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('show_all'))


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:

            student = students(request.form['name'], request.form['city'],
                               request.form['addr'], request.form['pin'], )

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/edit/<int:pid>', methods=['GET', 'POST'])
def edit(pid):
    p = students.query.get(pid)
    # user = students.query().filter(students.id == pid)

    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            p.name = request.form['name']
            p.city = request.form['city']
            p.addr = request.form['addr']
            p.pin = request.form['pin']

            """student = students(request.form['name'], request.form['city'],
                               request.form['addr'], request.form['pin'])
            """

            db.session.commit()
            flash('Record was successfully edited')
            return redirect(url_for('show_all'))
    return render_template('edit.html', p=p)
    # return redirect(url_for('show_all'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message=None
    if request.method == 'POST':
        try:
            if request.form['password'] == '' or request.form['username'] == '':
                flash("No password or username provided")
                return render_template('signup.html')
            else:
                db.session.add(User(username=request.form['username'], password=request.form['password']))
                db.session.commit()
                return redirect(url_for('login'))
        except:
            flash("User Already Exists")
            return render_template('signup.html', message=message)
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':

        return render_template('login.html')
    else:
        if request.form['password'] == '' or request.form['username'] == '':
            flash("No password or username provided")
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('show_all'))
        return render_template('login.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    flash("You have been successfully logged out!")
    return redirect(url_for('login'))
