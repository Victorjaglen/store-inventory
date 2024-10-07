from models import (engine, Base, session, Product)
import datetime
import csv


def add_csv():
    with open('inventory.csv', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = int(row[2])
                date = clean_date(row[3])
                new_product = Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date)
                session.add(new_product)
        session.commit()

def clean_date(date_str):
    split_date = date_str.split('/')
    day = int(split_date[1])
    month = int(split_date[0])
    year = int(split_date[2])
    return datetime.date(year, month, day)
    

def clean_price(price_str):
    split_price = price_str.split('$')
    price_float = float(split_price[1])
    return int(price_float * 100)

def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
            \n ****ID ERRROR****
            \rThe ID should be a number.
            \rPress Enter to try again.
            \r*************************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
            \n ****ID ERRROR****
            \rOptions {options}.
            \rPress Enter to try again.
            \r*************************''')
            return


# def view_product():


def menu():
    while True:
        print('''
                \n***Store Inventory***
              \rBelow are the options:

              \rV - View the product
              \rA - Add a new product
              \rB - Backup the database 
              \rE - Exit''')
        choice = input('What would you like to do?: ')
        if choice.lower() in ['a', 'v', 'b', 'e']:
            return choice
        else:
            input('''\nPlease choose one of the options above:
                  \rPress Enter to try again''')

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice.lower() == 'a':
            # add product
            pass

        elif choice.lower() == 'v':
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \n ID Options : {id_options}
                    \r Product id:  ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product).filter(Product.product_id==id_choice).first()
            print(f'''
                \n Product Name: {the_product.product_name}
                \r Product Quantity: {the_product.product_quantity}
                \r Product Price: {the_product.product_price} Cents
                \r Product Updated Date: {the_product.date_updated}''')
            input('\n Press Enter to return to the main menu')
        
        elif choice.lower() == 'b':
            # backup product
            pass
        elif choice.lower() == 'e':
            # exit
            pass
        else:
            print('Goodbye')
            app_running = False




if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
    # clean_date('1/13/2018')
    # add_csv()

    for product in session.query(Product):
        print(product)
    # clean_price('$7.99')
