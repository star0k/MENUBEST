import json
import os
from flask import Flask, flash, render_template, request, jsonify, url_for
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import data_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_wtf.file import FileField



UPLOAD_FOLDER = '/home/star0k/mysite/static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# best
ADMIN_USERNAME = 'pbkdf2:sha256:260000$9tKJdfyn$8fe82568745de2f164e3828a05307bf3ef7e7940f5cb5b578177a2f602890ffe'
# you should make this stronger
ADMIN_PASSWORD = 'pbkdf2:sha256:260000$lfrWAGkJ$5e5cd9ac32372e73e2ef7f9c725ca704dacd568ff5720d2273e9aa3ec9c99c3d'

app = Flask(__name__)
database = os.environ.get('DATABASE_URL')


app.config['SQLALCHEMY_DATABASE_URI'] = database
db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "gonna be awessom"
login_manager = LoginManager()
login_manager.init_app(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
resoptions = ['Name', 'Rid', 'Image', 'Location', 'Phone',
              'Open_Time', 'Close_Time', 'Week_Time', 'Recommended']
resoptions_Names = {'Name': 'Restaurant Name',
                    'Rid': 'Restaurant ID',
                    'Image': 'Restaurant Cover Image',
                    'Location': 'Restaurant Location',
                    'Phone': 'Restaurant Phone',
                    'Open_Time': 'Restaurant Open Time',
                    'Close_Time': 'Restaurant Close Time',
                    'Week_Time': 'Restaurant Week Time',
                    'Recommended': 'Restaurant Recommendation Status'}


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class LoginForm(FlaskForm):
    email = StringField('Email', render_kw={
                        "placeholder": "Email"}, validators=[data_required()])
    password = PasswordField('Password', render_kw={
                             "placeholder": "Password"}, validators=[data_required()])
    submit = SubmitField('Login')


class AddRes(FlaskForm):
    Name = StringField('Restaurant Name', validators=[data_required()])
    Rid = StringField('Restaurant ID', validators=[data_required()])
    Image = FileField('Cover Image')
    Location = StringField('Restaurant Location')
    Phone = StringField('Restaurant Phone')
    Open_Time = StringField('Restaurant Opens at')
    Close_Time = StringField('Restaurant Closes at')
    Week_Time = StringField('Restaurant Work Days')
    Recommended = StringField('Restaurant Reccomendation')
    Submit = SubmitField('ADD')


class Resturants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Rid = db.Column(db.String, unique=True, nullable=False)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    Image = db.Column(db.String, unique=False, nullable=False)
    Location = db.Column(db.String, unique=False, nullable=False)
    Phone = db.Column(db.String, unique=False, nullable=False)
    Open_Time = db.Column(db.String(80), unique=False, nullable=False)
    Close_Time = db.Column(db.String(80), unique=False, nullable=False)
    Week_Time = db.Column(db.String(80), unique=False, nullable=False)
    Recommended = db.Column(db.Boolean, unique=False, nullable=False)

    def __repr__(self):
        return '<id %r>' % self.id


class Plates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    RRid = db.Column(db.String, unique=False, nullable=False)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    Image = db.Column(db.String, unique=False, nullable=False)
    Description = db.Column(db.String, unique=False, nullable=False)
    Price = db.Column(db.Float, unique=False, nullable=False)
    Available = db.Column(db.Boolean, unique=False, nullable=False)
    Recommended = db.Column(db.Boolean, unique=False, nullable=False)

    def __repr__(self):
        return '<id %r>' % self.id


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String, unique=False, nullable=False)
    Password = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return '<id %r>' % self.id
db.create_all()
admin = Users (Email = ADMIN_USERNAME , Password = ADMIN_PASSWORD) 
db.session.add(admin)
db.session.commit()

def adder_handler(res):
    try:
        db.session.add(res)
        db.session.commit()
    except exc.IntegrityError:
        return "Already Exist !!"
    return "Success"


@app.route('/api/resturants', methods=['POST', 'GET'])
def Restaurants():
    if request.method == 'POST':
        try:
            content = request.json
        except:
            return "Can't Read Json", 400
        Recommended = False
        try:
            rec = content['is_recommended']
            Rid = content['resturant_id']
            Name = content['name']
            Image = content['image']
            Location = content['location']
            Phone = content['phone']
            Open_Time = content['open_time']
            Close_Time = content['close_time']
            Week_Time = content['week_time']
            rec[2]
            Rid[2]
            Name[2]
            Image[2]
            Location[2]
            Phone[2]
            Open_Time[2]
            Close_Time[2]
            Week_Time[2]
        except:
            return "one ore more parameters is wrong or missing.", 400
        if rec == "true":
            Recommended = True
        new_res = Resturants(Recommended=Recommended, Rid=Rid, Name=Name, Image=Image,
                             Open_Time=Open_Time, Phone=Phone, Close_Time=Close_Time,
                             Week_Time=Week_Time, Location=Location)
        return adder_handler(new_res), 201

    elif request.method == 'GET':
        resturants = (Resturants.query.all())
        jsonres = []
        for res in resturants:
            newjsn = {
                'id': res.id,
                'name': res.Name,
                'resturant_id': res.Rid,
                'image': res.Image,
                'location': res.Location,
                'phone': res.Phone,
                'open_time': res.Open_Time,
                'close_time': res.Close_Time,
                'week_time': res.Week_Time,
                'is_recommended': res.Recommended
            }
            jsonres.append(newjsn)

        final = json.dumps(jsonres, indent=2)
        return (final, 200, {'ContentType': 'application/json'})
       # resturants?resturant_id=STARRE&name=star20%resturant&image=STARREIMG.jpg&location=mersin&phone=905343936779&open_time=10am&close_time=2am&week_time=all&is_recommended=1


