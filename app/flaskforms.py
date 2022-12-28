from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField,HiddenField, SubmitField,IntegerField,TextAreaField, FloatField, FileField
from wtforms.validators import InputRequired, Email, Length,DataRequired, NumberRange
from flask_wtf.file import FileRequired, FileAllowed

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=80)])
    phone = StringField('Phone')
    address = StringField('Address')
    date_of_birth = DateField('Date of Birth')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class AddToCartForm(FlaskForm):
    product_id = HiddenField()
    add_to_cart = SubmitField('Add to Cart')

class RemoveFromCartForm(FlaskForm):
    product_id = HiddenField()
    remove_from_cart = SubmitField('Remove from Cart')

class UpdateCartForm(FlaskForm):
    product_id = HiddenField()
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=10)])
    remove_from_cart = SubmitField('Update')

class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    photo = FileField('Photo', validators=[InputRequired(), FileRequired(), FileAllowed(['jpg'], 'JPEG images only!')])