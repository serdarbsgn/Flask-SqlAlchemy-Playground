import uuid
from sqlalchemy import  delete, func, select, update,desc,not_
from sqlalchemy.dialects.mysql import insert
from app.sql_dependant.sql_tables import *
from sqlalchemy.sql.functions import coalesce,concat,count

class Insert():

    def user(data):
        statement = insert(User)
        return statement
    
    def cart_item(data):
        statement = insert(CartItem).values(cart_id=data["cart_id"],product_id=data["product_id"],quantity=1).on_duplicate_key_update(quantity=CartItem.quantity+1)
        return statement
class Update():
    
    def cart_item(data):
        statement = update(CartItem).where(CartItem.cart_id==data["cart_id"],CartItem.product_id==data["product_id"]).values(quantity = data["quantity"])
        return statement

    def user(data):
        statement = update(User).where(User)
        return statement

class Delete():

    def cart_item(data):
        statement = delete(CartItem).where(CartItem.cart_id==data["cart_id"],CartItem.product_id==data["product_id"])
        return statement

    def user(data):
        statement = delete(User).where(User)
        return statement