@app.route('/api/food', methods=['POST', 'GET'])
def Food():
    if request.method == 'POST':
        try:
            content = request.json
        except:
            return "Can't Read Json", 400
        Recommended = False
        Available = False
        try:
            RRid = content['related_resturant_id']
            Name = content['name']
            Image = content['image']
            Description = content['description']
            Price = content['price']
            rec = content['is_recommended']
            ava = content['is_available']
            RRid[2]
            Name[2]
            Image[2]
            Description[2]
            Price[2]
        except:
            return "one ore more parameters is wrong or missing.", 400
        if rec == 'true':
            Recommended = True

        if ava == 'true':
            Available = True
        new_res = Plates(Recommended=Recommended, RRid=RRid, Name=Name, Image=Image,
                         Description=Description, Price=Price, Available=Available)
        return adder_handler(new_res), 201, {'ContentType': 'application/json'}

    elif request.method == 'GET':
        try:
            RRid = request.args.get('related_resturant_id')
            food = (Plates.query.filter_by(RRid=RRid))
            t = food[0]
        except:
            return 'related resturant id error', 400
        print(food)
        jsonres = []
        for plate in food:
            newjsn = {
                'id': plate.id,
                'name': plate.Name,
                'is_recommended': plate.Recommended,
                'image': plate.Image,
                'description': plate.Description,
                'price': plate.Price,
                'available': plate.Available,
            }
            jsonres.append(newjsn)
        print(jsonres)
        return json.dumps(jsonres, indent=2)
       # food?related_resturant_id=STARRE&name=burger&image=burug.jpg&description=mersin-best-burger&price=24&is_available=1&is_recommended=1


@app.route('/api/resturants/<resname>', methods=['GET'])
def resturant(resname):
    try:
        res = (Resturants.query.filter_by(Rid=resname))[0]
    except IndexError:
        return "No such resturant.", 400
    newjsn = {
        'id': res.id,
        'name': res.Name,
        'resturant_id': res.Rid,
        'image': res.Image,
        'location': res.Location,
        'phone': res.Phone,
        'open_time': res.Open_Time,
        'close_time': res.Close_Time,
        'week_time': res.Week_Time,
        'is_recommended': res.Recommended
    }
    response = json.dumps(newjsn)
    return response


@app.route('/resturants/<resname>/edit', methods=['GET', 'POST'])
@login_required
def edres(resname):
    res = (Resturants.query.filter_by(Rid=resname))[0]
    if request.method == 'POST':
        try:
            res = (Resturants.query.filter_by(Rid=resname))[0]
        except IndexError:
            return "No such resturant.", 400
        for option in resoptions:
            try:
                if not request.form.get(option) == '':
                    setattr(res, option, request.form.get(option))
                    db.session.commit()
            except:
                pass
        if not res.Rid == resname:
            resname = res.Rid
        return redirect(f'/resturants/{resname}/edit')
    return render_template('edit-res.html', resid=resname, resname=resname, options=resoptions, options_names=resoptions_Names, oldvalue=res)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')
        admin = Users.query.filter_by(id='1').first()
        if check_password_hash(admin.Email, username) and check_password_hash(admin.Password, password):
            login_user(admin)
            return redirect('/control-panel')
        return ("bad credentals")
    return render_template('login.html', form=login_form)


@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/')
    else:
        return "not in"


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect('/')


@app.route('/new-res', methods=['GET', 'POST'])
@login_required
def addres():
    new_res_Form = AddRes()
    if request.method == 'POST':
        Recommended = False
        Rid = request.form.get('Rid')
        Name = request.form.get('Name')
        Location = request.form.get('Location')
        Phone = request.form.get('Phone')
        Open_Time = request.form.get('Open_Time')
        Close_Time = request.form.get('Close_Time')
        Week_Time = request.form.get('Week_Time')
        rec = request.form.get('Recommended')
        file = request.files['Image']
        image_url = " "
        if rec == 'true':
            Recommended = True

        if 'Image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        else:
            ext = file.filename.rsplit('.', 1)[1].lower()
            if not ext in ALLOWED_EXTENSIONS:
                flash("extention not allowed")
            else:
                image_url = f"{Rid}_Main_Pic.{ext}"
                #f = open(f"/home/star0k/mysite/static/{image_url}", "w")
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], image_url))
        new_res = Resturants(Recommended=Recommended, Rid=Rid, Name=Name, Image=image_url,
                             Open_Time=Open_Time, Phone=Phone, Close_Time=Close_Time,
                             Week_Time=Week_Time, Location=Location)
        adder_handler(new_res)
        return redirect('/control-panel')

    return render_template('new-res.html', form=new_res_Form)


@app.route('/control-panel')
@login_required
def panel():
    admin = Users.query.filter_by(id='1').first()
    print(current_user.Email)
    if admin.Email == current_user.Email:
        ress = Resturants.query.all()
        return render_template('admin-panel.html', resturants=ress)
    return "hi"


@app.route('/resturants/<resid>/delete/<conf>')
@login_required
def delete_res(resid, conf):
    if conf == 'del':
        resname = (Resturants.query.filter_by(Rid=resid).first()).Name
        return render_template("res-delete.html", resid=resid, resname=resname)
    if conf == 'confirm':
        Resturants.query.filter_by(Rid=resid).delete()
        db.session.commit()
        return redirect('/')


@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect('/login')
    return redirect('/control-panel')


if __name__ == "__main__":
    app.run(debug=True, port=8000)
