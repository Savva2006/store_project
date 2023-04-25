from flask import Flask, render_template, flash, request, redirect, url_for
from forms import LoginForm, RegistrationForm, AddGoodsForm, MainForm, AddStoreForm, UpdateGoodsForm
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
import pandas as pd


app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Savva/PycharmProjects/store_project/store/pystore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    count = db.Column(db.Integer)
    store_id = db.Column(db.Integer)

    def __init__(self, name, price, count, store_id):
        self.name = name
        self.price = price
        self.count = count
        self.store_id = store_id


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password


@app.route('/insert_store', methods=['POST'])
@login_required
def insert_store():
    db.create_all()
    form = AddStoreForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form['name']
            user_id = request.form['user_id']

            store_data = Stores(name, user_id)
            db.session.add(store_data)

            try:
                db.session.commit()
            except Exception as e:
                flash("Склад ["+name+"] уже существует")
            else:
                flash("Склад успешно добавлен")
        else:
            flash("Вы ввели неверные данные")

    return redirect(url_for('Admin'))


@app.route('/insert', methods=['POST'])
@login_required
def insert():
    db.create_all()
    form = AddGoodsForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form['name']
            price = request.form['price']
            count = request.form['count']
            store_id = request.form['store_id']

            if (db.session.query(db.exists().where(Goods.name == name,
                Goods.store_id == store_id)).scalar() is False):
                goods_data = Goods(name, price, count, store_id)
                db.session.add(goods_data)

                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    flash("Товар ["+name+"] не добавлен")
                else:
                    flash("Товар успешно добавлен")
            else:
                flash("Товар [" + name + "] уже существует в базе")

        else:
            flash("Вы ввели неверные данные")

    return redirect(url_for('Admin'))


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    db.create_all()
    form = UpdateGoodsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            goods_data = (db.session.query(Goods).filter(Goods.id ==
request.form.get('id'), Goods.store_id == request.form.get('store_id')).first())

            goods_data.name = request.form['name']
            goods_data.price = request.form['price']
            goods_data.count = request.form['count']
            goods_data.store_id = request.form['store_id']
        if (db.session.query(db.exists().where(Goods.name ==
            request.form['name'], Goods.store_id == request.form['store_id'],
                Goods.id != request.form['id'])).scalar() is False):
            try:
                db.session.commit()
            except Exception as e:
                flash("Товар ["+request.form['name']+"] не добавлен")
            else:
                flash("Данные успешно обновлены")
        else:
            flash("Вы ввели неверные данные" )

    return redirect(url_for('Admin'))


@app.route('/delete/<id>/<store_id>', methods=['GET', 'POST'])
@login_required
def delete(id, store_id):
    db.create_all()
    goods_data = (db.session.query(Goods).filter(Goods.id == id, Goods.store_id
                                                 == store_id).first())
    db.session.delete(goods_data)
    db.session.commit()
    flash("Товар успешно удален")

    return redirect(url_for('Admin'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def Admin():
    db.create_all()
    form = MainForm()
    name = current_user.login
    user_id = current_user.id
    store = (db.session.query(Stores).filter(Stores.user_id ==
                                             current_user.id).first())
    if store:
        goods_data = (db.session.query(Goods).filter(Goods.store_id ==
                                                     store.id).all())
    else:
        goods_data = ""

    return render_template('admin.html', goods=goods_data, username=name, store=store, user_id=user_id, form=form)


@app.route('/', methods=['GET', 'POST'])
def index():
    db.create_all()
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = (db.session.query(Users).filter(Users.login ==
                    form.login.data).first())

            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('Admin'))

    return render_template('index.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    db.create_all()
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pwd = generate_password_hash(form.password.data, method='sha256')
        name = form.name.data
        login = form.login.data
        password = hashed_pwd

        new_register = Users(name=name, login=login, password=password)
        db.session.add(new_register)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Логин ["+login+"] уже занят")
        else:
            flash("Регистрация прошла успешно, можете войти в систему.")
            return redirect(url_for('index'))

    return render_template('registration.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    db.create_all()
    if request.method == 'POST' and 'file' in request.files:
        f = request.files['file']
        data_xls = pd.read_excel(f)

        for row in data_xls.itertuples():
            name = row[1]
            price = row[2]
            count = row[3]
            store_id = request.form['store_id']

            if name != "":
                if price >= 0:
                    if count >= 0:
                        if (db.session.query(db.exists().where(Goods.name ==
                        name, Goods.store_id == store_id)).scalar() is False):
                            goods_data = Goods(name, price, count, store_id)
                            db.session.add(goods_data)

                            try:
                                db.session.commit()
                            except Exception as e:
                                db.session.rollback()
                                flash("Товар не добавлен")
                        else:
                            flash("Товар ["+name+"] уже существует в базе")
                    else:
                        flash("Количество для ["+name+"] не должно быть отрицательным")
                else:
                    flash("Цена для ["+name+"] не должна быть отрицательной")
            else:
                flash("Название не должно быть пустым")

    return redirect(url_for('Admin'))


if __name__ == "__main__":
    app.run(debug=True)
