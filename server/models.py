
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin



metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)




    restaurant_pizzas = db.relationship(
        'RestaurantPizza', 
        back_populates='restaurant', 
        cascade ='all, delete-orphan'
    )

   
    serialize_rules = ['-restaurant_pizzas.restaurant']

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)





    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

    



    serialize_rules = ['-restaurant_pizzas.pizza']

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id')) #foreign keys are tablename.column
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    


    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    


    serialize_rules = ['-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas']

  




    @validates('price')
    def validates_price(self,key,new_price):
        if not (1 <= new_price <= 30):
            raise ValueError('Price must be between 1 and 30.')
        else:
            return new_price

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"