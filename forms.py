from flask import flash
from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField, PasswordField
from wtforms.validators import InputRequired, ValidationError


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[InputRequired()])

    def validate_login(self, field):
        if field.data == "":
            flash("Логин не должно быть пустым")
            raise ValidationError()

    password = PasswordField('Пароль', validators=[InputRequired()])

    def validate_passowrd(self, field):
        if field.data == "":
            flash("Пароль не должно быть пустым")
            raise ValidationError()


class RegistrationForm(FlaskForm):
    name = StringField('Имя', validators=[InputRequired(
        message="Поле должно быть заполнено")])

    def validate_name(self, field):
        if field.data == "":
            flash("Имя не должно быть пустым")
            raise ValidationError()

    login = StringField('Логин', validators=[InputRequired(
        message="Поле должно быть заполнено")])

    def validate_login(self, field):
        if field.data == "":
            flash("Логин не должно быть пустым")
            raise ValidationError()

    password = PasswordField('Пароль', validators=[InputRequired(
        message="Поле должно быть заполнено")])

    def validate_passowrd(self, field):
        if field.data == "":
            flash("Пароль не должно быть пустым")
            raise ValidationError()


class AddGoodsForm(FlaskForm):
    name = StringField('Название', validators=[InputRequired()])

    def validate_name(self, field):
        if field.data == "":
            flash("Название не должно быть пустым")
            raise ValidationError()

    price = DecimalField('Цена', validators=[InputRequired()], places=2)

    def validate_price(self, field):
        if field.data < 0:
            flash("Цена не должна быть отрицательной")
            raise ValidationError()

    count = IntegerField('Количество', validators=[InputRequired()])

    def validate_count(self, field):
        if field.data < 0:
            flash("Количество не должно быть отрицательным")
            raise ValidationError()


class UpdateGoodsForm(FlaskForm):
    name = StringField('Название', validators=[InputRequired()])

    def validate_name(self, field):
        if field.data == "":
            flash("Название не должно быть пустым")
            raise ValidationError()

    price = DecimalField('Цена', validators=[InputRequired()], places=2)

    def validate_price(self, field):
        if field.data < 0:
            flash("Цена не должна быть отрицательной")
            raise ValidationError()

    count = IntegerField('Количество', validators=[InputRequired()])

    def validate_count(self, field):
        if field.data < 0:
            flash("Количество не должно быть отрицательным")
            raise ValidationError()


class MainForm(FlaskForm):
    name = StringField('Имя', validators=[InputRequired()])
    price = DecimalField('Цена', validators=[InputRequired()])
    count = IntegerField('Количество', validators=[InputRequired()])


class AddStoreForm(FlaskForm):
    name = StringField('Название', validators=[InputRequired()])

    def validate_name(self, field):
        if field.data == "":
            flash("Название не должно быть пустым")
            raise ValidationError()

