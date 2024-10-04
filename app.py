from models import (engine, Base, session, Product)







if __name__ == '__main__':
    Base.metadata.create_all(engine)