from app.flaskforms import AddProductForm, RegisterForm,LoginForm,AddToCartForm,RemoveFromCartForm,UpdateCartForm
from flask import redirect, url_for,render_template,request,session,flash
from app.sql_dependant.sql_read import Select
from app.sql_dependant.sql_tables import Cart, Product,User
from app.sql_dependant.sql_connection import sqlconn
from app.sql_dependant.sql_write import Insert,Delete, Update
from app.utils import generate_hash
from . import app
import os
project_dir = os.path.dirname(os.path.abspath(__file__))
photos_dir = "photos/products/"
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name._value(),
            last_name=form.last_name._value(),
            username=form.username._value(),
            email=form.email._value(),
            password=generate_hash(form.password._value()),
            phone=form.phone._value(),
            address=form.address._value(),
            date_of_birth=form.date_of_birth._value())
        sql = sqlconn()
        check = sql.session.execute(Select.user_unique_username_email({"username":user.username,"email":user.email})).mappings().fetchall()
        if len(check)>0:
            sql.close()
            return "Email and/or Username already exists",400
        sql.session.add(user)
        sql.session.commit()
        sql.close()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sql = sqlconn()
        check = sql.session.execute(Select.user_exists_username_password(({"username":form.username._value(),"password":generate_hash(form.password._value())}))).mappings().fetchall()
        if len(check)>0:
            session["user"] = check[0]["username"]
            return redirect(url_for('home')),200
        else: return "You are a fraud",401
    return render_template('login.html', form=form)

@app.route('/logout',methods=['GET'])
def logout():
    if "user" in session:
        session.pop('user', None)
    return redirect(url_for('home')),200

@app.route('/home', methods=['GET'])
def home():
    if "user" in session:
        user =  session["user"]
        return render_template('home.html',user=user)
    return render_template('home.html')

@app.route('/cart', methods=['GET'])
def cart():
    if "user" in session:
        user =  session["user"]
        sql = sqlconn()
        cart_items = sql.session.execute(Select.cart_item({"user":user})).mappings().fetchall()
        total = 0
        for item in cart_items:
            total += item["quantity"]*item["price"]
        return render_template('cart.html',user=user,cart_items=cart_items,total=total,form=RemoveFromCartForm(),form2=UpdateCartForm())
    return redirect(url_for('home')),401

@app.route('/market', methods=['GET'])
def market():
    sql = sqlconn()
    form = AddToCartForm()
    products = listify(sql.session.execute(Select.products()).mappings().fetchall())
    for product in products:
        product["image"] = photos_dir+product["image"]
    if "user" in session:
        user =  session["user"]
        return render_template('market.html',products = products,form = form,user=user)
    return render_template('market.html',products = products,form = form)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if "product_id" in request.form:
        form = AddToCartForm(product_id =request.form["product_id"])
    if form.validate_on_submit():
        if "user" in session:
            user =  session["user"]
            sql = sqlconn()
            check = sql.session.execute(Select.cart({"user":user})).fetchall()
            if len(check)==0:
                cart = Cart(
                    user_id = sql.session.execute(Select.user({"user":user})).fetchall()[0][0]
                )
                sql.session.add(cart)
                sql.session.commit()
            check = sql.session.execute(Select.cart({"user":user})).fetchall()
            sql.execute(Insert.cart_item({"cart_id":check[0]["id"],"product_id":form.product_id._value()}))
            sql.session.commit()
            sql.close()
            return redirect(url_for('cart'))
    return redirect(url_for('login'))

@app.route('/remove-from-cart',methods=['POST'])
def remove_from_cart():
    if "product_id" in request.form:
        form = RemoveFromCartForm(product_id = request.form["product_id"])
    if form.validate_on_submit():
        if "user" in session:
            user =  session["user"]
            sql = sqlconn()
            check = sql.session.execute(Select.cart({"user":user})).fetchall()
            if len(check)==0:
                return "This is wrong and its all your fault",400 
            sql.execute(Delete.cart_item({"cart_id":check[0]["id"],"product_id":form.product_id._value()}))
            sql.session.commit()
            sql.close()
            return redirect(url_for('cart'))
    return redirect(url_for('login'))

@app.route('/update-cart',methods=['POST'])
def update_cart():
    if "product_id" in request.form:
        form = UpdateCartForm(product_id = request.form["product_id"],quantity = request.form["quantity"])
    if form.validate_on_submit():
        if "user" in session:
            user =  session["user"]
            sql = sqlconn()
            check = sql.session.execute(Select.cart({"user":user})).fetchall()
            if len(check)==0:
                return "This is wrong and its all your fault",400 
            if sql.execute(Update.cart_item({"cart_id":check[0]["id"],"product_id":form.product_id._value(),"quantity":form.quantity._value()})):
                sql.session.commit()
            sql.close()
            return redirect(url_for('cart'))
    return redirect(url_for('login'))

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        if "user" not in session:
            return redirect(url_for('login'))
        sql = sqlconn()
        res = sql.session.execute(Select.product_count()).fetchone().count
        filepath = photos_dir+str(res+1)+".jpg"
        form.photo.data.save(project_dir+"/static/"+filepath)
        product = Product(
            name = form.name._value(),
            description = form.description._value(),
            price = form.price._value(),
            image = str(res+1)+".jpg"
        )
        sql.session.add(product)
        sql.commit()
        sql.close()
        flash('Product added successfully!')
        return render_template('add-product.html', form=form)
    return render_template('add-product.html', form=form)

def listify(map):
    templist = []
    for row in map:
        dicx = {}
        for key,val in row.items():
            dicx[key] = val
        templist.append(dicx)
    return templist