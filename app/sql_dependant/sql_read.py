import uuid
from sqlalchemy import  delete, func, select, update,desc,not_
from sqlalchemy.dialects.mysql import insert
from app.sql_dependant.sql_tables import *
from sqlalchemy.sql.functions import coalesce,concat,count

class Select():

    def user_unique_username_email(data):
        statement = select(User.first_name,User.last_name).where((User.username == data["username"]) | (User.email == data["email"]))
        return statement

    def user_exists_username_password(data):
        statement = select(User.username).where(User.username==data["username"],User.password==data["password"])
        return statement
    
    def products():
        statement = select(Product.id,Product.name,Product.description,Product.price,Product.image)
        return statement
    
    def cart_item(data):
        statement = select(CartItem.id,CartItem.cart_id,CartItem.product_id,CartItem.quantity,Product.name,Product.price).join(
        Product, CartItem.product_id == Product.id).where(
        CartItem.cart_id == select(Cart.id).where(Cart.user_id ==(select(User.id).where(User.username == data["user"])).scalar_subquery()).scalar_subquery())
        return statement

    def cart(data):
        return select(Cart.id).where(Cart.user_id == (select(User.id).where(User.username == data["user"])).scalar_subquery())
    
    def user(data):
        return select(User.id).where(User.username == data["user"])
    
    def product_count():
        return select(count(Product.id))