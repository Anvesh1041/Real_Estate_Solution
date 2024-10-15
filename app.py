from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Anvesh1702@localhost:3306/real_estate'
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
    
class Notifications(db.Model):
    n_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), db.ForeignKey('user.username'))
    id = db.Column(db.Integer, db.ForeignKey('property.id'))
    n_text = db.Column(db.String(200))


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
    if current_user.username == 'Admin':
        notifications = Notifications.query.all()
        return render_template('admin_dashboard.html', notifications=notifications)
    else:
        properties = Property.query.all()
        return render_template('dashboard.html', properties=properties)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.is_authenticated:
        if current_user.username == 'Admin':
            # Fetch notifications for the admin user
            notifications = Notifications.query.all()

            # Render the admin dashboard template with the fetched notifications
            return render_template('admin_dashboard.html', notifications=notifications)
        else:
            flash('Unauthorized access')
            return redirect(url_for('index'))
    else:
        flash('Please log in first')
        return redirect(url_for('login'))

@app.route('/id_search', methods=['POST'])
@login_required
def id_search():
    property_id = request.form.get('property_id')
    if property_id:
        try:
            property_id = int(property_id)
        except ValueError:
            flash('Invalid Property ID. Please enter a valid number.', 'danger')
            return redirect(url_for('admin_dashboard'))

        # Fetch property by ID
        property = Property.query.get(property_id)
        
        if property:
            return redirect(url_for('edit_property', id=property.id))
        else:
            flash(f'Property with ID {property_id} not found.', 'danger')
            return redirect(url_for('admin_dashboard'))
    else:
        flash('Please enter a Property ID.', 'warning')
        return redirect(url_for('admin_dashboard'))

@app.route('/edit_property/<int:id>', methods=['GET'])
@login_required
def edit_property(id):
    property = Property.query.get(id)  # Use id to fetch the property
    if not property:
        flash('Property not found.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    print(property.id)
    return render_template('edit_property.html', property=property)

@app.route('/delete_notification/<int:notification_id>', methods=['GET','POST'])
@login_required
def delete_notification(notification_id):
    if current_user.username == 'Admin':
        notification = Notifications.query.get(notification_id)
        if notification:
            db.session.delete(notification)
            db.session.commit()
            flash('Notification deleted successfully', 'success')
        else:
            flash('Notification not found', 'danger')
    else:
        flash('Unauthorized access', 'danger')
    return redirect(url_for('admin_dashboard'))


@app.route('/delete_property/<int:property_id>', methods=['GET', 'POST'])
@login_required
def delete_property(property_id):
    if current_user.username == 'Admin':
        # First, delete all associated notifications for the property
        notifications = Notifications.query.filter_by(id=property_id).all()
        for notification in notifications:
            db.session.delete(notification)
        
        # Then delete the property itself
        property = Property.query.get(property_id)
        if property:
            db.session.delete(property)
            db.session.commit()
            flash('Property and associated notifications removed successfully', 'success')
        else:
            flash('Property not found', 'danger')
    else:
        flash('Unauthorized access', 'danger')
    return redirect(url_for('admin_dashboard'))




searched=False
@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    global searched
    location = request.args.get('location')
    if location:
        searched=True
    else:
        searched=False

    if request.method == 'POST':
        location = request.form['location']
        return redirect(url_for('buy', location=location))
    
    if location:
        # properties = []
        properties = Property.query.filter_by(location=location).all()
        properties = [prop for prop in properties if '/' not in prop.price]
        return render_template('buy.html', properties=properties, location=location)

    else :
        properties = Property.query.all()
        properties = [prop for prop in properties if '/' not in prop.price]
        return render_template('buy.html', properties=properties)


@app.route('/rent', methods=['GET', 'POST'])
@login_required
def rent():
    global searched
    location = request.args.get('location')
    if location:
        searched=True
    else:
        searched=False

    if request.method == 'POST':
        location = request.form['location']
        return redirect(url_for('rent', location=location))
    
    if location:
        properties = Property.query.filter_by(location=location).all()
        properties = [prop for prop in properties if '/' in prop.price]
        return render_template('rent.html', properties=properties, location=location)

    else :
        properties = Property.query.all()
        properties = [prop for prop in properties if '/' in prop.price]
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
    location = property.location

    if not property:
        flash('Property not found')
        return redirect(url_for('buy', location=location))

    # Determine the back URL
    global searched
    if searched:
        if property and '/' in property.price:
            back_url = url_for('rent', location=location) if location else url_for('rent')
        else:
            back_url = url_for('buy', location=location) if location else url_for('buy')
    else:
        if property and '/' in property.price:
            back_url = url_for('rent')
        else:
            back_url = url_for('buy') 

    return render_template('property_detail.html', property=property, location=location, back_url=back_url)

@app.route('/add_notification/<int:property_id>', methods=['POST'])
@login_required
def add_notification(property_id):
    price=request.form.get('price')
    # Generate notification text using your function
    if '/' in price:
        notification_text = generate_notification(property_id, current_user.username, "rent")
    else:
        notification_text = generate_notification(property_id, current_user.username, "buy")
    # Create a new notification
    notification = Notifications(username=current_user.username, id=property_id, n_text=notification_text)
    db.session.add(notification)
    db.session.commit()

    flash('Request submitted successfully')
    return redirect(url_for('property_detail', id=property_id))


def generate_notification(id,username,action):
    return f"{username} tries to {action} property with id {id}"

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if request.method == 'POST':
        price = request.form['price']
        location = request.form['location']
        bhk = request.form['bhk']
        address = request.form['address']
        image_link = request.form['image_link']

        # Create a new property with the image link
        property = Property(price=price, location=location, bhk=bhk, address=address, img_path=image_link)
        db.session.add(property)
        db.session.commit()

        # Generate notification
        notification_text = generate_notification(property.id, current_user.username, "sell")

        # Create a new notification
        notification = Notifications(username=current_user.username, id=property.id, n_text=notification_text)
        db.session.add(notification)
        db.session.commit()

        flash('Property added successfully!', 'success')
        return redirect(url_for('sell'))
    else:
        return render_template('sell.html')


if __name__ == '__main__':
    app.run(debug=True)
