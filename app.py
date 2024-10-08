from models import (engine, Base, session, Product)
import datetime
import csv
import time

# Function to add data from a CSV file to the database
def add_csv():
    with open('inventory.csv', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)
        next(data)  # Skip header row
        for row in data:
            name = row[0]
            price = clean_price(row[1])
            quantity = int(row[2])
            date = clean_date(row[3])

            # Check if the product is already in the database
            product_in_db = session.query(Product).filter(Product.product_name == name).one_or_none()

            # If the date is newer, update product details
            if product_in_db:

                if date > product_in_db.date_updated:
                    product_in_db.product_price = price
                    product_in_db.product_quantity = quantity
                    product_in_db.date_updated = date
                    print(f'Updated Product: {name}')

            else:
                # If product is not in the database, add it
                new_product = Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date)
                session.add(new_product)

        session.commit()  # Save changes to the database

# Function to clean and validate the date input
def clean_date(date_str):
    try:
        split_date = date_str.split('/')
        day = int(split_date[1])
        month = int(split_date[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except (ValueError, IndexError):
        input('''
            \n ****Date ERRROR****
            \rThe Date format should include a valid Month Day year separated by /
            \rEx: 12/28/2018 
            \rPress Enter to try again.
            \r*************************''')
        return
    else:
        return return_date

# Function to clean and convert price to an integer (cents)
def clean_price(price_str):
    try:
        split_price = price_str.split('$')
        price_float = float(split_price[1])
    except (ValueError, IndexError):
        input('''
            \n ****Price ERRROR****
            \rThe Price should be a number with the currency symbol up front.
            \rEx: $7.41
            \rPress Enter to try again.
            \r*************************''')
    else:
        return int(price_float * 100)


# Function to clean and validate the product ID
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
            \nThe ID does not exist 
            \rOptions {options}.
            \rPress Enter to try again.
            \r*************************''')
            return


# Function to back up the product data to a CSV file
def backup_csv():
    backup_file = 'backup_inventory.csv'

    try:

        with open(backup_file, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['product_name', 'product_price', 'product_quantity', 'date_updated']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            products = session.query(Product).all()

            # Write product details to CSV
            for product in products:
                writer.writerow({
                    'product_name': product.product_name,
                    'product_price': f'${product.product_price / 100:.2f}',
                    'product_quantity': product.product_quantity,
                    'date_updated': product.date_updated.strftime('%m/%d/%Y')
                })

        print(f'Backup Created Successfully as {backup_file}')

    except Exception as e:
        print(f'Error creating backup: {e}')


# Function to display the menu options
def menu():
    while True:
        print('''
                \n***Store Inventory***
              \rBelow are the options:

              \rV - View the product
              \rA - Add a new product
              \rB - Backup the database
              \rE - Exit''')
        choice = input('\nWhat would you like to do?: ')
        if choice.lower() in ['a', 'v', 'b', 'e']:
            return choice
        else:
            input('''\nPlease choose one of the options above:
                  \rPress Enter to try again''')

# Main app function
def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice.lower() == 'a':
            # Adding a new product
            name = input('Product Name: ')
            quantity_error = True
            while quantity_error:
                try:
                    quantity = int(input('Quantity of the Product: '))
                except ValueError:
                    input('''
            \n ****QuantitY ERRROR****
            \rThe Quantity should be a number.
            \rPress Enter to try again.
            \r*************************''')
                else:
                    quantity_error = False

            # Clean and validate price
            price_error = True
            while price_error:
                price = input('Price of the product (Ex: $5.44): ')
                price_clean = clean_price(price)
                if type(price_clean) == int:
                    price_error = False

            # Clean and validate date
            date_error = True
            while date_error:
                date_updated = input('Date_updated (Ex: 12/28/2018): ')
                date_clean = clean_date(date_updated)
                if type(date_clean) == datetime.date:
                    date_error = False
            new_product = Product(product_name=name, product_price=price_clean, product_quantity=quantity, date_updated=date_clean)

            # Check if product exists in the database
            product_in_db = session.query(Product).filter(Product.product_name == name).one_or_none()

            if product_in_db is None:
                session.add(new_product)
                print('\nProduct Successfully Added')
            else:
                product_in_db.product_price = price_clean
                product_in_db.product_quantity = quantity
                product_in_db.date_updated = date_clean
                print('\nProduct Successfully Added')

            session.commit()  # Save changes to the database
            time.sleep(1.5)

        elif choice.lower() == 'v':
            # View a product
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \rID Options : {id_options}
                    \rProduct id:  ''')
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
            # Back up the database
            backup_csv()
            time.sleep(1.5)

        elif choice.lower() == 'e':
            # Exit the application
            print('\nGoodbye')
            app_running = False


# Initialize database and run the application
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()  # Load initial CSV data
    app()  # Start the application
