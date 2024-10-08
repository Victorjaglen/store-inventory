from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the database engine for SQLite
engine = create_engine('sqlite:///inventory.db', echo=False)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Base class for declarative models
Base = declarative_base()

# Product model representing the 'Products' table
class Product(Base):

    __tablename__ = 'Products'

    # Define columns for the table
    product_id = Column(Integer, primary_key=True)
    product_name = Column('Product Name', String)
    product_quantity = Column('Product Quantity', Integer)
    product_price = Column('Product Price', Integer)
    date_updated = Column('Date Updated', Date)

    # String representation of the Product object
    def __repr__(self):
        return f'Name:{self.product_name}, Quantity: {self.product_quantity}, Price: {self.product_price}, Date Updated: {self.date_updated}'
