from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Anvesh1702@localhost:3306/mini_project'
app.config['SECRET_KEY'] = 'some-secret-string'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    username = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.password}')"

    def get_id(self):
        return self.username


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    price = db.Column(db.String(20))
    location = db.Column(db.String(50))
    bhk = db.Column(db.Integer)
    address = db.Column(db.String(100))
    img_path = db.Column(db.String(100))

    def __repr__(self):
        return f"Property('{self.price}', '{self.location}', {self.bhk}, '{self.address}', '{self.img_path}')"


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Check if username is already taken
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        # Check if password and confirm_password match
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('signup'))
        
        # Create a new user
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        
        return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html')


@app.route('/dashboard')
@login_required
def dashboard():
    properties = Property.query.all()
    return render_template('dashboard.html', properties=properties)


@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    if request.method == 'POST':
        location = request.form['location']
        properties = Property.query.filter_by(location=location).all()
        if not properties:
            flash('No properties found in that location')
            return redirect(url_for('buy'))
        else:
            return render_template('buy.html', properties=properties)
    else:
        properties = Property.query.all()
        return render_template('buy.html', properties=properties)



@app.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    if request.method == 'POST':
        property_id = request.form['property_id']
        property = Property.query.get(property_id)
        if property:
            db.session.delete(property)
            db.session.commit()
            return redirect(url_for('rent'))
        else:
            return 'Property not found'
    else:
        properties = Property.query.all()
        return render_template('rent.html', properties=properties)

@app.route('/search')
def search():
    location = request.args.get('location')
    properties = Property.query.filter(Property.location.like(f'%{location}%')).all()
    if not properties:
        return render_template('buy.html')
    return render_template('buy.html', properties=properties)


@app.route('/property/<int:id>')
def property_detail(id):
    property = Property.query.get(id)
    if not property:
        flash('Property not found')
        return redirect(url_for('buy'))
    return render_template('property_detail.html', property=property)


from werkzeug.utils import secure_filename
import os

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if request.method == 'POST':
        price = request.form['price']
        location = request.form['location']
        bhk = request.form['bhk']
        address = request.form['address']

        # Get the uploaded file
        file = request.files['image']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Save the file to the uploads folder
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Create a new property
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        property = Property(price=price, location=location, bhk=bhk, address=address, img_path=img_path)
        db.session.add(property)
        db.session.commit()
        return redirect(url_for('sell'))
    else:
        return render_template('sell.html')


if __name__ == '__main__':
    app.run(debug=True)
