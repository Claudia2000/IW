from flask import Flask, render_template, request, session, escape, redirect, url_for, flash,make_response,jsonify
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail, Message
from flask import send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import cv2
from datetime import timedelta
from enum import unique
from flask.helpers import send_file, send_from_directory
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField, form
from wtforms.validators import InputRequired, Length, ValidationError 
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
import os

app=Flask(__name__, instance_path="C:/Users/Claudia/Desktop/iw/privado")
bcrypt=Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://claudia:12345678@127.0.0.1/hotel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='key1'
db=SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"
ma = Marshmallow(app)

app.send_file_max_age_default = timedelta(seconds=1)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cvelizs@ulasalle.edu.pe'
app.config['MAIL_PASSWORD'] = '2000amor'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

class Cliente(db.Model):
    idcliente = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dni = db.Column(db.String(8))
    cel = db.Column(db.String(9))

    def __init__(self, name, dni, cel):
        self.name = name
        self.dni = dni
        self.cel = cel
#db.create_all()
class ClienteSchema(ma.Schema):
    class Meta:
        fields = ("idcliente","name", "dni","cel")

cliente_schema = ClienteSchema()
cliente_schemas = ClienteSchema(many=True)

class Reserva(db.Model):
    idres = db.Column(db.Integer, primary_key=True)
    nomcli = db.Column(db.String(100))
    fecha_ingreso = db.Column(db.Date)
    fecha_salida = db.Column(db.Date)

    def __init__(self, nomcli, fecha_ingreso, fecha_salida):
        self.nomcli=nomcli
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida

db.create_all()

class ReservaSchema(ma.Schema):
    class Meta:
        fields = ("idres","nomcli","fecha_ingreso", "fecha_salida")

reserva_schema = ReservaSchema()
reserva_schemas = ReservaSchema(many=True)

@app.route('/create_cliente', methods=['POST'])
def create_cliente():
    print(request.json)
    name=request.json["name"]
    dni=request.json["dni"]
    cel=request.json["cel"]

    new_cliente = Cliente(name,dni,cel)

    db.session.add(new_cliente)
    db.session.commit()

    return cliente_schema.jsonify(new_cliente)

@app.route('/create_reserva', methods=['POST'])
def create_reserva():
    print(request.json)
    nomcli=request.json["nomcli"]
    fecha_ingreso=request.json["fecha_ingreso"]
    fecha_salida=request.json["fecha_salida"]

    new_reserva = Reserva(nomcli,fecha_ingreso,fecha_salida)

    db.session.add(new_reserva)
    db.session.commit()

    return reserva_schema.jsonify(new_reserva)

def get_reserva2():
    all_reservas = Reserva.query.all()
    result = reserva_schemas.dump(all_reservas)
    return result

@app.route('/get_reserva', methods=['GET'])
def get_reserva():
    all_reservas = Reserva.query.all()
    result = reserva_schemas.dump(all_reservas)
    return jsonify(result)

@app.route('/get_cliente', methods=['GET'])
def get_cliente():
    all_clientes = Cliente.query.all()
    result = cliente_schemas.dump(all_clientes)
    return jsonify(result)

@app.route('/update_cliente/<ide>', methods=["POST"])
def actualizar_elector(ide):

    name=request.json["name"]
    dni=request.json["dni"]
    cel=request.json["cel"]
    cliente_id=Cliente.query.filter_by(idcliente=ide).one()
    cliente_id.name=name
    cliente_id.dni=dni
    cliente_id.cel=cel
    db.session.commit()
    return "Actualizado correctamente"

@app.route('/delete_cliente/<ide>', methods=['POST'])
def eliminar_cliente(ide):
    deletecliente=Cliente.query.filter_by(idcliente=ide).one()
    db.session.delete(deletecliente)
    db.session.commit()
    return "Eliminado correctamente"

def get_cliente2():
    all_clientes = Cliente.query.all()
    result = cliente_schemas.dump(all_clientes)
    return result

@app.route('/confirma', methods=["GET","POST"])
@login_required
def confirma():
    get_cliente=get_cliente2()
    return render_template('principal.html', get_cliente=get_cliente)

@app.route("/reservar", methods=["POST"])
def reserva():
    if request.form.get('action2') == 'Reservas':
        get_reserva=get_reserva2()
        return render_template('reservas.html', get_reserva=get_reserva)

################################################################################### parte 2 (5-7)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    iduser = db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(20), nullable=False, unique=True)
    password =db.Column(db.String(80), nullable=False)

    def get_id(self):
      return (self.iduser)

#Formulario de registro, verifica que el usuario creado no exista
class RegisterForm(FlaskForm): 
    username = StringField("Username", validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
        InputRequired(), Length(min=4)], render_kw={"placeholder": "Password (4 minimum)"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one.")

#Formulario de login, verifica que el usuario exista
class LoginForm(FlaskForm): 
    username = StringField("Username", validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(
        min=4)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if not username:
            raise ValidationError('Account does not exist.')

@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        name=request.form["asunto"]
        email=request.form["user_mail"]
        body=request.form["user_message"]
        msg = Message(name, sender = 'cvelizs@ulasalle.edu.pe', recipients = [email])
        msg.body = body
        mail.send(msg)
        return render_template('clau.html')
    return render_template('clau.html')

@app.route('/home')
def home2():
   return render_template('home.html')

@app.route('/')
@app.route('/login', methods=["GET","POST"])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user: 
            """Validar contraseña encriptada"""
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('confirma'))
    return render_template('login.html', form=form)

"""@app.route('/confirma', methods=["GET","POST"])
@login_required
def confirma():
    return render_template('confirma.html')"""

#cerrar sesión
@app.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    if request.form.get('action1') == 'Cerrar sesion':
        logout_user()
        return redirect(url_for('login'))

@app.route('/register', methods=["GET","POST"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user= User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('login')
    return render_template('register.html', form=form)

#acceder a archivos publicos
@app.route('/publico/<path:filename>', methods=["GET","POST"])
def returnfiled(filename):
    return send_from_directory("static/images/",filename)

#acceder a carpetas protegidas
@app.route('/privado/<path:filename>', methods=["GET","POST"])
@login_required
def secret(filename):
    try:
        return send_from_directory(os.path.join(app.instance_path,''), filename)
    except Exception as e:
        return redirect(url_for('login'))

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'Archivo subido con éxito'

if __name__=="__main__":   
    app.run(port=5000, debug=True)
