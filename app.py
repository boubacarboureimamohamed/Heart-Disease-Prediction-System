# Importing essential libraries
import os
import secrets
from PIL import Image
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
import pickle
import numpy as np

# Load the Random Forest CLassifier model
filename = 'heart-disease-prediction-knn-model.pkl'
model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bbf95bae2d0e9f2d8c036d1f45f32f2d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@app.before_first_request
def create_tables():
     db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    dataset_file = db.Column(db.String(20), nullable=False, default='default_dataset.csv')
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.file_name}', '{self.description}', '{self.dataset_file}')"


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/list-dataset')
@login_required
def main_ds():
    ds = Dataset.query.all()
    ds_file = url_for('static', filename='dataset_file/')
    return render_template('main_ds.html', my_datasets=ds,  my_file=ds_file)


@app.route('/data-analysis')
@login_required
def data_an():
    return render_template('data_analysis.html')


@app.route('/add-dataset', methods=['GET', 'POST'])
@login_required
def add_ds():
    form = DatasetForm()
    if form.validate_on_submit():
        ds = Dataset(file_name=form.file_name.data, description=form.description.data)
        db.session.add(ds)
        db.session.commit()
        flash('Votre jeu de données a été importé ! Vous pouvez vérifier les rapports de données maintenant !', 'success')
        return redirect(url_for('main_ds'))
    return render_template('add_ds.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Connexion réussie ! Vous êtes connecté !', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Connexion échouée ! Veuillez vérifier le nom d\'utilisateur ou le mot de passe', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Votre compte a été créé ! Vous pouvez vous connecter maintenant !', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Votre compte a été mis à jour !', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)


@app.route('/prediction-model')
@login_required
def main():
    return render_template('main.html')


@app.route('/prediction-result', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        age = int(request.form['age'])
        sex = request.form.get('sex')
        cp = request.form.get('cp')
        trestbps = int(request.form['trestbps'])
        chol = int(request.form['chol'])
        fbs = request.form.get('fbs')
        restecg = int(request.form['restecg'])
        thalach = int(request.form['thalach'])
        exang = request.form.get('exang')
        oldpeak = float(request.form['oldpeak'])
        slope = request.form.get('slope')
        ca = int(request.form['ca'])
        thal = request.form.get('thal')

        data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
        my_prediction = model.predict(data)

        return render_template('result.html', prediction=my_prediction)


class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur :',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email :',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe :', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmez le mot de passe :',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet e-mail est pris. Veuillez en choisir un autre.')


class LoginForm(FlaskForm):
    email = StringField('Email :',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe :', validators=[DataRequired()])
    submit = SubmitField('Se Connecter')


class UpdateAccountForm(FlaskForm):
    username = StringField('Nom d\'utilisateur',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Télécharger une photo de profil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Mettre à jour')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Cet e-mail est pris. Veuillez en choisir un autre.')


class DatasetForm(FlaskForm):
    file_name = StringField('Nom du fichier :',
                           validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Description :',
                        validators=[DataRequired()])
    ds_file = FileField('Télécharger le fichier de jeu de données :', validators=[FileAllowed(['csv'])])
    submit = SubmitField('Sauvegarder')

    def validate_file_name(self, file_name):
        ds = Dataset.query.filter_by(file_name=file_name.data).first()
        if ds:
            raise ValidationError('Ce nom de fichier est pris. Veuillez en choisir un autre.')


if __name__ == '__main__':
    app.run(debug=True)
