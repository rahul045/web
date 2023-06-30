from flask import Flask,redirect, render_template,request
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import text
with open('config.json', 'r') as c:
    params = json.load(c)["params"]
db = SQLAlchemy()
# create the app
app = Flask(__name__)
if(params['local_server']):
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
db.init_app(app)

class  OrderItem(db.Model):
    __tablename__ = "OrderItem"
    id = db.Column(db.Integer ,nullable=False)
    orderDate= db.Column(db.String(50), nullable=False)
    package= db.Column(db.String(250), nullable=False)
    request_weight = db.Column(db.Float, nullable=False)
    result_weight = db.Column(db.Integer, nullable=False)
    requests= db.Column(db.String(256), nullable=False)
    productId = db.Column(db.String(50),  nullable=False)
    order_id=db.Column(db.Integer, primary_key=True)
class  User(db.Model):
    __tablename__="User"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name= db.Column(db.String(45), nullable=False)
    address_id = db.Column(db.Integer, nullable=False)
    isBusiness= db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    create_time= db.Column(db.String(50), nullable=False)
    business_reg_number= db.Column(db.String(50), nullable=False)


class Login(db.Model):
    Id = db.Column(db.Integer, primary_key=True,  nullable=False)
    Password = db.Column(db.String(50), nullable=False)


@app.route("/")
def home():
    return render_template('home.html', params=params)

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('uname')
        password=request.form.get('pass')
        dcust=User.query.filter_by(id=username,password=password).first()
        if(dcust):
            comp = dcust.id
            own = dcust.name
            return render_template("form.html", params=params, st=username,comp=comp,own=own)
        else:
          return render_template("error.html")
    return render_template("home.html",params=params)

@app.route("/password",methods=['GET','POST'])
def password():
    return render_template("change.html",params=params)

@app.route("/change",methods=['GET','POST'])
def change():
    if request.method=='POST':
        mob=request.form.get('mob')
        password=request.form.get('pass')
        duser=User.query.filter_by(phone_number=mob).first()
        if(duser):
            cuser = duser
            cuser.password=password
            db.session.delete(duser)
            db.session.add(cuser)
            db.session.commit()
            return render_template("home.html", params=params)
        else:
          return render_template("error2.html")
    return render_template("home.html",params=params)


@app.route("/form/<string:id>",methods=['GET','POST'])
def form(id):
    if request.method == 'POST':
        date=request.form.get('date')
        item = request.form.get('item')
        count = request.form.get('quantity')
        weight= request.form.get('weight')
        req = request.form.get('req')
        entry=OrderItem(id=id ,orderDate=date,package=item,result_weight=count,productId=500,request_weight=weight,requests=req)
        db.session.add(entry)
        db.session.commit()
        return render_template('home.html', params=params)
@app.route("/dashboard/<string:id>",methods=['GET','POST'])
def dashboard(id):
    orders=OrderItem.query.filter_by(id=id).all()
    return render_template('dashboard.html', params=params,orders=orders)


