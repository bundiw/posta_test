# delivery
# sender
# receiver
# fees
# from
# to

from sqlalchemy import Boolean, String, Integer,Float
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv('DATABASE_NAME')

USERNAME = os.getenv('USERNAME')

PASSWORD = os.getenv('PASSWORD')

HOST = os.getenv('HOST')

database_path= "postgresql://{}:{}@{}/{}".format(
    USERNAME, PASSWORD,HOST,DATABASE_NAME
)


db = SQLAlchemy()
migrate = Migrate(compare_type=True)
"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app,db)
    # db.create_all()


# delivery
# sender_address
# receiver_address
# fees
# departure
# destination
# received_status

"""
Delivery

"""
class Delivery(db.Model):
    __tablename__ = 'deliveries'
    
    id = db.Column(Integer, primary_key=True)
    sender_address = db.Column(String, nullable=False)
    receiver_address = db.Column(String, nullable=False)
    fees = db.Column(Float ,nullable=False)
    departure = db.Column(String ,nullable=False)
    destination =db.Column(String ,nullable=False)
    received_status = db.Column(Boolean,nullable=True)
    
    def __init__(self, sender_address, receiver_address, 
                 fees, departure,destination,received_status):
        
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.fees= fees
        self.departure  = departure 
        self.destination = destination
        self.received_status = received_status

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
            'id': self.id,
            'sender_address': self.sender_address,
            'receiver_address': self.receiver_address,
            'fees': self.fees,
            'departure': self.departure,
            'destination': self.destination,
            'received_status': self.received_status
        }


